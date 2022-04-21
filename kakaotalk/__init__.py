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
                if isinstance(item, KTDateTime):
                    self.dates.append(item.date)
                if isinstance(item, KTRoomOUT):
                    pass
                if isinstance(item, KTRoomJoin):
                    pass
                if isinstance(item, KTRoomKick):
                    pass
                if isinstance(item, KTSystemMessage):
                    pass
                if isinstance(item, KTMessageHide):
                    pass
                if self.messages and isinstance(item, str):
                    self.messages[-1].concat(item)
