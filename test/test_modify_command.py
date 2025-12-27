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

from topydo.commands.ModifyCommand import ModifyCommand
from topydo.lib.TodoList import TodoList

from .command_testcase import CommandTest


class ModifyCommandTest(CommandTest):
    def setUp(self):
        super().setUp()
        self.todolist = TodoList([])
        self.todolist.add("Foo")
        self.todolist.add("Asdf id:asdfid")
        self.today = date.today().isoformat()

    def test_modify1(self):
        command = ModifyCommand(["Bar", 1], self.todolist, self.out,
                                self.error)
        command.execute()

        self.assertEqual(self.output, "|  1| Foo Bar\n")
        self.assertEqual(self.errors, "")

    def test_modify2(self):
        command = ModifyCommand(["Bar", 9], self.todolist, self.out,
                                self.error)
        command.execute()

        self.assertEqual(self.output, "")
        self.assertEqual(self.errors, "Invalid todo number: 9\n")

    def test_modify3(self):
        command = ModifyCommand([1, 2], self.todolist, self.out, self.error)
        command.execute()

        self.assertEqual(self.output, "")
        self.assertEqual(self.errors, command.usage() + "\n")

    def test_modify4(self):
        command = ModifyCommand(["Bar", 1, 2], self.todolist, self.out,
                                self.error)
        command.execute()

        self.assertEqual(self.output, "|  1| Foo Bar\n|  2| Asdf id:asdfid Bar\n")
        self.assertEqual(self.errors, "")

    def test_modify5(self):
        command = ModifyCommand([], self.todolist, self.out, self.error)
        command.execute()

        self.assertEqual(self.output, "")
        self.assertEqual(self.errors, command.usage() + "\n")

    def test_modify6(self):
        command = ModifyCommand(["Bar"], self.todolist, self.out, self.error)
        command.execute()

        self.assertEqual(self.output, "")
        self.assertEqual(self.errors, command.usage() + "\n")

    def test_modify7(self):
        command = ModifyCommand(["due:today", 1, 2], self.todolist,
                                self.out, self.error)
        command.execute()

        self.assertEqual(self.output,
                         "|  1| Foo due:%s\n|  2| Asdf id:asdfid due:%s\n" %
                         (self.today, self.today))
        self.assertEqual(self.errors, "")

    def test_modify_name(self):
        name = ModifyCommand.name()

        self.assertEqual(name, 'modify')

    def test_help(self):
        command = ModifyCommand(["help"], self.todolist, self.out, self.error)
        command.execute()

        self.assertEqual(self.output, "")
        self.assertEqual(self.errors,
                         command.usage() + "\n\n" + command.help() + "\n")

if __name__ == '__main__':
    unittest.main()
