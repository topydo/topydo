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

""" This module provides TopydoString to embed colors in a string. """

import collections

class TopydoString(collections.UserString):
    """
    Represents a string that also contains color information. A combination of
    (position, color) is maintained, where the position is the start position
    where a certain color should start.
    """

    def __init__(self, p_content, p_metadata=None):
        if isinstance(p_content, TopydoString):
            # don't nest topydostrings
            self.colors = p_content.colors
            self.metadata = p_content.metadata
            super().__init__(p_content.data)
        else:
            self.colors = {}
            super().__init__(p_content)

            # allows clients to pass arbitrary data with this string (e.g. a Todo
            # object)
            self.metadata = p_metadata

    def append(self, p_string, p_color):
        """
        Append a string with the given color (normal Color or an
        AbstractColor).
        """
        self.colors[len(self.data)] = p_color
        self.data += p_string

    def set_color(self, p_pos, p_color):
        """ Start using a color at the given position. """
        self.colors[p_pos] = p_color

