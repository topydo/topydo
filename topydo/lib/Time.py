# Topydo - A todo.txt client written in Python.
# Copyright (C) 2018 Leo Gaspard <topydo@leo.gaspard.ninja>
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

""" This module provides functions that deal with time. """

import arrow
from datetime import datetime, time, timedelta

from topydo.lib.Config import config

def _time_shift():
    return config().time_shift()

def today():
    return (datetime.now() - timedelta(hours=_time_shift())).date()

def next_day_switch():
    return datetime.combine(today() + timedelta(days=1),
                            time(hour=_time_shift()))

def humanize(p_datetime):
    return arrow.get(str(p_datetime)) \
                .humanize(other=arrow.get(str(today()))) \
                .replace('just now', 'today')
