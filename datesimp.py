import datetime

months = {1:"jan", 2:"feb", 3:"mar", 4:"apr", 5:"may", 6:"jun", 7:"jul", 8:"aug", 9:"sept", 10:"oct", 11:"nov", 12:"dec"}
days = {1:"monday", 2:"tuesday", 3:"wednesday", 4:"thursday", 5:"friday", 6:"saturday", 7:"sunday"}

def get_year():
    now = datetime.datetime.now()
    return now.year

def get_month():
    now = datetime.datetime.now()
    return months[now.month]

def get_day():
    now = datetime.datetime.now()
    return now.day

def get_weekday():
    now = datetime.datetime.now()
    return days[now.isoweekday()]