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

import re

from topydo.lib.Colors import int_to_ansi, Colors
from topydo.lib.Recurrence import relative_date_to_date

COLOR16_RANGE = [
    (10, '#00ff00', '#000000'), # light green
    (2,  '#008700', '#ffffff'), # green
    (3,  '#ffff00', '#000000'), # yellow
    (1,  '#ff0000', '#ffffff'), # red
]

# https://upload.wikimedia.org/wikipedia/en/1/15/Xterm_256color_chart.svg
# a gradient from green to yellow to red
COLOR256_RANGE = [
            (22, '#005f00', '#ffffff'),
            (28, '#008700', '#ffffff'),
            (34, '#00af00', '#ffffff'),
            (40, '#00d700', '#000000'),
            (46, '#00ff00', '#000000'),
            (82, '#5fff00', '#000000'),
            (118, '#87ff00', '#000000'),
            (154, '#afff00', '#000000'),
            (190, '#dfff00', '#000000'),
            (226, '#ffff00', '#000000'),
            (220, '#ffd700', '#000000'),
            (214, '#ffaf00', '#000000'),
            (208, '#ff8700', '#000000'),
            (202, '#ff5f00', '#ffffff'),
            (196, '#ff0000', '#ffffff'),
]

def _progress_to_color(p_todo, p_safe=True):
    def get_progress():
        """
        Returns a value from 0 to 1 where we are today in a date range. Returns
        a value >1 when a todo item is overdue.
        """

        def get_length():
            """
            Returns the length of the p_todo item in days, based on the recurrence
            period + due date, or the start/due date.
            """
            result = 0

            def diff_days(p_start, p_end):
                if p_start < p_end:
                    diff = p_end - p_start
                    return diff.days

                return 0

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

        if p_todo.is_overdue():
            return 1.1
        elif p_todo.due_date():
            days_till_due = p_todo.days_till_due()
            length = get_length() or 14
            return max((length - days_till_due), 0) / length
        else:
            return 0

    color_range = COLOR16_RANGE if p_safe else COLOR256_RANGE
    progress = get_progress()

    # TODO: remove linear scale to exponential scale
    if progress > 1:
        # overdue, return the last color
        return color_range[-1]
    else:
        # not overdue, calculate position over color range excl. due date
        # color
        pos = round(progress * (len(color_range) - 2))
        return color_range[pos]

def progress_color_code(p_todo, p_safe=True):
    return _progress_to_color(p_todo, p_safe)[0]

def progress_html_color(p_todo):
    """ Returns a tuple (foreground, background) color """
    _, background, foreground = _progress_to_color(p_todo, p_safe=False)
    return (foreground, background)

def color_block(p_todo, p_safe=True):
    color_code = progress_color_code(p_todo, p_safe)
    ansi_code = int_to_ansi(color_code, p_safe=p_safe, p_background=color_code)
    priority_color = Colors().get_priority_color(p_todo.priority())

    return '{} {}'.format(ansi_code, priority_color)

