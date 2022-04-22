# 카톡 톡 데이터 데이터 처리용 스크립트

카톡 내보내기로 받은 .txt 파일 분석하기 전에 데이터 정제하기 - python

개인적으로 태블루에 쓸 DB, csv 파일 만드는 용도로 작성한 스크립트들

사용방법

```python
# main.py
import kakaotalk

KakaoTalk_TXT = f"samples/talk{num}.txt"

csv_temp = f"talk{num}.csv"

with open(KakaoTalk_TXT, encoding='utf-8', mode='r') as fp:
    talks = kakaotalk.Talks(fp=fp)


with open(csv_temp, newline='', encoding='utf-8', mode='w') as fp:
    writer = csv.writer(fp)
    writer.writerow(['Type', 'Sender', 'TIME' ,'message'])

    format_FULL= "%Y-%m-%d %H:%M"
    format_YMD = "%Y-%m-%d"
    format_HM = "%H:%M"

    for m in talks.messages:
        writer.writerow([
            m.type,
            m.sender.name,
            m.time.strftime(format_FULL),
            m.message
        ])
```

특이사항

-   답장하는 톡의 경우 답장하는 대상은 안나옴
-   사진을 보냈을 경우 단순히 '사진' 또는 '사진 2장' 이렇게 나오기 때문에 단순히 톡으로 '사진'보내면 분간 못함
