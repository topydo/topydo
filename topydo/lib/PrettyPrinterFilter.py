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

""" Provides a base class for pretty printer filters. """


class PrettyPrinterFilter(object):
    """
    Base class for a pretty printer filter.

    Subclasses must re-implement the filter method.
    """

    def filter(self, p_todo_str, _):
        """
        Applies a filter to p_todo_str and returns a modified version of it.
        """
        raise NotImplementedError
