from typing import List
from kakaotalk import *
import kakaotalk

KakaoTalk_TXT = "samples/talk4.txt"

def main():
    with open(KakaoTalk_TXT, encoding='utf-8', mode='r') as fp:
        talks = kakaotalk.Talks(fp=fp)

    print(len(talks.messages))

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