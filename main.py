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