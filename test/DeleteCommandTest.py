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

import CommandTest
from topydo.lib.Config import config
from topydo.lib.DeleteCommand import DeleteCommand
from topydo.lib.TodoList import TodoList
from topydo.lib.TodoListBase import InvalidTodoException

def _yes_prompt(self):
    return "y"

def _no_prompt(self):
    return "n"

class DeleteCommandTest(CommandTest.CommandTest):
    def setUp(self):
        super(DeleteCommandTest, self).setUp()
        todos = [
            "Foo id:1",
            "Bar p:1",
        ]

        self.todolist = TodoList(todos)

    def test_del1(self):
        command = DeleteCommand(["1"], self.todolist, self.out, self.error, _no_prompt)
        command.execute()

        self.assertTrue(self.todolist.is_dirty())
        self.assertEquals(self.todolist.todo(1).source(), "Bar")
        self.assertEquals(self.output, "|  2| Bar p:1\nRemoved: Foo id:1\n")
        self.assertEquals(self.errors, "")

    def test_del1_regex(self):
        command = DeleteCommand(["Foo"], self.todolist, self.out, self.error, _no_prompt)
        command.execute()

        self.assertTrue(self.todolist.is_dirty())
        self.assertEquals(self.todolist.todo(1).source(), "Bar")
        self.assertEquals(self.output, "|  2| Bar p:1\nRemoved: Foo id:1\n")
        self.assertEquals(self.errors, "")

    def test_del2(self):
        command = DeleteCommand(["1"], self.todolist, self.out, self.error, _yes_prompt)
        command.execute()

        self.assertTrue(self.todolist.is_dirty())
        self.assertEquals(self.todolist.count(), 0)
        self.assertEquals(self.output, "|  2| Bar p:1\nRemoved: Bar\nRemoved: Foo\n")
        self.assertEquals(self.errors, "")

    def test_del3(self):
        command = DeleteCommand(["-f", "1"], self.todolist, self.out, self.error, _yes_prompt)
        command.execute()

        self.assertTrue(self.todolist.is_dirty())
        self.assertEquals(self.todolist.count(), 1) # force won't delete subtasks
        self.assertEquals(self.output, "|  2| Bar p:1\nRemoved: Foo id:1\n")
        self.assertEquals(self.errors, "")

    def test_del4(self):
        command = DeleteCommand(["--force", "1"], self.todolist, self.out, self.error, _yes_prompt)
        command.execute()

        self.assertTrue(self.todolist.is_dirty())
        self.assertEquals(self.todolist.count(), 1) # force won't delete subtasks
        self.assertEquals(self.output, "|  2| Bar p:1\nRemoved: Foo id:1\n")
        self.assertEquals(self.errors, "")

    def test_del5(self):
        command = DeleteCommand(["2"], self.todolist, self.out, self.error)
        command.execute()

        self.assertTrue(self.todolist.is_dirty())
        self.assertEquals(self.todolist.todo(1).source(), "Foo")
        self.assertEquals(self.output, "Removed: Bar p:1\nThe following todo item(s) became active:\n|  1| Foo\n")
        self.assertEquals(self.errors, "")

    def test_del7(self):
        command = DeleteCommand(["99"], self.todolist, self.out, self.error)
        command.execute()

        self.assertFalse(self.todolist.is_dirty())
        self.assertEquals(self.output, "")
        self.assertEquals(self.errors, "Invalid todo number given.\n")

    def test_del8(self):
        command = DeleteCommand(["A"], self.todolist, self.out, self.error)
        command.execute()

        self.assertFalse(self.todolist.is_dirty())
        self.assertEquals(self.output, "")
        self.assertEquals(self.errors, "Invalid todo number given.\n")

    def test_del9(self):
        """ Test deletion with textual IDs. """
        config("test/data/todolist-uid.conf")

        command = DeleteCommand(["b0n"], self.todolist, self.out, self.error)
        command.execute()

        self.assertEquals(str(self.todolist), "Foo")
        self.assertRaises(InvalidTodoException, self.todolist.todo, 'b0n')

    def test_multi_del1(self):
        """ Test deletion of multiple items. """
        command = DeleteCommand(["1", "2"], self.todolist, self.out, self.error, _no_prompt)
        command.execute()

        self.assertEquals(self.todolist.count(), 0)

    def test_multi_del2(self):
        """ Test deletion of multiple items. """
        command = DeleteCommand(["1", "2"], self.todolist, self.out, self.error, _yes_prompt)
        command.execute()

        self.assertEquals(self.todolist.count(), 0)

    def test_multi_del3(self):
        """  Fail if any of supplied todo numbers is invalid. """
        command = DeleteCommand(["99", "2"], self.todolist, self.out, self.error, _yes_prompt)
        command.execute()

        self.assertFalse(self.todolist.is_dirty())
        self.assertEquals(self.output, "")
        self.assertEquals(self.errors, "Invalid todo number given: 99.\n")

    def test_multi_del4(self):
        """  Check output when all supplied todo numbers are invalid. """
        command = DeleteCommand(["99", "A"], self.todolist, self.out, self.error, _yes_prompt)
        command.execute()

        self.assertFalse(self.todolist.is_dirty())
        self.assertEquals(self.output, "")
        self.assertEquals(self.errors, "Invalid todo number given: 99.\nInvalid todo number given: A.\n")

    def test_empty(self):
        command = DeleteCommand([], self.todolist, self.out, self.error)
        command.execute()

        self.assertFalse(self.todolist.is_dirty())
        self.assertFalse(self.output)
        self.assertEquals(self.errors, command.usage() + "\n")

    def test_help(self):
        command = DeleteCommand(["help"], self.todolist, self.out, self.error)
        command.execute()

        self.assertEquals(self.output, "")
        self.assertEquals(self.errors, command.usage() + "\n\n" + command.help() + "\n")

if __name__ == '__main__':
    unittest.main()
