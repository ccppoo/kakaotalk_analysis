from __future__ import annotations

from dataclasses import dataclass
from types import FunctionType
from typing import IO, ClassVar, Iterator, List, Set
from kakaotalk.events import *
from kakaotalk.events import KTEventBaseClass
from kakaotalk.member import *
from kakaotalk.parser import *
from kakaotalk.room import *
from kakaotalk.base import *


def load(fp : IO) -> Talks:
    '''
    최초로 카톡 내보내기로 받은 txt 파일 분석용
    '''
    room = KTChatRoom(fp)

    all : List[KTObject]= []
    members : Set[KTRoomMember]= set()
    messages : List[KTMessage] = []
    dates : List[KTDateTime]= []
    outs : List[KTRoomOUT]= []
    joins : List[KTRoomJoin]= []
    kicks : List[KTRoomKick]= []
    sysmsg : List[KTSystemMessage]= []
    hidemsg  : List[KTMessageHide]= []

    KTparser = KTParser()
    KTparser.send(None)

    for line in fp.readlines():
        if item := KTparser.send(line):
            if isinstance(item, KTMessage):
                all.append(item)
                members.add(item.sender)
            elif isinstance(item, KTDateTime):
                all.append(item)
                dates.append(item)
            elif isinstance(item, KTRoomOUT):
                all.append(item)
                outs.append(item)
            elif isinstance(item, KTRoomJoin):
                all.append(item)
                joins.append(item)
            elif isinstance(item, KTRoomKick):
                all.append(item)
                kicks.append(item)
            elif isinstance(item, KTSystemMessage):
                all.append(item)
                sysmsg.append(item)
            elif isinstance(item, KTMessageHide):
                all.append(item)
                hidemsg.append(item)
            elif messages and isinstance(item, str):
                assert isinstance(all[-1], KTMessage)
                all[-1]._concat(item)
            else:
                assert item == None

    return Talks(room, all, members, messages, dates, outs, joins, kicks, sysmsg, hidemsg)

@dataclass
class KTCondition:
    '''
    필터링을 하기 위해서 사전에 정의된 함수들
    '''
    Message : ClassVar[FunctionType]
    Time : ClassVar[FunctionType]
    Member : ClassVar[FunctionType]

@dataclass
class Talks:
    '''
    채팅방 구성원에 대한 메타데이터는 주어지지 않아
    채팅을 치지 않은 사람에 대한 정보는 알 수 없음
    '''
    room : KTChatRoom
    all : List[KTEventBaseClass]
    members : Set[KTRoomMember]
    _messages : List[KTMessage]
    dates : List[KTDateTime]
    outs : List[KTRoomOUT]
    joins : List[KTRoomJoin]
    kicks : List[KTRoomKick]
    sysmsg : List[KTSystemMessage]
    hidemsg  : List[KTMessageHide]

    def __len__(self ) -> int:
        return len(self.messages)

    def __repr__(self) -> str:
        return f"<class <kakaotalk.Talks> name={self.room.room_name} saved_at={self.room.saved_at} messages={len(self.messages)}>"

    @property
    def messages(self, ) -> Iterator[KTMessage]:
        for x in self.all:
            if isinstance(x, KTMessage):
                yield x

    @messages.setter
    def messages(self, data) -> None:
        self._messages = data
    
    def filter(condition : KTCondition) -> Talks:
        # TODO : add filtering 
        '''
        사용자가 원하는 조건에 따라서 필터링할 수 있는거
        메세지에 한해서 조건 or 날짜 or 시간대
        '''
        
    def filters(*conditions : KTCondition) -> Talks:
        pass

