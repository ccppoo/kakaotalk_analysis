from typing import List
from kakaotalk import *
import kakaotalk


num = 5
KakaoTalk_TXT = f"samples/talk{num}.txt"

csv_temp = f"talk{num}.csv"

def makefield():
    
    pass

def main():
    with open(KakaoTalk_TXT, encoding='utf-8', mode='r') as fp:
        talks = kakaotalk.Talks(fp=fp)

    import csv

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

if __name__ == "__main__":
    main()