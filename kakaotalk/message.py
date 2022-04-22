from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from .member import *

__all__ = [
    "KTMessage",
    "KTMessageType"
]

class KTMessageType(Enum):
    message = "message"
    photo = "photo"
    emoticon = "emoticon"

@dataclass
class KTMessage:
    sender : KTRoomMember
    time : datetime
    message : str
    isPhoto : bool
    isEmoticon : bool

    def _concat(self, string : str) -> KTMessage:
        self.message += string
        return self

    @property
    def type(self) -> str:
        if self.isPhoto:
            return KTMessageType.photo.value
        elif self.isEmoticon:
            return KTMessageType.emoticon.value
        else:
            return KTMessageType.message.value

    def __hash__(self) -> int:
        return hash((self.sender, self.time, self.message))

    def __eq__(self, other: KTMessage) -> bool:
        if not isinstance(other, KTMessage):
            return False

        return self.sender == other.sender and \
            self.time == other.time and \
            self.message == other.message