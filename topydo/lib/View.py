# Topydo - A todo.txt client written in Python.
# Copyright (C) 2014 Bram Schoenmakers <me@bramschoenmakers.nl>
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

""" A view is a list of todos, sorted and filtered. """

from topydo.lib.PrettyPrinter import pretty_print_list, pp_color

class View(object):
    """
    A view is instantiated by a todo list, usually obtained from a todo.txt
    file. Also a sorter and a list of filters should be given that is applied
    to the list.
    """
    def __init__(self, p_sorter, p_filters, p_todolist):
        self._todolist = p_todolist
        self._viewdata = []
        self._sorter = p_sorter
        self._filters = p_filters

        self.update()

    def update(self):
        """
        Updates the view data. Should be called when the backing todo list
        has changed.
        """
        self._viewdata = self._sorter.sort(self._todolist.todos())

        for _filter in self._filters:
            self._viewdata = _filter.filter(self._viewdata)

    def pretty_print(self, p_pp_filters=None):
        """ Pretty prints the view. """
        p_pp_filters = p_pp_filters or []
        pp_filters = [self._todolist.pp_number(), pp_color] + p_pp_filters
        return '\n'.join(pretty_print_list(self._viewdata, pp_filters))

    def __str__(self):
        return '\n'.join(pretty_print_list(self._viewdata))
