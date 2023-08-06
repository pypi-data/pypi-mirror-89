
import pendulum as p
import datetime as dt
import time as t
from calendar import monthrange

import pytz

Y = '%Y'
YM = '%Y-%m'
YMD = '%Y-%m-%d'
HMS = '%H:%M:%S'
HM = '%H:%M'
YMD_HMS = YMD + ' ' + HMS
YMDTHMS = YMD + 'T' + HMS
YMD_HM = YMD + ' ' + HM

ALL_DATE_FORMATS = ('%Y-%m-%dT%H:%M:%S.%f', '%Y-%m-%d %H:%M:%S.%f',
                    YMDTHMS, YMD_HMS, YMD_HMS + '+00',
                    '%Y-%m-%dT%H:%M', '%Y-%m-%d %H:%M', YMD, '%Y')


def format_dateq(date):
    return '"' + format_date(date) + '"'


def format_date(date):
    return date.strftime(YMD)


def format_timeq(time):
    return '"' + format_time(time) + '"'


def format_time(time):
    return time.strftime(YMD_HMS)


def to_date(value, none=False):
    if none and value is None:
        return None
    if isinstance(value, dt.datetime):
        raise Exception('Use tz-aware conversion')
    elif isinstance(value, dt.date):
        return value
    elif isinstance(value, int):
        return dt.date.fromordinal(value)
    else:
        for format in (YMD, YM, Y):
            try:
                return dt.date(*t.strptime(value, format)[:3])
            except ValueError:
                pass
        raise ValueError('Cannot parse "%s" as a date' % value)


def dates_from(start):
    today = time_to_local_date(now())
    while start <= today:
        yield start
        start += dt.timedelta(days=1)


def to_time(value, none=False):
    if none and value is None:
        return None
    if isinstance(value, dt.datetime):
        return value.replace(tzinfo=pytz.UTC)
    elif isinstance(value, dt.date):
        raise Exception('Use tz-aware conversion')
    elif isinstance(value, int):
        return local_date_to_time(to_date(value))
    elif isinstance(value, float):
        return dt.datetime.fromtimestamp(value, pytz.UTC)
    else:
        for format in ALL_DATE_FORMATS:
            try:
                return dt.datetime.strptime(value, format).replace(tzinfo=pytz.UTC)
            except ValueError:
                pass
        raise ValueError('Cannot parse "%s" as a datetime' % value)


DAY = 'd'
WEEK = 'w'
MONTH = 'm'
YEAR = 'y'


def add_date(date, duration):
    # this only works with dates
    # before, working with datetime, we had confusion between dates and datetimes and unnecessary conversions
    # now, for times, use timedelta.
    date, n, unit = to_date(date), duration[0], duration[1].lower()
    if unit == DAY:
        return date + dt.timedelta(days=n)
    if unit == WEEK:
        return date + dt.timedelta(days=n * 7)
    if unit == MONTH:
        year, month = date.year, date.month + n
        while month > 12:
            month -= 12
            year += 1
        while month < 1:
            month += 12
            year -= 1
        return dt.date(year, month, min(date.day, monthrange(year, month)[1]))
    if unit == YEAR:
        year = date.year + n
        return dt.date(year, date.month, min(date.day, monthrange(year, date.month)[1]))
    raise Exception('Unexpected unit "%s" (need one of %s, %s, %s, %s)' % (unit, DAY, WEEK, MONTH, YEAR))


def format_seconds(seconds):
    sign, seconds = '-' if seconds < 0 else '', abs(seconds)
    if seconds >= 60:
        minutes, seconds = seconds // 60, seconds % 60
        if minutes >= 60:
            hours, minutes = minutes // 60, minutes % 60
            if hours >= 24:
                days, hours = hours // 24, hours % 24
                return '%s%dd %dh%02dm%02ds' % (sign, days, hours, minutes, seconds)
            else:
                return '%s%dh%02dm%02ds' % (sign, hours, minutes, seconds)
        else:
            return '%s%dm%02ds' % (sign, minutes, seconds)
    else:
        return '%s%ds' % (sign, seconds)


def format_minutes(seconds):
    sign, seconds = '-' if seconds < 0 else '', abs(seconds)
    if seconds >= 60:
        minutes, seconds = seconds // 60, seconds % 60
        if minutes >= 60:
            hours, minutes = minutes // 60, minutes % 60
            if hours >= 24:
                days, hours = hours // 24, hours % 24
                return '%s%dd %dh%02dm' % (sign, days, hours, minutes)
            else:
                return '%s%dh%02dm' % (sign, hours, minutes)
        else:
            return '%s%dm%02ds' % (sign, minutes, seconds)
    else:
        return '%s%ds' % (sign, seconds)


# in general, dates are in the local timezone (because diary) while datetimes (referred to as "time")
# are in utc (because database).  however, for display we sometimes need to use local datetimes.  these
# are only exposed as strings.


def local_date_to_time(date, none=False):
    if none and date is None: return None
    date = to_date(date)
    ptime = p.DateTime(year=date.year, month=date.month, day=date.day,
                       tzinfo=p.tz.get_local_timezone()).in_timezone(pytz.UTC)
    return dt.datetime(*ptime.timetuple()[:6], tzinfo=pytz.UTC)


def local_time_to_time(time, none=False):
    if none and time is None: return None
    for format in ALL_DATE_FORMATS:
        try:
            return dt.datetime.strptime(time, format).replace(
                tzinfo=p.tz.get_local_timezone()).astimezone(pytz.UTC)
        except ValueError:
            pass
    raise ValueError(f'Cannot parse "{time}" as a datetime')


def time_to_local_timeq(time, fmt=None, none=False):
    local_time = time_to_local_time(time, fmt=fmt, none=none)
    if local_time:
        local_time = '"' + local_time + '"'
    return local_time


def time_to_local_time(time, fmt=None, none=False):
    if none and time is None: return None
    if fmt:
        return time.astimezone(tz=None).strftime(fmt)
    else:
        local_time = time.astimezone(tz=None).strftime(YMD_HMS)
        if local_time.endswith(' 00:00:00'):
            return time.astimezone(tz=None).strftime(YMD)
        else:
            return local_time


def is_local_time(time):
    try:
        local_time_to_time(time)
        return True
    except:
        return False


def local_time_or_now(date):
    '''
    convert a local date/time into a utc time, using current time as default
    (useful when user entering date on command line and omission defaults to now)
    '''
    if date:
        return local_time_to_time(date)
    else:
        return now()


def now():
    return dt.datetime.now(tz=pytz.UTC)


def now_local():
    return time_to_local_time(now())


def time_to_local_date(time):
    time = to_time(time)
    ptime = p.DateTime(*time.timetuple()[:6], tzinfo=pytz.UTC).in_timezone(p.tz.get_local_timezone())
    return dt.date(year=ptime.year, month=ptime.month, day=ptime.day)


def min_time(a, b):
    if a is None:
        return b
    if b is None:
        return a
    return min(a, b)


def max_time(a, b):
    if a is None:
        return b
    if b is None:
        return a
    return max(a, b)


def extend_range(start, finish, time):
    return min_time(start, time), max_time(finish, time)


def round_hour(time, up=True):
    down = time.replace(second=0, microsecond=0, minute=0)
    if up and down < time:
        return down + dt.timedelta(hours=1)
    else:
        return down


def datetime_to_epoch(datetime):
    return datetime.timestamp()
