from dataclasses import dataclass
from typing import List, IO
from .member import *
import re

def intro(string):
    
    return re.findall('.*? 님과 카카오톡 대화', string)

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