from typing import List
from kakaotalk import *
import kakaotalk

KakaoTalk_TXT = "samples/talk4.txt"

def main():
    with open(KakaoTalk_TXT, encoding='utf-8', mode='r') as fp:
        talks = kakaotalk.Talks(fp=fp)


if __name__ == "__main__":
    main()