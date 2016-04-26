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

import unittest
from freezegun import freeze_time

from test.command_testcase import CommandTest
from topydo.commands.AppendCommand import AppendCommand
from topydo.lib.TodoList import TodoList


class AppendCommandTest(CommandTest):
    def setUp(self):
        super().setUp()
        self.todolist = TodoList([])
        self.todolist.add("Foo")

    def test_append1(self):
        command = AppendCommand([1, "Bar"], self.todolist, self.out,
                                self.error)
        command.execute()

        self.assertEqual(self.output, "|  1| Foo Bar\n")
        self.assertEqual(self.errors, "")

    def test_append2(self):
        command = AppendCommand([2, "Bar"], self.todolist, self.out,
                                self.error)
        command.execute()

        self.assertEqual(self.output, "")
        self.assertEqual(self.errors, "Invalid todo number given.\n")

    def test_append3(self):
        command = AppendCommand([1, ""], self.todolist, self.out, self.error)
        command.execute()

        self.assertEqual(self.output, "")
        self.assertEqual(self.output, "")

    def test_append4(self):
        command = AppendCommand([1], self.todolist, self.out, self.error)
        command.execute()

        self.assertEqual(self.output, "")
        self.assertEqual(self.errors, command.usage() + "\n")

    def test_append5(self):
        command = AppendCommand([1, "Bar", "Baz"], self.todolist, self.out,
                                self.error)
        command.execute()

        self.assertEqual(self.output, "|  1| Foo Bar Baz\n")
        self.assertEqual(self.errors, "")

    def test_append6(self):
        command = AppendCommand([], self.todolist, self.out, self.error)
        command.execute()

        self.assertEqual(self.output, "")
        self.assertEqual(self.errors, command.usage() + "\n")

    def test_append7(self):
        command = AppendCommand(["Bar"], self.todolist, self.out, self.error)
        command.execute()

        self.assertEqual(self.output, "")
        self.assertEqual(self.errors, command.usage() + "\n")

    @freeze_time('2016, 4, 24')
    def test_append8(self):
        """Due dates given by append are processed."""
        command = AppendCommand([1, "due:tomorrow"], self.todolist, self.out,
                                self.error)
        command.execute()

        self.assertEqual(self.output, "|  1| Foo due:2016-04-25\n")
        self.assertEqual(self.errors, "")

    def test_append9(self):
        """Use append to add a dependency."""
        self.todolist.add("Bar")
        command = AppendCommand([1, "after:2"], self.todolist, self.out,
                                self.error)
        command.execute()

        self.assertEqual(self.output, "|  1| Foo id:1\n")
        self.assertEqual(self.errors, "")


    def test_help(self):
        command = AppendCommand(["help"], self.todolist, self.out, self.error)
        command.execute()

        self.assertEqual(self.output, "")
        self.assertEqual(self.errors,
                         command.usage() + "\n\n" + command.help() + "\n")

if __name__ == '__main__':
    unittest.main()
