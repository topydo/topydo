# Topydo - A todo.txt client written in Python.
# Copyright (C) 2014 - 2015 Bram Schoenmakers <bram@topydo.org>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

""" This module deals with relative dates (2d, 5y, Monday, today, etc.) """

import calendar
import re
from datetime import date, timedelta


def _add_months(p_sourcedate, p_months):
    """
    Adds a number of months to the source date.

    Takes into account shorter months and leap years and such.

    https://stackoverflow.com/questions/4130922/how-to-increment-datetime-month-in-python
    """
    month = p_sourcedate.month - 1 + p_months
    year = p_sourcedate.year + month // 12
    month = month % 12 + 1
    day = min(p_sourcedate.day, calendar.monthrange(year, month)[1])

    return date(year, month, day)


def _add_business_days(p_sourcedate, p_bdays):
    """ Adds a number of business days to the source date. """
    result = p_sourcedate
    delta = 1 if p_bdays > 0 else -1

    while abs(p_bdays) > 0:
        result += timedelta(delta)

        weekday = result.weekday()
        if weekday >= 5:
            continue

        p_bdays = p_bdays - 1 if delta > 0 else p_bdays + 1

    return result


def _convert_pattern(p_length, p_periodunit, p_offset=None):
    """
    Converts a pattern in the form [0-9][dwmyb] and returns a date from the
    offset with the period of time added to it.
    """
    result = None

    p_offset = p_offset or date.today()
    p_length = int(p_length)

    if p_periodunit == 'd':
        result = p_offset + timedelta(p_length)
    elif p_periodunit == 'w':
        result = p_offset + timedelta(weeks=p_length)
    elif p_periodunit == 'm':
        result = _add_months(p_offset, p_length)
    elif p_periodunit == 'y':
        result = _add_months(p_offset, p_length * 12)
    elif p_periodunit == 'b':
        result = _add_business_days(p_offset, p_length)

    return result


def _convert_weekday_pattern(p_weekday):
    """
    Converts a weekday name to an absolute date.

    When today's day of the week is entered, it will return next week's date.
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

    shift = 7 - (day - target_day) % 7
    return date.today() + timedelta(shift)


def relative_date_to_date(p_date, p_offset=None):
    """
    Transforms a relative date into a date object.

    The following formats are understood:

    * [0-9][dwmy]
    * 'yesterday', 'today' or 'tomorrow'
    * days of the week (in full or abbreviated)
    """
    result = None
    p_date = p_date.lower()
    p_offset = p_offset or date.today()

    relative = re.match('(?P<length>-?[0-9]+)(?P<period>[dwmyb])$',
                        p_date, re.I)

    monday = 'mo(n(day)?)?$'
    tuesday = 'tu(e(sday)?)?$'
    wednesday = 'we(d(nesday)?)?$'
    thursday = 'th(u(rsday)?)?$'
    friday = 'fr(i(day)?)?$'
    saturday = 'sa(t(urday)?)?$'
    sunday = 'su(n(day)?)?$'

    weekday = re.match('|'.join(
        [monday, tuesday, wednesday, thursday, friday, saturday, sunday]),
        p_date)

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

    elif re.match('yes(terday)?$', p_date):
        result = _convert_pattern('-1', 'd')

    return result
