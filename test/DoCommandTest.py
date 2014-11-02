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
import DoCommand
import TodoList

def _yes_prompt(self):
    return "y"

def _no_prompt(self):
    return "n"

class DoCommandTest(CommandTest.CommandTest):
    def setUp(self):
        todos = [
            "Foo id:1",
            "Bar p:1",
            "Baz p:1",
            "Recurring! rec:1d",
            "x 2014-10-18 Already complete",
            "Inactive t:2030-12-31 id:2",
            "Subtodo of inactive p:2",
        ]

        self.todolist = TodoList.TodoList(todos)
        self.today = date.today()
        self.tomorrow = self.today + timedelta(1)
        self.today = self.today.isoformat()
        self.tomorrow = self.tomorrow.isoformat()

    def test_do1(self):
        command = DoCommand.DoCommand(["3"], self.todolist, self.out, self.error, _no_prompt)
        command.execute()

        self.assertTrue(self.todolist.is_dirty())
        self.assertTrue(self.todolist.todo(3).is_completed())
        self.assertEquals(self.output, "Completed: x %s Baz p:1\n" % self.today)
        self.assertEquals(self.errors, "")

    def test_do_subtasks1(self):
        command = DoCommand.DoCommand(["1"], self.todolist, self.out, self.error, _yes_prompt)
        command.execute()

        result = "  2 Bar p:1\n  3 Baz p:1\nCompleted: x %s Bar p:1\nCompleted: x %s Baz p:1\nCompleted: x %s Foo id:1\n" % (self.today, self.today, self.today)

        for number in [1, 2, 3]:
            self.assertTrue(self.todolist.todo(number).is_completed())

        self.assertTrue(self.todolist.is_dirty())
        self.assertFalse(self.todolist.todo(4).is_completed())
        self.assertEquals(self.output, result)
        self.assertEquals(self.errors, "")

    def test_do_subtasks2(self):
        command = DoCommand.DoCommand(["1"], self.todolist, self.out, self.error, _no_prompt)
        command.execute()

        result = "  2 Bar p:1\n  3 Baz p:1\nCompleted: x %s Foo id:1\n" % self.today

        self.assertTrue(self.todolist.is_dirty())
        self.assertTrue(self.todolist.todo(1).is_completed())
        self.assertFalse(self.todolist.todo(2).is_completed())
        self.assertFalse(self.todolist.todo(3).is_completed())
        self.assertEquals(self.output, result)
        self.assertEquals(self.errors, "")

    def test_do_subtasks_force1(self):
        prompt_shown = False

        def prompt(p_prompt):
            prompt_shown = True

        command = DoCommand.DoCommand(["-f", "1"], self.todolist, self.out, self.error, prompt)
        command.execute()

        self.assertFalse(prompt_shown)
        self.assertEquals(self.errors, "")
        self.assertFalse(self.todolist.todo(2).is_completed())

    def test_do_subtasks_force2(self):
        prompt_shown = False

        def prompt(p_prompt):
            prompt_shown = True

        command = DoCommand.DoCommand(["--force", "1"], self.todolist, self.out, self.error, prompt)
        command.execute()

        self.assertFalse(prompt_shown)
        self.assertEquals(self.errors, "")
        self.assertFalse(self.todolist.todo(2).is_completed())

    def test_recurrence(self):
        command = DoCommand.DoCommand(["4"], self.todolist, self.out, self.error)

        self.assertFalse(self.todolist.todo(4).has_tag('due'))

        command.execute()

        todo = self.todolist.todo(8)
        result = "  8 %s Recurring! rec:1d due:%s\nCompleted: x %s Recurring! rec:1d\n" % (self.today, self.tomorrow, self.today)

        self.assertTrue(self.todolist.is_dirty())
        self.assertEquals(self.output, result)
        self.assertEquals(self.errors, "")
        self.assertEquals(self.todolist.count(), 8)
        self.assertTrue(self.todolist.todo(4).is_completed())
        self.assertFalse(todo.is_completed())
        self.assertTrue(todo.has_tag('due'))

    def test_invalid1(self):
        command = DoCommand.DoCommand(["99"], self.todolist, self.out, self.error)
        command.execute()

        self.assertFalse(self.todolist.is_dirty())
        self.assertFalse(self.output)
        self.assertEquals(self.errors, "Invalid todo number given.\n")

    def test_invalid2(self):
        command = DoCommand.DoCommand(["AAA"], self.todolist, self.out, self.error)
        command.execute()

        self.assertFalse(self.todolist.is_dirty())
        self.assertFalse(self.output)
        self.assertEquals(self.errors, command.usage() + "\n")

    def test_activated_todos1(self):
        command = DoCommand.DoCommand(["2"], self.todolist, self.out, self.error)
        command.execute()

        first_output = "Completed: x %s Bar p:1\n" % self.today

        self.assertEquals(self.output, first_output)
        self.assertEquals(self.errors, "")

        command = DoCommand.DoCommand(["3"], self.todolist, self.out, self.error)
        command.execute()

        self.assertEquals(self.output, first_output + "Completed: x %s Baz p:1\nThe following todo item(s) became active:\nFoo id:1\n" % self.today)
        self.assertEquals(self.errors, "")

    def test_activated_todos2(self):
        command = DoCommand.DoCommand(["7"], self.todolist, self.out, self.error)
        command.execute()

        self.assertEquals(self.output, "Completed: x %s Subtodo of inactive p:2\n" % self.today)
        self.assertEquals(self.errors, "")

    def test_already_complete(self):
        command = DoCommand.DoCommand(["5"], self.todolist, self.out, self.error)
        command.execute()

        self.assertFalse(self.todolist.is_dirty())
        self.assertEquals(self.todolist.todo(5).completion_date(), date(2014, 10, 18))
        self.assertFalse(self.output)
        self.assertEquals(self.errors, "Todo has already been completed.\n")

    def test_do_regex1(self):
        command = DoCommand.DoCommand(["baz"], self.todolist, self.out, self.error)
        command.execute()

        self.assertTrue(self.todolist.is_dirty())
        self.assertTrue(self.todolist.todo(3).is_completed())
        self.assertEquals(self.output, "Completed: x %s Baz p:1\n" % self.today)
        self.assertEquals(self.errors, "")

    def test_empty(self):
        command = DoCommand.DoCommand([], self.todolist, self.out, self.error)
        command.execute()

        self.assertFalse(self.todolist.is_dirty())
        self.assertFalse(self.output)
        self.assertEquals(self.errors, command.usage() + "\n")

    def test_help(self):
        command = DoCommand.DoCommand(["help"], self.todolist, self.out, self.error)
        command.execute()

        self.assertEquals(self.output, "")
        self.assertEquals(self.errors, command.usage() + "\n\n" + command.help() + "\n")
