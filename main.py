from __future__ import annotations

from abc import abstractmethod
from os import PathLike
import re
from dataclasses import dataclass
from datetime import datetime
from typing import IO, List


KakaoTalk_TXT = "talk.txt"


info_msg1 = "불법촬영물 등 식별 및 게재제한 조치 안내"

@dataclass
class KTRoomMember:
    name : str

    def __hash__(self) -> int:
        return hash(self.name)

    def __eq__(self, other: object) -> bool:
        if isinstance(other, KTRoomMember):
            return hash(self) == hash(other)
        return NotImplemented

@dataclass
class KTMessage:
    sender : KTRoomMember
    time : str = None
    message : str = None

    def concat(self, string : str) -> KTMessage:
        self.message += string
        return self

@dataclass
class KTEventBaseClass:
    event_name : str
    message : str

    @abstractmethod
    def __repr__(self) -> str:
        return ""

class KTRoomJoin(KTEventBaseClass):

    def __init__(self, origin : str, name : str):
        self.event_name = "room join"
        self.message = origin
        self.name = name

class KTRoomOUT(KTEventBaseClass):
    def __init__(self, origin : str, name : str):
        self.event_name = "room out"
        self.message = origin
        self.name = name

class KTRoomKick(KTEventBaseClass):
    def __init__(self, origin : str, name : str):
        self.event_name = "room Kick"
        self.message = origin
        self.name = name

class KTMessageHide(KTEventBaseClass):
    pass

@dataclass
class KTDateTime(KTEventBaseClass):
    date : datetime

    def __init__(self, origin : str, time : datetime):
        self.event_name = "datetime"
        self.message = origin
        self.date = time

class KTSystemMessage(KTEventBaseClass):
    def __init__(self, origin : str):
        self.event_name = "system message"
        self.message = origin
        

@dataclass
class KTChatRoom:
    room_name : str = None
    saved_at : str = None
    file_name : str = None
    
    RoomMembers : List[KTRoomMember] = None

    def __init__(self, fp : IO):
        self.__readFile(fp)
    
    def __readFile(self, fp : IO):
        _room_name = f"{fp.readline()}".strip()
        _joined_at = f"{fp.readline()}".strip()
        self.room_name = re.findall('(.*)님과 카카오톡 대화$', _room_name)[0]
        self.saved_at = re.findall('^저장한 날짜 : (.*)$', _joined_at)[0]

def intro(string):
    
    return re.findall('.*? 님과 카카오톡 대화', string)

def parse_msg(string):
    '''
    메세지 파싱
    '''
    return re.findall('\[(.*)\]\s\[(.*)\]\s(.*)', string)

def parse_date(string):
    '''
    날짜 파싱
    '''
    
    return re.findall('^-* ([0-9]+)년 ([0-9]+)월 ([0-9]+)일 (.*) -*$', string)

def parse_in(string):
    '''
    들어온 사람 파싱

    본인이 들어온 경우
    "운영정책을 위반한 메시지로 신고 접수 시 카카오톡 이용에 제한이 있을 수 있습니다."
    이 메세지 추가됨 
    '''
    return re.findall('(.*)님이 들어왔습니다.$', string)

def parse_out(string):
    '''
    나간 사람 파싱
    '''
    return re.findall('(.*)님이 나갔습니다.$', string)

def parse_kick(string):
    '''
    내보낸 사람 파싱
    '''
    return re.findall('(.*)님을 내보냈습니다.$', string)

def parse_infomsg(string):
    '''
    일정주기로 올라오는 오픈톡방 안내메세지
    '''
    isSysMessage = string.strip() == info_msg1
    return string if isSysMessage else None

def start_talk(fp : IO):
    KTChatRoom(fp)

def consumer():
    '''
    여기서 카카오가 내보낸 txt 파일 한 줄 한 줄씩 검사
    \n이 있는 경우 줄이 쪼개진채로 오기 때문에 한 문장이 안됨
    \n 문자 지우고 한 문잘로 만드는 역할을 여기서 함
    '''
    line = yield
    n=0

    aa = 1

    mem = None
    msg = None

    chat_flag = 0
    sep = 0
    rest = None
    while (line):
        if a := parse_date(line):
            line = yield KTDateTime(line, datetime(*[int(x) for x in a[0][0:3]]))
            # print(1)
            sep = 1
            continue
        elif b := parse_in(line):
            line = yield KTRoomJoin(line, b[0])
            # print(2)
            sep = 1
            continue
        elif c := parse_out(line):
            line = yield KTRoomOUT(line, c[0])
            # print(3)
            sep = 1
            continue
        elif e := parse_kick(line):
            line = yield  KTRoomKick(line, e[0])
            # print(4)
            sep = 1
            continue
        elif f := parse_infomsg(line):
            # if aa : print(f"{f=}")
            line = yield KTSystemMessage(line)
            # 새로 들어오면 나오는 시스템 메세지는 2개의 줄로 들어와서 그냥 스킵 
            line = yield 
            sep = 1
            # print(5)
            continue
        elif d := parse_msg(line):
            d = d[0]
            mem = KTRoomMember(d[0])
            msg = KTMessage(mem, d[1], d[2])
            # if aa : print(f"{d=}")
            # 18086
            if not rest == msg:
                line = yield msg
                sep = 0
                # print(6)
                rest = msg
            else:
                sep = 1
        else:
            if rest:
                rest.concat(line)
                line = yield
                # print(7)
                continue
            line = yield

        if sep:
            line = yield rest
            sep = 0
            # print(8)
        # print(f"{line=}")
    if msg:
        yield msg

def main():
    cc = consumer()
    cc.send(None)

    user = set()
    messages  = 0
    datecount = 0
    room = None
    realmsg = 0
    outcount = 0
    joincount = 0
    kickcount=0
    sysmsgcount= 0

    aa = []
    with open(KakaoTalk_TXT,encoding="utf-8", mode="r") as fp:    
        room = KTChatRoom(fp)
        
        for line in fp.readlines():

            if item := cc.send(line):
                if isinstance(item, KTMessage):
                    realmsg += 1
                    messages += 1

                    aa = item
                if isinstance(item, KTDateTime):
                    datecount += 1
                if isinstance(item, KTRoomOUT):
                    outcount += 1
                if isinstance(item, KTRoomJoin):
                    joincount += 1
                if isinstance(item, KTRoomKick):
                    kickcount += 1
                if isinstance(item, KTSystemMessage):
                    sysmsgcount += 1

    print(f'{realmsg=}')
    print(f"{messages=}")
    print(f"{datecount=}")
    print(f"{outcount=}")
    print(f"{joincount=}")
    print(f"{kickcount=}")
    print(f"{sysmsgcount=}")
    print(aa)

info_msg1 = "불법촬영물 등 식별 및 게재제한 조치 안내"
info_msg2 = "그룹 오픈채팅방에서 동영상・압축파일 전송 시 전기통신사업법에 따라 방송통신심의위원회에서 불법촬영물등으로 심의・의결한 정보에 해당하는지를 비교・식별 후 전송을 제한하는 조치가 적용됩니다. 불법촬영물등을 전송할 경우 관련 법령에 따라 처벌받을 수 있사오니 서비스 이용 시 유의하여 주시기 바랍니다."

if __name__ == "__main__":
    main()