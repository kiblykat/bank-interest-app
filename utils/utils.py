import datetime


def validate_date(date_str):
    try:
        datetime.datetime.strptime(date_str, "%Y%m%d")
        return True
    except:
        return False
