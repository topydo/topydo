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

import CommandTest
import DeleteCommand
import TodoList

class DeleteCommandTest(CommandTest.CommandTest):
    def setUp(self):
        todos = [
            "Foo id:1",
            "Bar p:1",
        ]

        self.todolist = TodoList.TodoList(todos)

    def test_del1(self):
        command = DeleteCommand.DeleteCommand(["1"], self.todolist, self.out, self.error, lambda p: "n")
        command.execute()

        self.assertTrue(self.todolist.is_dirty())
        self.assertEquals(self.todolist.todo(1).source(), "Bar")
        self.assertEquals(self.output, "  2 Bar p:1\nRemoved: Foo id:1\n")
        self.assertEquals(self.errors, "")

    def test_del2(self):
        command = DeleteCommand.DeleteCommand(["1"], self.todolist, self.out, self.error, lambda p: "y")
        command.execute()

        self.assertTrue(self.todolist.is_dirty())
        self.assertEquals(self.todolist.count(), 0)
        self.assertEquals(self.output, "  2 Bar p:1\nRemoved: Bar\nRemoved: Foo\n")
        self.assertEquals(self.errors, "")

    def test_del3(self):
        command = DeleteCommand.DeleteCommand(["-f", "1"], self.todolist, self.out, self.error, lambda p: "y")
        command.execute()

        self.assertTrue(self.todolist.is_dirty())
        self.assertEquals(self.todolist.count(), 1) # force won't delete subtasks
        self.assertEquals(self.output, "  2 Bar p:1\nRemoved: Foo id:1\n")
        self.assertEquals(self.errors, "")

    def test_del4(self):
        command = DeleteCommand.DeleteCommand(["2"], self.todolist, self.out, self.error)
        command.execute()

        self.assertTrue(self.todolist.is_dirty())
        self.assertEquals(self.todolist.todo(1).source(), "Foo")
        self.assertEquals(self.output, "Removed: Bar p:1\n")
        self.assertEquals(self.errors, "")

    def test_del5(self):
        command = DeleteCommand.DeleteCommand(["99"], self.todolist, self.out, self.error)
        command.execute()

        self.assertFalse(self.todolist.is_dirty())
        self.assertEquals(self.output, "")
        self.assertEquals(self.errors, "Invalid todo number given.\n")

    def test_del6(self):
        command = DeleteCommand.DeleteCommand(["A"], self.todolist, self.out, self.error)
        command.execute()

        self.assertFalse(self.todolist.is_dirty())
        self.assertEquals(self.output, "")
        self.assertEquals(self.errors, command.usage() + "\n")

    def test_empty(self):
        command = DeleteCommand.DeleteCommand([], self.todolist, self.out, self.error)
        command.execute()

        self.assertFalse(self.todolist.is_dirty())
        self.assertFalse(self.output)
        self.assertEquals(self.errors, command.usage() + "\n")

    def test_help(self):
        command = DeleteCommand.DeleteCommand(["help"], self.todolist, self.out, self.error)
        command.execute()

        self.assertEquals(self.output, "")
        self.assertEquals(self.errors, command.usage() + "\n\n" + command.help() + "\n")
