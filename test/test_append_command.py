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
from datetime import date

from topydo.commands.AppendCommand import AppendCommand
from topydo.lib.TodoList import TodoList

from .command_testcase import CommandTest


class AppendCommandTest(CommandTest):
    def setUp(self):
        super().setUp()
        self.todolist = TodoList([])
        self.todolist.add("Foo")
        self.today = date.today().isoformat()

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

    def test_append8(self):
        command = AppendCommand([1, "due:today t:today"], self.todolist,
                                self.out, self.error)
        command.execute()

        self.assertEqual(self.output,
                         "|  1| Foo due:%s t:%s\n" % (self.today, self.today))
        self.assertEqual(self.errors, "")

    def test_append9(self):
        self.todolist.add("Qux due:2015-12-21 t:2015-12-21 before:1")
        self.todolist.add("Baz")
        command = AppendCommand([2, "due:today t:today before:3"], self.todolist,
                                self.out, self.error)
        command.execute()

        self.assertEqual(
                self.output,
                "|  2| Qux due:%s t:%s p:1 p:2\n" % (self.today, self.today))
        self.assertEqual(self.errors, "")

    def test_append_name(self):
        name = AppendCommand.name()

        self.assertEqual(name, 'append')

    def test_help(self):
        command = AppendCommand(["help"], self.todolist, self.out, self.error)
        command.execute()

        self.assertEqual(self.output, "")
        self.assertEqual(self.errors,
                         command.usage() + "\n\n" + command.help() + "\n")

if __name__ == '__main__':
    unittest.main()
