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

from topydo.lib.Colors import NEUTRAL_COLOR, Colors
from topydo.lib.Config import config
from topydo.lib.PrettyPrinterFilter import PrettyPrinterFilter


class PrettyPrinterColorFilter(PrettyPrinterFilter):
    """
    Adds colors to the todo string by inserting ANSI codes.

    Should be passed as a filter in the filter list of pretty_print()
    """

    def filter(self, p_todo_str, p_todo):
        """ Applies the colors. """
        if config().colors():
            colorscheme = Colors()
            priority_colors = colorscheme.get_priority_colors()
            project_color = colorscheme.get_project_color()
            context_color = colorscheme.get_context_color()
            metadata_color = colorscheme.get_metadata_color()
            link_color = colorscheme.get_link_color()

            priority_color = NEUTRAL_COLOR
            try:
                priority_color = priority_colors[p_todo.priority()]
            except KeyError:
                pass

            # color projects / contexts
            p_todo_str = re.sub(
                r'\B(\+|@)(\S*\w)',
                lambda m: (
                    context_color if m.group(0)[0] == "@"
                    else project_color) + m.group(0) + priority_color,
                p_todo_str)

            # tags
            p_todo_str = re.sub(r'\b\S+:[^/\s]\S*\b',
                                metadata_color + r'\g<0>' + priority_color,
                                p_todo_str)

            # add link_color to any valid URL specified outside of the tag.
            p_todo_str = re.sub(r'(^|\s)(\w+:){1}(//\S+)',
                                r'\1' + link_color + r'\2\3' + priority_color,
                                p_todo_str)

            p_todo_str += NEUTRAL_COLOR

            # color by priority
            p_todo_str = priority_color + p_todo_str

        return p_todo_str

