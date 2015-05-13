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
from topydo.lib.PriorityCommand import PriorityCommand
from topydo.lib.TodoList import TodoList

class PriorityCommandTest(CommandTest.CommandTest):
    def setUp(self):
        super(PriorityCommandTest, self).setUp()
        todos = [
            "(A) Foo",
            "Bar",
        ]

        self.todolist = TodoList(todos)

    def test_set_prio1(self):
        command = PriorityCommand(["1", "B"], self.todolist, self.out, self.error)
        command.execute()

        self.assertTrue(self.todolist.is_dirty())
        self.assertEquals(self.output, "Priority changed from A to B\n|  1| (B) Foo\n")
        self.assertEquals(self.errors, "")

    def test_set_prio2(self):
        command = PriorityCommand(["2", "Z"], self.todolist, self.out, self.error)
        command.execute()

        self.assertTrue(self.todolist.is_dirty())
        self.assertEquals(self.output, "Priority set to Z.\n|  2| (Z) Bar\n")
        self.assertEquals(self.errors, "")

    def test_set_prio3(self):
        command = PriorityCommand(["Foo", "B"], self.todolist, self.out, self.error)
        command.execute()

        self.assertTrue(self.todolist.is_dirty())
        self.assertEquals(self.output, "Priority changed from A to B\n|  1| (B) Foo\n")
        self.assertEquals(self.errors, "")

    def test_set_prio4(self):
        command = PriorityCommand(["1", "A"], self.todolist, self.out, self.error)
        command.execute()

        self.assertFalse(self.todolist.is_dirty())
        self.assertEquals(self.output, "|  1| (A) Foo\n")
        self.assertEquals(self.errors, "")

    def test_set_prio5(self):
        command = PriorityCommand(["Foo", "2", "C"], self.todolist, self.out, self.error)
        command.execute()

        self.assertTrue(self.todolist.is_dirty())
        self.assertEquals(self.output, "Priority changed from A to C\n|  1| (C) Foo\nPriority set to C.\n|  2| (C) Bar\n")
        self.assertEquals(self.errors, "")

    def test_invalid1(self):
        command = PriorityCommand(["99", "A"], self.todolist, self.out, self.error)
        command.execute()

        self.assertFalse(self.todolist.is_dirty())
        self.assertFalse(self.output)
        self.assertEquals(self.errors, "Invalid todo number given.\n")

    def test_invalid2(self):
        command = PriorityCommand(["1", "99", "A"], self.todolist, self.out, self.error)
        command.execute()

        self.assertFalse(self.todolist.is_dirty())
        self.assertFalse(self.output)
        self.assertEquals(self.errors, "Invalid todo number given: 99.\n")

    def test_invalid3(self):
        command = PriorityCommand(["98", "99", "A"], self.todolist, self.out, self.error)
        command.execute()

        self.assertFalse(self.todolist.is_dirty())
        self.assertFalse(self.output)
        self.assertEquals(self.errors, "Invalid todo number given: 98.\nInvalid todo number given: 99.\n")

    def test_invalid4(self):
        command = PriorityCommand(["1", "ZZ"], self.todolist, self.out, self.error)
        command.execute()

        self.assertFalse(self.todolist.is_dirty())
        self.assertFalse(self.output)
        self.assertEquals(self.errors, "Invalid priority given.\n")

    def test_invalid5(self):
        command = PriorityCommand(["A"], self.todolist, self.out, self.error)
        command.execute()

        self.assertFalse(self.todolist.is_dirty())
        self.assertFalse(self.output)
        self.assertEquals(self.errors, command.usage() + "\n")

    def test_invalid6(self):
        command = PriorityCommand(["1"], self.todolist, self.out, self.error)
        command.execute()

        self.assertFalse(self.todolist.is_dirty())
        self.assertFalse(self.output)
        self.assertEquals(self.errors, command.usage() + "\n")

    def test_empty(self):
        command = PriorityCommand([], self.todolist, self.out, self.error)
        command.execute()

        self.assertFalse(self.todolist.is_dirty())
        self.assertFalse(self.output)
        self.assertEquals(self.errors, command.usage() + "\n")

    def test_help(self):
        command = PriorityCommand(["help"], self.todolist, self.out, self.error)
        command.execute()

        self.assertEquals(self.output, "")
        self.assertEquals(self.errors, command.usage() + "\n\n" + command.help() + "\n")

if __name__ == '__main__':
    unittest.main()
