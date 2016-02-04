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

""" This module serves for managing output colors. """

from topydo.lib.Config import config

NEUTRAL_COLOR = 0
PROJECT_COLOR = 1
CONTEXT_COLOR = 2
PRIORITY_COLOR = 3
LINK_COLOR = 4
METADATA_COLOR = 5
PROGRESS_COLOR = 6

def get_color(p_type, p_todo, p_256color=False):
    """
    Returns an integer representing a color.

    With 16 colors, an integer [0..16] is returned, with 256 colors the
    corresponding xterm code is returned.

    -1 represents the neutral color.
    """
    def normalize_color(p_input):
        color_names_dict = {
            'black': 0,
            'red': 1,
            'green': 2,
            'yellow': 3,
            'blue': 4,
            'magenta': 5,
            'cyan': 6,
            'gray': 7,
            'darkgray': 8,
            'light-red': 9,
            'light-green': 10,
            'light-yellow': 11,
            'light-blue': 12,
            'light-magenta': 13,
            'light-cyan': 14,
            'white': 15,
        }

        try:
            return color_names_dict[p_input]
        except KeyError:
            return p_input

    def priority_color():
        priority_colors = config().priority_colors()

        try:
            return priority_colors[p_todo.priority()]
        except KeyError:
            return -1

    def progress_color():
        import re
        from topydo.lib.Recurrence import relative_date_to_date

        color16_range = [
            10,  # light green
            2,   # green
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

        color_range = color256_range if p_256color else color16_range
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

    if p_type == CONTEXT_COLOR:
        result = config().context_color()
    elif p_type == PROJECT_COLOR:
        result = config().project_color()
    elif p_type == PRIORITY_COLOR:
        result = priority_color()
    elif p_type == METADATA_COLOR:
        result = config().metadata_color()
    elif p_type == LINK_COLOR:
        result = config().link_color()
    elif p_type == PROGRESS_COLOR:
        result = progress_color()
    else:
        result = -1

    return normalize_color(result)

def get_ansi_color(p_type, p_todo, p_256color=False, p_background=None, p_decoration='normal'):
    """
    Returns ansi code for color based on xterm color id (0-255) and
    decoration, where decoration can be one of: normal, bold, faint,
    italic, or underline. When p_safe is True, resulting ansi code is
    constructed in most compatible way, but with support for only base 16
    colors.
    """

    def ansicode(p_int, p_as_background=False):
        ansi = 4 if p_background else 3

        if p_256color and p_int >= 0:
            return ';{}8;5;{}'.format(ansi, p_int)
        else:
            return ''

        if 0 <= p_int < 8:
            return ';{}{}'.format(ansi, p_int)
        elif 8 <= p_int < 16:
            return ';1;{}{}'.format(ansi, p_int - 8)
        else:
            return ''

    decoration_dict = {
        'normal': '0',
        'bold': '1',
        'faint': '2',
        'italic': '3',
        'underline': '4'
    }

    decoration = decoration_dict[p_decoration]
    fg_color = get_color(p_type, p_todo, p_256color)
    bg_color = get_color(p_background, p_todo, p_256color) if p_background else -1

    return '\033[{}{}{}m'.format(
        decoration,
        ansicode(fg_color),
        ansicode(bg_color, p_as_background=True)
    )

