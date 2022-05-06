# 카톡 톡 데이터 데이터 처리용 스크립트

카톡 내보내기로 받은 .txt 파일 분석하기 전에 데이터 정제하기 - python

개인적으로 태블루에 쓸 DB, csv 파일 만드는 용도로 작성한 스크립트들

필자는 태블루에 이용하기 위한 CSV 파일 생성을 목적으로 적어놨기 때문에 csv 모듈을 쓴 것이고,

파이썬 `matplotlib`을 이용해서 차트 그릴 수 있음

아래 예시 코드에서 `myFilter` 처럼 본인의 입맛에 맞게 사용하시면 됩니다.

```python
# main.py
from datetime import datetime
from os import PathLike
from kakaotalk import *
import kakaotalk
import csv

KakaoTalk_TXT = "<Path to kakaotalk txt file>"

all_event_parsed = "kakaotalk_events.csv"
Join_Out_Kick_event_parsed = "join_out_kick_events.csv"
message_pasred = "talk_parsed.csv"
filter_date = 'date_filtered_messages.csv'

def loadFile(filename : PathLike) -> Talks:
    with open(filename, encoding='utf-8', mode='r') as fp:
        return kakaotalk.load(fp=fp)

def makeCSV_all_event():

    talks = loadFile(KakaoTalk_TXT)

    with open(all_event_parsed, newline='', encoding='utf-8', mode='w') as fp:
        writer = csv.writer(fp)
        writer.writerow(['Event Name','Message Type', 'Sender', 'TIME' ,'message'])

        for m in filter(lambda x : not isinstance(x, KTMessage), talks.all):
            writer.writerow([
                m.event_name,
                m.time,
                m.message
            ])

def makeCSV_Join_Out_Kick_event():

    talks = loadFile(KakaoTalk_TXT)

    myFilter = lambda x : isinstance(x, (KTRoomJoin, KTRoomOUT, KTRoomKick) )

    with open(Join_Out_Kick_event_parsed, newline='', encoding='utf-8', mode='w') as fp:
        writer = csv.writer(fp)
        writer.writerow(['Event Name','Message Type', 'Sender', 'TIME' ,'message'])

        for m in filter(myFilter, talks.all):
            writer.writerow([
                m.event_name,
                m.time,
                m.message,
                m.name
            ])

def makeCSV_all_messages():

    talks = loadFile(KakaoTalk_TXT)

    with open(message_pasred, newline='', encoding='utf-8', mode='w') as fp:
        writer = csv.writer(fp)
        writer.writerow(['Type', 'Sender', 'Time' ,'Message'])

        for m in talks.messages:
            writer.writerow([
                m.message_type,
                m.sender.name,
                m.time,
                m.message
            ])

def filter_messages_by_date():
    talks = loadFile(KakaoTalk_TXT)

    start = datetime(2022, 3, 1)
    end = datetime(2022, 3, 31)
    myFilter = lambda x : x._time >= start and x._time <= end

    with open(filter_date, newline='', encoding='utf-8', mode='w') as fp:
        writer = csv.writer(fp)
        writer.writerow(['Type', 'Sender', 'Time' ,'Message'])

        for m in filter(myFilter, talks.messages):
            writer.writerow([
                m.message_type,
                m.sender.name,
                m.time,
                m.message
            ])

if __name__ == "__main__":
    makeCSV_all_event()
    makeCSV_all_messages()
    makeCSV_Join_Out_Kick_event()
    filter_messages_by_date()
```

특이사항

-   답장하는 톡의 경우 답장하는 대상은 안나옴
-   사진을 보냈을 경우 단순히 '사진' 또는 '사진 2장' 이렇게 나오기 때문에 단순히 톡으로 '사진'보내면 분간 못함
