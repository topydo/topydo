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

""" This module provides TopydoString to embed colors in a string. """

import collections

class TopydoString(collections.UserString):
    """
    Represents a string that also contains color information. A combination of
    (position, color) is maintained, where the position is the start position
    where a certain color should start.
    """

    def __init__(self, p_content):
        if isinstance(p_content, TopydoString):
            # don't nest topydostrings
            self.colors = p_content.colors
            super().__init__(p_content.data)
        else:
            self.colors = {}
            super().__init__(p_content)

    def append(self, p_string, p_color):
        """ Append a string with the given color. """
        self.colors[len(self.data)] = p_color
        self.data += p_string

    def set_color(self, p_pos, p_color):
        """ Start using a color at the given position. """
        self.colors[p_pos] = p_color

    def with_colors(self, p_transform_fn):
        """
        Returns a string with color information at the right positions.
        p_transform_fn is a function that takes a Color object and returns a
        string representing the color (e.g. "#ff0000").
        """
        result = self.data

        for pos, color in sorted(self.colors.items(), reverse=True):
            result = result[:pos] + p_transform_fn(color) + result[pos:]

        return result
