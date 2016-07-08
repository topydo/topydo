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

""" Provides a pretty printer filter that colorizes todo items. """

import re

from topydo.lib.Color import AbstractColor
from topydo.lib.Config import config
from topydo.lib.PrettyPrinterFilter import PrettyPrinterFilter
from topydo.lib.TopydoString import TopydoString


class PrettyPrinterColorFilter(PrettyPrinterFilter):
    """
    Adds colors to the todo string by inserting ANSI codes.

    Should be passed as a filter in the filter list of pretty_print()
    """

    def filter(self, p_todo_str, p_todo):
        """ Applies the colors. """
        if config().colors():
            p_todo_str = TopydoString(p_todo_str, p_todo)

            priority_color = config().priority_color(p_todo.priority())

            colors = [
                (r'\B@(\S*\w)', AbstractColor.CONTEXT),
                (r'\B\+(\S*\w)', AbstractColor.PROJECT),
                (r'\b\S+:[^/\s]\S*\b', AbstractColor.META),
                (r'(^|\s)(\w+:){1}(//\S+)', AbstractColor.LINK),
            ]

            # color by priority
            p_todo_str.set_color(0, priority_color)

            for pattern, color in colors:
                for match in re.finditer(pattern, p_todo_str.data):
                    p_todo_str.set_color(match.start(), color)
                    p_todo_str.set_color(match.end(), priority_color)

            p_todo_str.append('', AbstractColor.NEUTRAL)

        return p_todo_str

