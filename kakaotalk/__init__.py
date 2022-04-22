from dataclasses import dataclass
from datetime import datetime
from typing import IO, List, Set
from kakaotalk.events import *
from kakaotalk.member import *
from kakaotalk.message import *
from kakaotalk.parser import *
from kakaotalk.room import *

@dataclass
class Talks:

    members : Set[KTRoomMember] = None
    messages : List[KTMessage] = None
    dates : List[datetime] = None
    room : KTChatRoom = None

    def __init__(self, fp: IO) -> None:
        room = KTChatRoom(fp)

        self.members = set()
        self.messages = []
        self.dates = []

        cc = kt_parser()
        cc.send(None)
        for line in fp.readlines():
            if item := cc.send(line):
                if isinstance(item, KTMessage):
                    self.messages.append(item)
                    self.members.add(item.sender)
                elif isinstance(item, KTDateTime):
                    self.dates.append(item.date)
                elif isinstance(item, KTRoomOUT):
                    pass
                elif isinstance(item, KTRoomJoin):
                    pass
                elif isinstance(item, KTRoomKick):
                    pass
                elif isinstance(item, KTSystemMessage):
                    pass
                elif isinstance(item, KTMessageHide):
                    pass
                elif self.messages and isinstance(item, str):
                    self.messages[-1]._concat(item)
                else:
                    assert item == None
    
    def __len__(self ) -> int:
        return len(self.messages)

    def __repr__(self) -> str:
        return f"<class <kakaotalk.Talks> name={self.room.room_name} saved_at={self.room.saved_at} messages={len(self.messages)}>"

    @property
    def messages(self, ) -> List[KTMessage]:
        return self.messages