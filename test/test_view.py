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

import unittest

from topydo.lib import Filter
from topydo.lib.Sorter import Sorter
from topydo.lib.TodoFile import TodoFile
from topydo.lib.TodoList import TodoList

from .facilities import load_file, print_view, todolist_to_string
from .topydo_testcase import TopydoTest


class ViewTest(TopydoTest):
    def test_view(self):
        """ Check filters and printer for views. """
        todofile = TodoFile('test/data/FilterTest1.txt')
        ref = load_file('test/data/ViewTest1-result.txt')

        todolist = TodoList(todofile.read())
        sorter = Sorter('text')
        todofilter = Filter.GrepFilter('+Project')
        view = todolist.view(sorter, [todofilter])

        self.assertEqual(print_view(view), todolist_to_string(ref))

if __name__ == '__main__':
    unittest.main()
