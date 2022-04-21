from typing import List
from kakaotalk import *

KakaoTalk_TXT = "samples/talk4.txt"

def main():
    cc = kt_parser()
    cc.send(None)

    messages  = 0
    datecount = 0
    room = None
    outcount = 0
    joincount = 0
    kickcount=0
    sysmsgcount= 0
    msghide = 0
    messages_list: List[KTMessage] = []
    with open(KakaoTalk_TXT,encoding="utf-8", mode="r") as fp:    
        room = KTChatRoom(fp)

        for line in fp.readlines():
            if item := cc.send(line):
                if isinstance(item, KTMessage):
                    messages_list.append(item)
                    messages += 1
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
                if isinstance(item, KTMessageHide):
                    msghide += 1
                if messages_list and isinstance(item, str):
                    messages_list[-1].concat(item)

    print(f"{messages=}")
    print(f"{datecount=}")
    print(f"{outcount=}")
    print(f"{joincount=}")
    print(f"{kickcount=}")
    print(f"{sysmsgcount=}")
    print(f"{msghide=}")
    print(room)

if __name__ == "__main__":
    main()