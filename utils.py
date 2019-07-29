from datetime import datetime, timedelta, timezone


def now():
    JST = timezone(timedelta(hours=+9), 'JST')
    return datetime.now(JST)


def timestamp():
    ts = now().strftime('%Y-%m-%d %H:%M:%S')

    return ts
