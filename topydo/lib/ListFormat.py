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
