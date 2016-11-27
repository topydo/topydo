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

""" A view is a list of todos, sorted, grouped and filtered. """


class View(object):
    """
    A view is instantiated by a todo list, usually obtained from a todo.txt
    file. Also a sorter and a list of filters should be given that is applied
    to the list.
    """

    def __init__(self, p_sorter, p_filters, p_todolist):
        self.todolist = p_todolist
        self._sorter = p_sorter
        self._filters = p_filters

    def _apply_filters(self, p_todos):
        """ Applies the filters to the list of todo items. """
        result = p_todos

        for _filter in self._filters:
            result = _filter.filter(result)

        return result

    @property
    def todos(self):
        """ Returns a sorted and filtered list of todos in this view. """
        result = self._sorter.sort(self.todolist.todos())
        return self._apply_filters(result)

    @property
    def groups(self):
        result = self._apply_filters(self.todolist.todos())
        return self._sorter.group(result)
