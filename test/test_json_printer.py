# Topydo - A todo.txt client written in Python.
# Copyright (C) 2015 Bram Schoenmakers <bram@topydo.org>
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

from topydo.lib.printers.Json import JsonPrinter
from topydo.lib.Todo import Todo

from .topydo_testcase import TopydoTest


class JsonPrinterTest(TopydoTest):
    """
    Tests the functionality of printing a single todo item. Printing a list is
    already covered by the ListCommand tests.
    """

    def test_json(self):
        """ Print a single todo item. """
        printer = JsonPrinter()
        todo = Todo('2015-06-06 Foo due:2015-05-32')

        result = printer.print_todo(todo)

        self.assertEqual(result, '{"completed": false, "completion_date": null, "contexts": [], "creation_date": "2015-06-06", "priority": null, "projects": [], "source": "2015-06-06 Foo due:2015-05-32", "tags": [["due", "2015-05-32"]], "text": "Foo"}')

if __name__ == '__main__':
    unittest.main()
