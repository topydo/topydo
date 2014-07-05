from datetime import date, timedelta
import re

def _convert_pattern(p_length, p_period):
    result = None

    p_length = int(p_length)

    if p_period == 'd':
        result = date.today() + timedelta(p_length)
    elif p_period == 'w':
        result = date.today() + timedelta(weeks=p_length)
    elif p_period == 'm':
        # we'll consider a month to be 30 days
        result = date.today() + timedelta(30 * p_length)
    elif p_period == 'y':
        # we'll consider a year to be 365 days (yeah, I'm aware of leap years)
        result = date.today() + timedelta(365 * p_length)

    return result

def _convert_weekday_pattern(p_weekday):
    day_value = {
            'mo': 0,
            'tu': 1,
            'we': 2,
            'th': 3,
            'fr': 4,
            'sa': 5,
            'su': 6
            }

    targetDayString = p_weekday[:2].lower()
    targetDay = day_value[targetDayString]

    day = date.today().weekday()

    shift = (targetDay - day) % 7
    return date.today() + timedelta(shift)

def relative_date_to_date(p_date):
    """
    Transforms a relative date into a date object.

    The following formats are understood:

    * [0-9][dwmy]
    * 'today' or 'tomorrow'
    * days of the week (in full or abbreviated)
    """

    result = None
    p_date = p_date.lower()

    relative = re.match('(?P<length>[0-9]+)(?P<period>[dwmy])$', p_date, re.I)
    weekday = re.match('mo(n(day)?)?$|tu(e(sday)?)?$|we(d(nesday)?)?$|th(u(rsday)?)?$|fr(i(day)?)?$|sa(t(urday)?)?$|su(n(day)?)?$', p_date)

    if relative:
        length = relative.group('length')
        period = relative.group('period')
        result = _convert_pattern(length, period)

    elif weekday:
        result = _convert_weekday_pattern(weekday.group(0))

    elif re.match('tod(ay)?$', p_date):
        result = _convert_pattern('0', 'd')

    elif re.match('tom(orrow)?$', p_date):
        result = _convert_pattern('1', 'd')

    return result
