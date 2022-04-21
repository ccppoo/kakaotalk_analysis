from __future__ import annotations
from dataclasses import dataclass
from .member import *

__all__ = [
    "KTMessage"
]

@dataclass
class KTMessage:
    sender : KTRoomMember
    time : str = None
    message : str = None

    def concat(self, string : str) -> KTMessage:
        self.message += string
        return self

    def __hash__(self) -> int:
        return hash((self.sender, self.time, self.message))

    def __eq__(self, other: KTMessage) -> bool:
        if not isinstance(other, KTMessage):
            return False

        return self.sender == other.sender and \
            self.time == other.time and \
            self.message == other.message