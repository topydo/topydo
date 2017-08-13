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

from topydo.commands.ListContextCommand import ListContextCommand

from .command_testcase import CommandTest
from .facilities import load_file_to_todolist


class ListContextCommandTest(CommandTest):
    def test_contexts1(self):
        todolist = load_file_to_todolist("test/data/TodoListTest.txt")
        command = ListContextCommand([""], todolist, self.out, self.error)
        command.execute()

        self.assertEqual(self.output, "Context1\nContext2\n")
        self.assertFalse(self.errors)

    def test_contexts2(self):
        todolist = load_file_to_todolist("test/data/TodoListTest.txt")
        command = ListContextCommand(["aaa"], todolist, self.out, self.error)
        command.execute()

        self.assertEqual(self.output, "Context1\nContext2\n")
        self.assertFalse(self.errors)

    def test_listcontext_name(self):
        name = ListContextCommand.name()

        self.assertEqual(name, 'listcontext')

    def test_help(self):
        command = ListContextCommand(["help"], None, self.out, self.error)
        command.execute()

        self.assertEqual(self.output, "")
        self.assertEqual(self.errors,
                         command.usage() + "\n\n" + command.help() + "\n")

if __name__ == '__main__':
    unittest.main()
