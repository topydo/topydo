# Topydo - A todo.txt client written in Python.
# Copyright (C) 2016 Bram Schoenmakers <bram@topydo.org>
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

# when a todo item has not enough information to determine the length, assume
# this length
ASSUMED_TODO_LENGTH = 14  # days

def progress_color(p_todo):
    color16_range = [
        2,   # green
        10,  # light green
        3,   # yellow
        1,   # red
    ]

    # https://commons.wikimedia.org/wiki/File:Xterm_256color_chart.svg
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

        does_recur = p_todo.has_tag('rec')
        start_date = p_todo.start_date()
        due_date = p_todo.due_date()
        creation_date = p_todo.creation_date()

        if does_recur and due_date and not start_date:
            # add negation, offset is based on due date
            recurrence_pattern = p_todo.tag_value('rec')
            neg_recurrence_pattern = re.sub(r'^\+?', '-', recurrence_pattern)

            start = relative_date_to_date(neg_recurrence_pattern, due_date)
            result = diff_days(start, due_date)
        elif due_date and not start_date and not creation_date:
            result = ASSUMED_TODO_LENGTH
        elif due_date and start_date and due_date < start_date:
            result = ASSUMED_TODO_LENGTH
        elif due_date and not start_date and creation_date and due_date < creation_date:
            result = ASSUMED_TODO_LENGTH
        else:
            result = p_todo.length()

        # a todo item is at least one day long
        return max(1, result)

    def get_progress(p_todo, p_consider_parents=True):
        """
        Returns a value from 0 to 1 where we are today in a date range. Returns
        a value >1 when a todo item is overdue.
        """
        def progress_of_parents():
            try:
                parents = p_todo.parents()
            except AttributeError:
                parents = []

            if parents:
                return max(get_progress(parent, False) for parent in parents)
            else:
                return 0

        if p_todo.is_completed():
            return 0
        elif p_todo.is_overdue():
            return 1.1
        elif p_todo.due_date():
            days_till_due = p_todo.days_till_due()
            length = get_length()
            return max((length - days_till_due), 0) / length
        elif p_consider_parents:
            return progress_of_parents()
        else:
            return 0

    use_256_colors = config().colors() == 256
    color_range = color256_range if use_256_colors else color16_range
    progress = get_progress(p_todo)

    # TODO: remove linear scale to exponential scale
    if progress > 1:
        # overdue, return the last color
        return Color(color_range[-1])
    elif p_todo.is_completed():
        # return grey
        return Color(243) if use_256_colors else Color(7)
    else:
        # not overdue, calculate position over color range excl. due date
        # color
        pos = round(progress * (len(color_range) - 2))
        return Color(color_range[pos])
