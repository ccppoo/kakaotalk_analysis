# 카톡 톡 데이터 데이터 처리용 스크립트

카톡 내보내기로 받은 .txt 파일 분석하기 전에 데이터 정제하기 - python

개인적으로 태블루에 쓸 DB, csv 파일 만드는 용도로 작성한 스크립트들

사용방법

```python
import kakaotalk

with open(KakaoTalk_TXT, encoding='utf-8', mode='r') as fp:
    talks = kakaotalk.Talks(fp=fp)

talks.members

len(talks.messages)
```
