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

from datetime import date, timedelta

import CommandTest
from topydo.lib.PostponeCommand import PostponeCommand
from topydo.lib.TodoList import TodoList

class PostponeCommandTest(CommandTest.CommandTest):
    def setUp(self):
        super(PostponeCommandTest, self).setUp()
        self.today = date.today()
        self.past = date.today() - timedelta(1)
        self.future = date.today() + timedelta(1)
        self.start = date.today() - timedelta(2)
        self.future_start = self.future - timedelta(2)

        todos = [
            "Foo",
            "Bar due:%s" % self.today.isoformat(),
            "Baz due:%s t:%s" % (self.today.isoformat(), self.start.isoformat()),
            "Past due:%s" % self.past.isoformat(),
            "Future due:%s t:%s" % (self.future.isoformat(), self.future_start.isoformat()),
        ]

        self.todolist = TodoList(todos)

    def test_postpone1(self):
        command = PostponeCommand(["1", "1w"], self.todolist, self.out, self.error)
        command.execute()

        due = self.today + timedelta(7)

        self.assertTrue(self.todolist.is_dirty())
        self.assertEquals(self.output, "  1 Foo due:%s\n" % due.isoformat())
        self.assertEquals(self.errors, "")

    def test_postpone2(self):
        command = PostponeCommand(["2", "1w"], self.todolist, self.out, self.error)
        command.execute()

        due = self.today + timedelta(7)

        self.assertTrue(self.todolist.is_dirty())
        self.assertEquals(self.output, "  2 Bar due:%s\n" % due.isoformat())
        self.assertEquals(self.errors, "")

    def test_postpone3(self):
        command = PostponeCommand(["-s", "2", "1w"], self.todolist, self.out, self.error)
        command.execute()

        due = self.today + timedelta(7)

        self.assertTrue(self.todolist.is_dirty())
        self.assertEquals(self.output, "  2 Bar due:%s\n" % due.isoformat())
        self.assertEquals(self.errors, "")

    def test_postpone4(self):
        command = PostponeCommand(["3", "1w"], self.todolist, self.out, self.error)
        command.execute()

        due = self.today + timedelta(7)

        self.assertTrue(self.todolist.is_dirty())
        self.assertEquals(self.output, "  3 Baz due:%s t:%s\n" % (due.isoformat(), self.start.isoformat()))
        self.assertEquals(self.errors, "")

    def test_postpone5(self):
        command = PostponeCommand(["-s", "3", "1w"], self.todolist, self.out, self.error)
        command.execute()

        due = self.today + timedelta(7)
        start = self.start + timedelta(7)

        self.assertTrue(self.todolist.is_dirty())
        self.assertEquals(self.output, "  3 Baz due:%s t:%s\n" % (due.isoformat(), start.isoformat()))
        self.assertEquals(self.errors, "")

    def test_postpone6(self):
        command = PostponeCommand(["4", "1w"], self.todolist, self.out, self.error)
        command.execute()

        due = self.today + timedelta(7)

        self.assertTrue(self.todolist.is_dirty())
        self.assertEquals(self.output, "  4 Past due:%s\n" % due.isoformat())
        self.assertEquals(self.errors, "")

    def test_postpone7(self):
        command = PostponeCommand(["5", "1w"], self.todolist, self.out, self.error)
        command.execute()

        due = self.future + timedelta(7)

        self.assertTrue(self.todolist.is_dirty())
        self.assertEquals(self.output, "  5 Future due:%s t:%s\n" % (due.isoformat(), self.future_start.isoformat()))
        self.assertEquals(self.errors, "")

    def test_postpone8(self):
        command = PostponeCommand(["-s", "5", "1w"], self.todolist, self.out, self.error)
        command.execute()

        due = self.future + timedelta(7)
        start = self.future_start + timedelta(7)

        self.assertTrue(self.todolist.is_dirty())
        self.assertEquals(self.output, "  5 Future due:%s t:%s\n" % (due.isoformat(), start.isoformat()))
        self.assertEquals(self.errors, "")

    def test_postpone9(self):
        command = PostponeCommand(["1", "foo"], self.todolist, self.out, self.error)
        command.execute()

        self.assertFalse(self.todolist.is_dirty())
        self.assertEquals(self.output, "")
        self.assertEquals(self.errors, "Invalid date pattern given.\n")

    def test_postpone10(self):
        command = PostponeCommand(["99", "foo"], self.todolist, self.out, self.error)
        command.execute()

        self.assertFalse(self.todolist.is_dirty())
        self.assertEquals(self.output, "")
        self.assertEquals(self.errors, "Invalid todo number given.\n")

    def test_postpone11(self):
        command = PostponeCommand(["A", "foo"], self.todolist, self.out, self.error)
        command.execute()

        self.assertFalse(self.todolist.is_dirty())
        self.assertEquals(self.output, "")
        self.assertEquals(self.errors, "Invalid todo number given.\n")

    def test_postpone12(self):
        command = PostponeCommand(["1"], self.todolist, self.out, self.error)
        command.execute()

        self.assertFalse(self.todolist.is_dirty())
        self.assertEquals(self.output, "")
        self.assertEquals(self.errors, command.usage() + "\n")

    def test_postpone13(self):
        command = PostponeCommand(["Foo", "1w"], self.todolist, self.out, self.error)
        command.execute()

        due = self.today + timedelta(7)

        self.assertTrue(self.todolist.is_dirty())
        self.assertEquals(self.output, "  1 Foo due:%s\n" % due.isoformat())
        self.assertEquals(self.errors, "")

    def test_help(self):
        command = PostponeCommand(["help"], self.todolist, self.out, self.error)
        command.execute()

        self.assertEquals(self.output, "")
        self.assertEquals(self.errors, command.usage() + "\n\n" + command.help() + "\n")

