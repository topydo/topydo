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
from topydo.lib.DepriCommand import DepriCommand
from topydo.lib.TodoList import TodoList

class DepriCommandTest(CommandTest.CommandTest):
    def setUp(self):
        super(DepriCommandTest, self).setUp()
        todos = [
            "(A) Foo",
            "Bar",
            "(B) Baz",
        ]

        self.todolist = TodoList(todos)

    def test_depri1(self):
        command = DepriCommand(["1"], self.todolist, self.out, self.error)
        command.execute()

        self.assertTrue(self.todolist.is_dirty())
        self.assertEquals(self.todolist.todo(1).priority(), None)
        self.assertEquals(self.output, "Priority removed.\n|  1| Foo\n")
        self.assertEquals(self.errors, "")

    def test_depri2(self):
        command = DepriCommand(["2"], self.todolist, self.out, self.error)
        command.execute()

        self.assertFalse(self.todolist.is_dirty())
        self.assertEquals(self.todolist.todo(2).priority(), None)
        self.assertEquals(self.output, "")
        self.assertEquals(self.errors, "")

    def test_depri3(self):
        command = DepriCommand(["Foo"], self.todolist, self.out, self.error)
        command.execute()

        self.assertTrue(self.todolist.is_dirty())
        self.assertEquals(self.todolist.todo(1).priority(), None)
        self.assertEquals(self.output, "Priority removed.\n|  1| Foo\n")
        self.assertEquals(self.errors, "")

    def test_depri4(self):
        command = DepriCommand(["1","Baz"], self.todolist, self.out, self.error)
        command.execute()

        self.assertTrue(self.todolist.is_dirty())
        self.assertEquals(self.todolist.todo(1).priority(), None)
        self.assertEquals(self.todolist.todo(3).priority(), None)
        self.assertEquals(self.output, "Priority removed.\n|  1| Foo\nPriority removed.\n|  3| Baz\n")
        self.assertEquals(self.errors, "")


    def test_invalid1(self):
        command = DepriCommand(["99"], self.todolist, self.out, self.error)
        command.execute()

        self.assertFalse(self.todolist.is_dirty())
        self.assertFalse(self.output)
        self.assertEquals(self.errors, "Invalid todo number given.\n")

    def test_invalid2(self):
        command = DepriCommand(["99", "1"], self.todolist, self.out, self.error)
        command.execute()

        self.assertFalse(self.todolist.is_dirty())
        self.assertFalse(self.output)
        self.assertEquals(self.errors, "Invalid todo number given: 99.\n")

    def test_invalid3(self):
        command = DepriCommand(["99", "FooBar"], self.todolist, self.out, self.error)
        command.execute()

        self.assertFalse(self.todolist.is_dirty())
        self.assertFalse(self.output)
        self.assertEquals(self.errors, "Invalid todo number given: 99.\nInvalid todo number given: FooBar.\n")

    def test_empty(self):
        command = DepriCommand([], self.todolist, self.out, self.error)
        command.execute()

        self.assertFalse(self.todolist.is_dirty())
        self.assertFalse(self.output)
        self.assertEquals(self.errors, command.usage() + "\n")

    def test_help(self):
        command = DepriCommand(["help"], self.todolist, self.out, self.error)
        command.execute()

        self.assertEquals(self.output, "")
        self.assertEquals(self.errors, command.usage() + "\n\n" + command.help() + "\n")

if __name__ == '__main__':
    unittest.main()
