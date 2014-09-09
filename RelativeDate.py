""" This module deals with relative dates (2d, 5y, Monday, today, etc.) """

from datetime import date, timedelta
import re

def _convert_pattern(p_length, p_periodunit, p_offset=date.today()):
    """
    Converts a pattern in the form [0-9][dwmy] and returns a date from today
    with the period of time added to it.
    """
    result = None

    p_length = int(p_length)

    if p_periodunit == 'd':
        result = p_offset + timedelta(p_length)
    elif p_periodunit == 'w':
        result = p_offset + timedelta(weeks=p_length)
    elif p_periodunit == 'm':
        # we'll consider a month to be 30 days
        result = p_offset + timedelta(30 * p_length)
    elif p_periodunit == 'y':
        # we'll consider a year to be 365 days (yeah, I'm aware of leap years)
        result = p_offset + timedelta(365 * p_length)

    return result

def _convert_weekday_pattern(p_weekday):
    """
    Converts a weekday name to an absolute date.

    When today's day of the week is entered, it will return today and not next
    week's.
    """
    day_value = {
        'mo': 0,
        'tu': 1,
        'we': 2,
        'th': 3,
        'fr': 4,
        'sa': 5,
        'su': 6
        }

    target_day_string = p_weekday[:2].lower()
    target_day = day_value[target_day_string]

    day = date.today().weekday()

    shift = (target_day - day) % 7
    return date.today() + timedelta(shift)

def relative_date_to_date(p_date, p_offset=date.today()):
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
        result = _convert_pattern(length, period, p_offset)

    elif weekday:
        result = _convert_weekday_pattern(weekday.group(0))

    elif re.match('tod(ay)?$', p_date):
        result = _convert_pattern('0', 'd')

    elif re.match('tom(orrow)?$', p_date):
        result = _convert_pattern('1', 'd')

    return result
