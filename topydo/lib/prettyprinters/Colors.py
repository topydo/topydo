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

""" Provides a pretty printer filter that colorizes todo items. """

import re

from topydo.lib.Color import Color
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
            p_todo_str = TopydoString(p_todo_str)

            priority_color = config().priority_color(p_todo.priority())
            neutral_color = Color('NEUTRAL')

            colors = [
                (r'\B@(\S*\w)', config().context_color()),
                (r'\B\+(\S*\w)', config().project_color()),
                (r'\b\S+:[^/\s]\S*\b', config().metadata_color()),
                (r'(^|\s)(\w+:){1}(//\S+)', config().link_color()),
            ]

            for pattern, color in colors:
                for match in re.finditer(pattern, p_todo_str.data):
                    p_todo_str.set_color(match.start(), color)
                    p_todo_str.set_color(match.end(), priority_color)

            p_todo_str.append('', neutral_color)

            # color by priority
            p_todo_str.set_color(0, priority_color)

        return p_todo_str

