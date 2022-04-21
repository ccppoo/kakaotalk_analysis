from abc import abstractmethod
from dataclasses import dataclass
from datetime import datetime

__all__ = [
    "KTRoomJoin",
    "KTRoomOUT",
    "KTRoomKick",
    "KTMessageHide",
    "KTDateTime",
    "KTSystemMessage"
]

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
    '''
    채팅방 관리자가 메시지를 가렸습니다.
    '''
    def __init__(self, time):
        self.event_name = "message hide"
        self.message = "채팅방 관리자가 메시지를 가렸습니다."
        self.time = time

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