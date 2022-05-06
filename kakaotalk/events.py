from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from enum import Enum

from kakaotalk.member import *
from kakaotalk.base import *


__all__ = [
    "KTRoomJoin",
    "KTRoomOUT",
    "KTRoomKick",
    "KTMessageHide",
    "KTDateTime",
    "KTSystemMessage",
    "KTMessage",
    "KTMessageType"
]

@dataclass
class KTEventBaseClass(KTObject):
    event_name : str
    message : str
    _time : datetime

    @property
    def time(self, time_format : str = "%Y-%m-%d %H:%M") -> str:
        '''
        time_format:
            default : "%Y-%m-%d %H:%M" (2022-03-22 15:32)
        '''
        # if isinstance(self._time, datetime):
        return self._time.strftime(time_format)

class KTRoomJoin(KTEventBaseClass):

    def __init__(self, origin : str, name : str, time : datetime):
        self.event_name = "room join"
        self.message = origin
        self.name = name
        self._time = time

class KTRoomOUT(KTEventBaseClass):
    def __init__(self, origin : str, name : str, time : datetime):
        self.event_name = "room out"
        self.message = origin
        self.name = name
        self._time = time

class KTRoomKick(KTEventBaseClass):
    def __init__(self, origin : str, name : str, time : datetime):
        self.event_name = "room Kick"
        self.message = origin
        self.name = name
        self._time = time


class KTMessageHide(KTEventBaseClass):
    '''
    채팅방 관리자가 메시지를 가렸습니다.
    '''
    def __init__(self, time):
        self.event_name = "message hide"
        self.message = "채팅방 관리자가 메시지를 가렸습니다."
        self._time = time

@dataclass
class KTDateTime(KTEventBaseClass):
    '''
    일반 채팅의 경우 보낸 시간이 있기 때문에 직접 datetime 클래스가 _time으로 사용된다.
    하지만, 다른 이벤트의 경우 정확한 시간은 나오지 않으므로 해당되는 날짜만 기록된다.
    '''
    def __init__(self, origin : str, time : datetime):
        self.event_name = "datetime"
        self.message = origin
        self._time = time

class KTSystemMessage(KTEventBaseClass):
    def __init__(self, origin : str, time : datetime):
        self.event_name = "system message"
        self.message = origin
        self._time = time

class KTMessageType(Enum):
    message = "message"
    photo = "photo"
    emoticon = "emoticon"

    @staticmethod
    def _is(isPhoto, isEmoticon):
        if isPhoto:
            return KTMessageType.photo
        if isEmoticon:
            return KTMessageType.emoticon
        return KTMessageType.message

class KTMessage(KTEventBaseClass):

    def __init__(self, sender, time, message, type : KTMessageType):
        super().__init__("message", message, time )
        
        self.sender = sender
        self._type = type

    def _concat(self, string : str) -> KTMessage:
        self.message += string
        return self

    @property
    def message_type(self) -> str:
        return self._type.value

    def __hash__(self) -> int:
        return hash((self.sender, self._time, self.message))

    def __eq__(self, other: KTMessage) -> bool:
        if not isinstance(other, KTMessage):
            return False

        return self.sender == other.sender and \
            self._time == other._time and \
            self.message == other.message