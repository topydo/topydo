# Topydo - A todo.txt client written in Python.
# Copyright (C) 2014 - 2015 Bram Schoenmakers <me@bramschoenmakers.nl>
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

""" Ulities for formatting output with "list_format" option."""

import arrow

def filler(p_str, p_len):
    """
    Returns p_str preceded by additional spaces if p_str is shorter than p_len.
    """
    to_fill = p_len - len(p_str)
    return to_fill*' ' + p_str

def humanize_date(p_datetime):
    now = arrow.now()
    date = now.replace(day=p_datetime.day, month=p_datetime.month, year=p_datetime.year)
    return date.humanize()

def humanize_dates(p_due=None, p_start=None, p_creation=None):
    """
    Returns string with humanized versions of p_due, p_start and p_creation.
    Examples:
    - all dates: "16 days ago, due in a month, started 2 days ago"
    - p_due and p_start: "due in a month, started 2 days ago"
    - p_creation and p_due: "16 days ago, due in a month"
    """
    dates_list = []
    if p_creation:
        dates_list.append(humanize_date(p_creation))
    if p_due:
        dates_list.append('due ' + humanize_date(p_due))
    if p_start:
        now = arrow.now().date()
        start = humanize_date(p_start)
        if p_start <= now:
            dates_list.append('started ' + start)
        else:
            dates_list.append('starts ' + start)

    return ', '.join(dates_list)

def strip_placeholder_braces(p_matchobj):
    """
    Returns string with conditional braces around placeholder stripped and
    percent sign glued into placeholder character.

    Returned string is composed from 'start', 'before', 'placeholder', 'after',
    'whitespace', and 'end' match-groups of p_matchobj. Conditional braces are
    stripped from 'before' and 'after' groups. 'whitespace', 'start', and 'end'
    groups are preserved without any change.

    Using this function as an 'repl' argument in re.sub it is possible to turn:
        %{(}B{)}
    into:
        (%B)
    """
    before = p_matchobj.group('before') or ''
    placeholder = p_matchobj.group('placeholder')
    after = p_matchobj.group('after') or ''
    whitespace = p_matchobj.group('whitespace') or ''

    return before + '%' + placeholder + after + whitespace
