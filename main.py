from kakaotalk import *

KakaoTalk_TXT = "talk2.txt"

def main():
    cc = kt_parser()
    cc.send(None)

    messages  = 0
    datecount = 0
    room = None
    realmsg = 0
    outcount = 0
    joincount = 0
    kickcount=0
    sysmsgcount= 0
    msghide = 0
    with open(KakaoTalk_TXT,encoding="utf-8", mode="r") as fp:    
        room = KTChatRoom(fp)
        k = 0
        for line in fp.readlines():
            if item := cc.send(line):
                if isinstance(item, KTMessage):
                    realmsg += 1
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

    print(f'{realmsg=}')
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