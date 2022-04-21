import re
from datetime import datetime
from .consts import *
from .message import *
from .events import *
from .member import *

__all__ = [
    "kt_parser"
]

def parse_msg(string):
    '''
    메세지 파싱
    '''
    # return re.findall('^\[(.*)\]\s\[(오후|오전 [0-9]+:[0-9]+)\]\s(.*)[^\n]+$', string)
    return re.findall('^\[(.*)\]\s\[((?:오후|오전) [0-9]+:[0-9]+)\]\s(.*)$', string)
    return re.findall('\[(.*)\]\s\[(.*)\]\s(.*)', string)

def parse_date(string):
    '''
    날짜 파싱
    '''
    return re.findall('^-* ([0-9]+)년 ([0-9]+)월 ([0-9]+)일 (.*) -*$', string)

def parse_in(string):
    '''
    들어온 사람 파싱

    본인이 들어온 경우
    "운영정책을 위반한 메시지로 신고 접수 시 카카오톡 이용에 제한이 있을 수 있습니다."
    이 메세지 추가됨 
    '''
    return re.findall('(.*)님이 들어왔습니다.$', string)

def parse_out(string):
    '''
    나간 사람 파싱
    '''
    return re.findall('(.*)님이 나갔습니다.$', string)

def parse_kick(string):
    '''
    내보낸 사람 파싱
    '''
    return re.findall('(.*)님을 내보냈습니다.$', string)

def parse_infomsg(string):
    '''
    일정주기로 올라오는 오픈톡방 안내메세지
    '''
    isSysMessage = string.strip() == INFO_MESSAGE_1
    return string if isSysMessage else None

def parse_msg_hide(string):

    return string.strip() == "채팅방 관리자가 메시지를 가렸습니다."

def change_time(string):
    AM = "오전"
    PM = "오후"
    meridiem, hour, minute = re.findall('^(오후|오전) ([0-9]+):([0-9]+)$', string)[0]
    hour, minute = int(hour), int(minute)

    if meridiem == PM and not hour==12:
        hour += 12

    if meridiem == AM and hour==12:
        hour -= 12

    return hour, minute

def kt_parser():
    '''
    여기서 카카오가 내보낸 txt 파일 한 줄 한 줄씩 검사
    \n이 있는 경우 줄이 쪼개진채로 오기 때문에 한 문장이 안됨
    \n 문자 지우고 한 문잘로 만드는 역할을 여기서 함
    '''
    line = yield
    curr_date : datetime = None
    mem = None
    msg = None

    sep = 0
    rest = None
    while (line):
        if parsed := parse_date(line):
            curr_date = KTDateTime(line, datetime(*[int(x) for x in parsed[0][0:3]]))
            line = yield curr_date
            sep = 1
            continue
        elif parsed := parse_in(line):
            line = yield KTRoomJoin(line, parsed[0])
            sep = 1
            continue
        elif parsed := parse_out(line):
            line = yield KTRoomOUT(line, parsed[0])
            sep = 1
            continue
        elif parsed := parse_kick(line):
            line = yield  KTRoomKick(line, parsed[0])
            sep = 1
            continue
        elif parsed := parse_infomsg(line):
            line = yield KTSystemMessage(line)
            # 새로 들어오면 나오는 시스템 메세지는 2개의 줄로 들어와서 그냥 스킵 
            line = yield 
            sep = 1
            continue
        elif parsed := parse_msg_hide(line):
            line = yield KTMessageHide("time temp")
            continue
        elif parsed := parse_msg(line):
            parsed = parsed[0]
            
            mem = KTRoomMember(parsed[0])
            hour, minute = change_time(parsed[1])
            dd = curr_date.date
            ttime = datetime(dd.year, dd.month, dd.day, hour, minute)
            msg = KTMessage(sender= mem, time = ttime, message=parsed[2])

            if not rest == msg:
                line = yield msg
                sep = 0
                rest = msg
            else:
                sep = 1
        else:
            if rest:
                # parse_msg 에서 regex 마지막 메세지 찾는 것중에 (.*)여기에 \n 포함이 안되어서 추가
                rest.concat(f"\n{line.strip()}")
                line = yield
                continue
            line = yield

        if sep:
            line = yield rest
            sep = 0

    if msg:
        # 마지막에 남은 메세지 내보내기
        yield rest