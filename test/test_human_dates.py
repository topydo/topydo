# Topydo - A todo.txt client written in Python.
# Copyright (C) 2015 Bram Schoenmakers <me@bramschoenmakers.nl>
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
from test.command_testcase import CommandTest

from topydo.commands import AddCommand, ListCommand
from topydo.lib import TodoList
from topydo.lib.Config import config


class HumanDatesTest(CommandTest):

    def setUp(self):
        super(HumanDatesTest, self).setUp()
        self.todolist = TodoList.TodoList([])
        self.today = date.today().isoformat()
        self.tomorrow = (date.today() + timedelta(days=1)).isoformat()

    def testAddedDate(self):
        """ Converts the date added to a human readable format. """
        args = ["New todo"]
        command = AddCommand.AddCommand(args, self.todolist, self.out,
                                        self.error)
        command.execute()
        self.assertEqual(self.errors, "")

        self.output = ""
        command = ListCommand.ListCommand([], self.todolist, self.out,
                                          self.error)
        command.execute()
        self.assertEqual(self.output, "|  1|   New todo (just now)\n")
        self.assertEqual(self.errors, "")

    def testDueDate(self):
        """ Converts the due date to a human readable format. """
        args = ["New todo due:{}".format(self.today)]
        command = AddCommand.AddCommand(args, self.todolist, self.out,
                                        self.error)
        command.execute()
        self.assertEqual(self.errors, "")

        self.output = ""
        command = ListCommand.ListCommand([], self.todolist, self.out,
                                          self.error)
        command.execute()
        self.assertEqual(self.output,
                         "|  1|   New todo (just now, due just now)\n")
        self.assertEqual(self.errors, "")

    def testThresholdDate(self):
        """ Converts the threshold date to a human readable format. """
        args = ["New todo {}:{}".format(config().tag_start(), self.today)]
        command = AddCommand.AddCommand(args, self.todolist, self.out,
                                        self.error)
        command.execute()
        self.assertEqual(self.errors, "")

        self.output = ""
        command = ListCommand.ListCommand([], self.todolist, self.out,
                                          self.error)
        command.execute()
        self.assertEqual(self.output, "|  1|   New todo (just now, threshold of just now)\n")
        self.assertEqual(self.errors, "")

    def testThresholdFutureDate(self):
        """ Deals with a future threshold date. """
        args = ["New todo {}:{}".format(config().tag_start(), self.tomorrow)]
        command = AddCommand.AddCommand(args, self.todolist, self.out,
                                        self.error)
        command.execute()
        self.assertEqual(self.errors, "")

        self.output = ""
        command = ListCommand.ListCommand(['-x'], self.todolist, self.out,
                                          self.error)
        command.execute()
        self.assertEqual(self.output, "|  1|   New todo (just now, threshold in a day)\n")
        self.assertEqual(self.errors, "")

    def testThreeDates(self):
        """
        Converts all three dates (added, due, threshold) to a human readable
        format.
        """
        args = ["New todo due:{} {}:{}".format(self.today,
                                               config().tag_start(),
                                               self.today)]
        command = AddCommand.AddCommand(args, self.todolist, self.out,
                                        self.error)
        command.execute()
        self.assertEqual(self.errors, "")

        self.output = ""
        command = ListCommand.ListCommand([], self.todolist, self.out,
                                          self.error)
        command.execute()
        self.assertEqual(self.output, "|  1|   New todo (just now, due just now, threshold of just now)\n")
        self.assertEqual(self.errors, "")


if __name__ == '__main__':
    unittest.main()
