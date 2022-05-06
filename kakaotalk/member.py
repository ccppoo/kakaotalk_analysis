from dataclasses import dataclass
from kakaotalk.base import *

__all__ = [
    "KTRoomMember"
]

@dataclass
class KTRoomMember(KTObject):

    name : str

    def __hash__(self) -> int:
        return hash(self.name)

    def __eq__(self, other: object) -> bool:
        if isinstance(other, KTRoomMember):
            return hash(self) == hash(other)
        return NotImplemented