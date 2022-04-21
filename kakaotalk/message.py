from __future__ import annotations
from dataclasses import dataclass
from .member import *


@dataclass
class KTMessage:
    sender : KTRoomMember
    time : str = None
    message : str = None

    def concat(self, string : str) -> KTMessage:
        self.message += string
        return self