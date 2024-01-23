import re
from datetime import datetime

def minute_calculator(start: str, end: str) -> datetime:
    format = '%H:%M'
    match_start = datetime.strptime(start,format)
    match_end = datetime.strptime(end,format)
    deltacorrector = datetime.strptime("00:00",format) #correction for the return not to be a timedelta class
    return match_end - match_start + deltacorrector

def caps_lock_ignore(text):
    return re.compile(text,re.I)     