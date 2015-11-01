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

"""
Various utility functions.
"""

import re

from collections import namedtuple
from datetime import date


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
                int(parsed_date.group(1)),  # year
                int(parsed_date.group(2)),  # month
                int(parsed_date.group(3))   # day
            )
        else:
            raise ValueError

    return result


def is_valid_priority(p_priority):
    return p_priority is not None and re.match(r'^[A-Z]$', p_priority) is not None


def escape_ansi(p_string):
    return escape_ansi.pattern.sub('', p_string)

escape_ansi.pattern = re.compile(r'\x1b[^m]*m')

def get_terminal_size():
    """
    Try to determine terminal size at run time. If that is not possible,
    returns the default size of 80x24.
    """
    try:
        from shutil import get_terminal_size # pylint: disable=no-name-in-module
    except ImportError:
        from backports.shutil_get_terminal_size import get_terminal_size

    try:
        sz = get_terminal_size()
    except ValueError:
        """
        This can result from the 'underlying buffer being detached', which
        occurs during running the unittest on Windows (but not on Linux?)
        """
        terminal_size = namedtuple('Terminal_Size', 'columns lines')
        sz = terminal_size((80, 24))

    return sz
