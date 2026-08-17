import datetime

# 日期格式常量
DATE_FORMAT_YYYYMMDD = "%Y-%m-%d"
DATE_FORMAT_YYYYMMDD_HHMMSS = "%Y-%m-%d %H:%M:%S"

# 格式化日期
def format_date(date:datetime.datetime,format_str:str):
    return date.strftime(format_str)

def format_date_time(date=datetime.datetime.now()):
    return date.strftime(DATE_FORMAT_YYYYMMDD_HHMMSS)

# 格式化当前时间
def format_now():
    date = datetime.datetime.now()
    return format_date(date,DATE_FORMAT_YYYYMMDD)