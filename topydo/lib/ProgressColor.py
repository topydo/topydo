# Topydo - A todo.txt client written in Python.
# Copyright (C) 2016 Bram Schoenmakers <me@bramschoenmakers.nl>
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

import re

from topydo.lib.Color import Color
from topydo.lib.Config import config
from topydo.lib.Recurrence import relative_date_to_date

def progress_color(p_todo):
    color16_range = [
        2,   # green
        10,  # light green
        3,   # yellow
        1,   # red
    ]

    # https://upload.wikimedia.org/wikipedia/en/1/15/Xterm_256color_chart.svg
    # a gradient from green to yellow to red
    color256_range = \
        [22, 28, 34, 40, 46, 82, 118, 154, 190, 226, 220, 214, 208, 202, 196]

    def get_length():
        """
        Returns the length of the p_todo item in days, based on the recurrence
        period + due date, or the start/due date.
        """
        result = 0

        def diff_days(p_start, p_end):
            """
            Returns the difference in days between p_start and p_end, where
            start is before due.
            """
            diff = p_end - p_start
            return diff.days

        if p_todo.has_tag('rec') and p_todo.due_date():
            # add negation, offset is based on due date
            recurrence_pattern = p_todo.tag_value('rec')
            neg_recurrence_pattern = re.sub('^\+?', '-', recurrence_pattern)

            start = relative_date_to_date(
                neg_recurrence_pattern, p_todo.due_date())
            due = p_todo.due_date()

            result = diff_days(start, due)
        else:
            result = p_todo.length()

        return result

    def get_progress():
        """
        Returns a value from 0 to 1 where we are today in a date range. Returns
        a value >1 when a todo item is overdue.
        """

        if p_todo.is_overdue():
            return 1.1
        elif p_todo.due_date():
            days_till_due = p_todo.days_till_due()
            length = get_length() or 14
            return max((length - days_till_due), 0) / length
        else:
            return 0

    color_range = color256_range if config().colors() == 256 else color16_range
    progress = get_progress()

    # TODO: remove linear scale to exponential scale
    if progress > 1:
        # overdue, return the last color
        return Color(color_range[-1])
    else:
        # not overdue, calculate position over color range excl. due date
        # color
        pos = round(progress * (len(color_range) - 2))
        return Color(color_range[pos])
