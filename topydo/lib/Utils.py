# Topydo - A todo.txt client written in Python.
# Copyright (C) 2014 Bram Schoenmakers <me@bramschoenmakers.nl>
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

"""
Various utility functions.
"""

from datetime import date
import re

def date_string_to_date(p_date):
    """
    Given a date in YYYY-MM-DD, returns a Python date object. Returns None
    if the date is invalid.
    """
    result = None

    if p_date:
        parsed_date = re.match(r'(\d{4})-(\d{2})-(\d{2})', p_date)
        if parsed_date:
            result = date(
                int(parsed_date.group(1)), # year
                int(parsed_date.group(2)), # month
                int(parsed_date.group(3))  # day
            )
        else:
            raise ValueError

    return result

def is_valid_priority(p_priority):
    return p_priority != None and re.match(r'^[A-Z]$', p_priority) != None

def escape_ansi(p_string):
    return escape_ansi.pattern.sub('', p_string)

escape_ansi.pattern = re.compile(r'\x1b[^m]*m')
