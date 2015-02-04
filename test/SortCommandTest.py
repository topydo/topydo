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

import unittest

import CommandTest
from topydo.lib.Config import config
from topydo.lib.SortCommand import SortCommand
import TestFacilities

class SortCommandTest(CommandTest.CommandTest):
    def setUp(self):
        super(SortCommandTest, self).setUp()
        self.todolist = TestFacilities.load_file_to_todolist("test/data/SorterTest1.txt")

    def test_sort1(self):
        """ Alphabetically sorted """
        command = SortCommand(["text"], self.todolist, self.out, self.error)
        command.execute()

        self.assertEquals(str(self.todolist), "First\n(A) Foo\n2014-06-14 Last")

    def test_sort2(self):
        command = SortCommand([], self.todolist, self.out, self.error)
        command.execute()

        self.assertEquals(str(self.todolist), "(A) Foo\n2014-06-14 Last\nFirst")

    def test_sort3(self):
        """ Check that order does not influence the UID of a todo. """
        config("test/data/todolist-uid.conf")

        todo1 = self.todolist.todo('tpi')
        command = SortCommand(["text"], self.todolist, self.out, self.error)
        command.execute()
        todo2 = self.todolist.todo('tpi')

        self.assertEquals(todo1.source(), todo2.source())

    def test_help(self):
        command = SortCommand(["help"], self.todolist, self.out, self.error)
        command.execute()

        self.assertEquals(self.output, "")
        self.assertEquals(self.errors, command.usage() + "\n\n" + command.help() + "\n")

if __name__ == '__main__':
    unittest.main()
