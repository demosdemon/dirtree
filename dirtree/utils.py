import datetime

from dateutil import tz


def identity(x):
    '''return the input value'''
    return x


def local_timestamp(ts):
    '''return a dst aware `datetime` object from `ts`'''
    return datetime.datetime.fromtimestamp(ts, tz.tzlocal())


def strftime(ts):
    if ts is None:
        return 'None'

    if isinstance(ts, int):
        ts = local_timestamp(ts)

    return ts.strftime('%F %T %z')
