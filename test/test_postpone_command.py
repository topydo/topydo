# Topydo - A todo.txt client written in Python.
# Copyright (C) 2015 - 2015 Bram Schoenmakers <bram@topydo.org>
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
from datetime import date, timedelta

from topydo.commands.PostponeCommand import PostponeCommand
from topydo.lib.TodoList import TodoList

from .command_testcase import CommandTest


class PostponeCommandTest(CommandTest):
    def setUp(self):
        super().setUp()
        self.today = date.today()
        self.past = date.today() - timedelta(1)
        self.future = date.today() + timedelta(1)
        self.start = date.today() - timedelta(2)
        self.future_start = self.future - timedelta(2)

        todos = [
            "Foo",
            "Bar due:{}".format(self.today.isoformat()),
            "Baz due:{} t:{}".format(self.today.isoformat(), self.start.isoformat()),
            "Past due:{}".format(self.past.isoformat()),
            "Future due:{} t:{}".format(self.future.isoformat(), self.future_start.isoformat()),
            "FutureStart t:{}".format(self.future.isoformat()),
            "InvalidDueDate due:2017-06-31",
            "InvalidStartDate t:2017-06-31",
        ]

        self.todolist = TodoList(todos)

    def test_postpone01(self):
        command = PostponeCommand(["1", "1w"], self.todolist, self.out,
                                  self.error)
        command.execute()

        due = self.today + timedelta(7)

        self.assertTrue(self.todolist.dirty)
        self.assertEqual(self.output,
                         "|  1| Foo due:{}\n".format(due.isoformat()))
        self.assertEqual(self.errors, "")

    def test_postpone02(self):
        command = PostponeCommand(["2", "1w"], self.todolist, self.out,
                                  self.error)
        command.execute()

        due = self.today + timedelta(7)

        self.assertTrue(self.todolist.dirty)
        self.assertEqual(self.output,
                         "|  2| Bar due:{}\n".format(due.isoformat()))
        self.assertEqual(self.errors, "")

    def test_postpone03(self):
        command = PostponeCommand(["-s", "2", "1w"], self.todolist, self.out,
                                  self.error)
        command.execute()

        due = self.today + timedelta(7)

        self.assertTrue(self.todolist.dirty)
        self.assertEqual(self.output,
                         "|  2| Bar due:{}\n".format(due.isoformat()))
        self.assertEqual(self.errors, "Warning: todo item has no (valid) start date, therefore it was not adjusted.\n")

    def test_postpone04(self):
        command = PostponeCommand(["3", "1w"], self.todolist, self.out,
                                  self.error)
        command.execute()

        due = self.today + timedelta(7)

        self.assertTrue(self.todolist.dirty)
        self.assertEqual(self.output, "|  3| Baz due:{} t:{}\n".format(due.isoformat(), self.start.isoformat()))
        self.assertEqual(self.errors, "")

    def test_postpone05(self):
        command = PostponeCommand(["-s", "3", "1w"], self.todolist, self.out,
                                  self.error)
        command.execute()

        due = self.today + timedelta(7)
        start = self.start + timedelta(7)

        self.assertTrue(self.todolist.dirty)
        # pylint: disable=E1103
        self.assertEqual(self.output, "|  3| Baz due:{} t:{}\n".format(due.isoformat(), start.isoformat()))
        self.assertEqual(self.errors, "")

    def test_postpone06(self):
        command = PostponeCommand(["4", "1w"], self.todolist, self.out,
                                  self.error)
        command.execute()

        due = self.today + timedelta(7)

        self.assertTrue(self.todolist.dirty)
        self.assertEqual(self.output,
                         "|  4| Past due:{}\n".format(due.isoformat()))
        self.assertEqual(self.errors, "")

    def test_postpone07(self):
        command = PostponeCommand(["5", "1w"], self.todolist, self.out,
                                  self.error)
        command.execute()

        due = self.future + timedelta(7)

        self.assertTrue(self.todolist.dirty)
        # pylint: disable=E1103
        self.assertEqual(self.output, "|  5| Future due:{} t:{}\n".format(due.isoformat(), self.future_start.isoformat()))
        self.assertEqual(self.errors, "")

    def test_postpone08(self):
        command = PostponeCommand(["-s", "5", "1w"], self.todolist, self.out,
                                  self.error)
        command.execute()

        due = self.future + timedelta(7)
        start = self.future_start + timedelta(7)

        self.assertTrue(self.todolist.dirty)
        # pylint: disable=E1103
        self.assertEqual(self.output, "|  5| Future due:{} t:{}\n".format(due.isoformat(), start.isoformat()))
        self.assertEqual(self.errors, "")

    def test_postpone09(self):
        command = PostponeCommand(["1", "foo"], self.todolist, self.out,
                                  self.error)
        command.execute()

        self.assertFalse(self.todolist.dirty)
        self.assertEqual(self.output, "")
        self.assertEqual(self.errors, "Invalid date pattern given.\n")

    def test_postpone10(self):
        command = PostponeCommand(["99", "foo"], self.todolist, self.out,
                                  self.error)
        command.execute()

        self.assertFalse(self.todolist.dirty)
        self.assertEqual(self.output, "")
        self.assertEqual(self.errors, "Invalid todo number given.\n")

    def test_postpone11(self):
        command = PostponeCommand(["A", "foo"], self.todolist, self.out,
                                  self.error)
        command.execute()

        self.assertFalse(self.todolist.dirty)
        self.assertEqual(self.output, "")
        self.assertEqual(self.errors, "Invalid todo number given.\n")

    def test_postpone12(self):
        command = PostponeCommand(["1"], self.todolist, self.out, self.error)
        command.execute()

        self.assertFalse(self.todolist.dirty)
        self.assertEqual(self.output, "")
        self.assertEqual(self.errors, command.usage() + "\n")

    def test_postpone13(self):
        command = PostponeCommand(["Foo", "1w"], self.todolist, self.out,
                                  self.error)
        command.execute()

        due = self.today + timedelta(7)

        self.assertTrue(self.todolist.dirty)
        self.assertEqual(self.output,
                         "|  1| Foo due:{}\n".format(due.isoformat()))
        self.assertEqual(self.errors, "")

    def test_postpone14(self):
        command = PostponeCommand(["1", "2", "1w"], self.todolist, self.out,
                                  self.error)
        command.execute()

        due = self.today + timedelta(7)

        self.assertTrue(self.todolist.dirty)
        self.assertEqual(self.output, "|  1| Foo due:{}\n|  2| Bar due:{}\n".format(due.isoformat(), due.isoformat()))
        self.assertEqual(self.errors, "")

    def test_postpone15(self):
        command = PostponeCommand(["Foo", "2", "1w"], self.todolist, self.out,
                                  self.error)
        command.execute()

        due = self.today + timedelta(7)

        self.assertTrue(self.todolist.dirty)
        self.assertEqual(self.output, "|  1| Foo due:{}\n|  2| Bar due:{}\n".format(due.isoformat(), due.isoformat()))
        self.assertEqual(self.errors, "")

    def test_postpone16(self):
        command = PostponeCommand(["-s", "2", "3", "1w"], self.todolist,
                                  self.out, self.error)
        command.execute()

        due = self.today + timedelta(7)
        start = self.start + timedelta(7)

        self.assertTrue(self.todolist.dirty)
        # pylint: disable=E1103
        self.assertEqual(self.output, "|  2| Bar due:{}\n|  3| Baz due:{} t:{}\n".format(due.isoformat(), due.isoformat(), start.isoformat()))
        self.assertEqual(self.errors, "Warning: todo item has no (valid) start date, therefore it was not adjusted.\n")

    def test_postpone17(self):
        command = PostponeCommand(["1", "2", "3"], self.todolist, self.out,
                                  self.error)
        command.execute()

        self.assertFalse(self.todolist.dirty)
        self.assertEqual(self.output, "")
        self.assertEqual(self.errors, "Invalid date pattern given.\n")

    def test_postpone18(self):
        command = PostponeCommand(["1", "99", "123", "1w"], self.todolist,
                                  self.out, self.error)
        command.execute()

        self.assertFalse(self.todolist.dirty)
        self.assertEqual(self.output, "")
        self.assertEqual(self.errors, "Invalid todo number given: 99.\nInvalid todo number given: 123.\n")

    def test_postpone19(self):
        command = PostponeCommand(["Zoo", "99", "123", "1w"], self.todolist,
                                  self.out, self.error)
        command.execute()

        self.assertFalse(self.todolist.dirty)
        self.assertEqual(self.output, "")
        self.assertEqual(self.errors, "Invalid todo number given: Zoo.\nInvalid todo number given: 99.\nInvalid todo number given: 123.\n")

    def test_postpone20(self):
        """ Throw an error with invalid argument containing special characters. """
        command = PostponeCommand([u"Fo\u00d3B\u0105r", "Bar", "1d"],
                                  self.todolist, self.out, self.error, None)
        command.execute()

        self.assertFalse(self.todolist.dirty)
        self.assertEqual(self.output, "")
        self.assertEqual(self.errors,
                         u"Invalid todo number given: Fo\u00d3B\u0105r.\n")

    def test_postpone21(self):
        """
        Show an error when a todo item has an invalid due date.
        """
        command = PostponeCommand(["7", "1d"], self.todolist, self.out, self.error)
        command.execute()

        self.assertFalse(self.todolist.dirty)
        self.assertEqual(self.output, "")
        self.assertEqual(self.errors, "Postponing todo item failed: invalid due date.\n")

    def test_postpone22(self):
        """
        Todo item has an invalid start date.
        """
        command = PostponeCommand(["8", "1d"], self.todolist, self.out, self.error)
        command.execute()

        self.assertTrue(self.todolist.dirty)
        self.assertEqual(self.output, "|  8| InvalidStartDate t:2017-06-31 due:{}\n".format(self.future.isoformat()))
        self.assertEqual(self.errors, "")

    def test_postpone23(self):
        """
        Todo item has an invalid start date.
        """
        command = PostponeCommand(["-s", "8", "1d"], self.todolist, self.out, self.error)
        command.execute()

        self.assertTrue(self.todolist.dirty)
        self.assertEqual(self.output, "|  8| InvalidStartDate t:2017-06-31 due:{}\n".format(self.future.isoformat()))
        self.assertEqual(self.errors, "Warning: todo item has no (valid) start date, therefore it was not adjusted.\n")

    def test_expr_postpone1(self):
        command = PostponeCommand(["-e", "due:tod", "2w"], self.todolist,
                                  self.out, self.error, None)
        command.execute()

        due = self.today + timedelta(14)
        result = "|  2| Bar due:{d}\n|  3| Baz due:{d} t:{s}\n".format(d=due.isoformat(), s=self.start.isoformat())

        self.assertTrue(self.todolist.dirty)
        self.assertEqual(self.output, result)
        self.assertEqual(self.errors, "")

    def test_expr_postpone2(self):
        cmd_args = ["-e", "t:{}".format(self.start.isoformat()), "due:tod", "1w"]
        command = PostponeCommand(cmd_args, self.todolist, self.out,
                                  self.error, None)
        command.execute()

        due = self.today + timedelta(7)

        result = "|  3| Baz due:{} t:{}\n".format(due.isoformat(),
                                                  self.start.isoformat())

        self.assertTrue(self.todolist.dirty)
        self.assertEqual(self.output, result)
        self.assertEqual(self.errors, "")

    def test_expr_postpone3(self):
        command = PostponeCommand(["-e", "@test", "due:tod", "+project", "C"],
                                  self.todolist, self.out, self.error, None)
        command.execute()

        self.assertFalse(self.todolist.dirty)

    def test_expr_postpone4(self):
        """ Don't postpone unrelevant todo items. """
        command = PostponeCommand(["-e", "FutureStart", "1w"], self.todolist,
                                  self.out, self.error, None)
        command.execute()

        self.assertFalse(self.todolist.dirty)

    def test_expr_postpone5(self):
        """ Force postponing unrelevant items with additional -x flag. """
        command = PostponeCommand(["-xe", "FutureStart", "1w"], self.todolist,
                                  self.out, self.error, None)
        command.execute()

        due = self.today + timedelta(7)
        result = "|  6| FutureStart t:{} due:{}\n".format(self.future.isoformat(), due.isoformat())

        self.assertTrue(self.todolist.dirty)
        self.assertEqual(self.output, result)
        self.assertEqual(self.errors, "")

    def test_postpone_name(self):
        name = PostponeCommand.name()

        self.assertEqual(name, 'postpone')

    def test_help(self):
        command = PostponeCommand(["help"], self.todolist, self.out,
                                  self.error)
        command.execute()

        self.assertEqual(self.output, "")
        self.assertEqual(self.errors,
                         command.usage() + "\n\n" + command.help() + "\n")

if __name__ == '__main__':
    unittest.main()
