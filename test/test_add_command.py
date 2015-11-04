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
from datetime import date
from io import StringIO

from six import u

from test.command_testcase import CommandTest
from topydo.commands import AddCommand, ListCommand
from topydo.lib import TodoList
from topydo.lib.Config import config

# We're searching for 'mock'
# pylint: disable=no-name-in-module
try:
    from unittest import mock
except ImportError:
    import mock


class AddCommandTest(CommandTest):
    def setUp(self):
        super(AddCommandTest, self).setUp()
        self.todolist = TodoList.TodoList([])
        self.today = date.today().isoformat()

    def test_add_task(self):
        args = ["New todo"]
        command = AddCommand.AddCommand(args, self.todolist, self.out,
                                        self.error)
        command.execute()

        self.assertEqual(self.todolist.todo(1).source(),
                         self.today + " New todo")
        self.assertEqual(self.errors, "")

    def test_add_multiple_args(self):
        args = ["New", "todo"]
        command = AddCommand.AddCommand(args, self.todolist, self.out,
                                        self.error)
        command.execute()

        self.assertEqual(self.todolist.todo(1).source(),
                         self.today + " New todo")
        self.assertEqual(self.errors, "")

    def test_add_priority1(self):
        command = AddCommand.AddCommand(["Foo (C)"], self.todolist, self.out,
                                        self.error)
        command.execute()

        self.assertEqual(self.todolist.todo(1).priority(), 'C')
        self.assertEqual(self.todolist.todo(1).source(),
                         "(C) " + self.today + " Foo")
        self.assertEqual(self.errors, "")

    def test_add_priority2(self):
        command = AddCommand.AddCommand(["Foo (CC)"], self.todolist, self.out,
                                        self.error)
        command.execute()

        self.assertEqual(self.todolist.todo(1).priority(), None)
        self.assertEqual(self.todolist.todo(1).source(),
                         self.today + " Foo (CC)")
        self.assertEqual(self.errors, "")

    def test_add_priority3(self):
        command = AddCommand.AddCommand(["Fo(C)o"], self.todolist, self.out,
                                        self.error)
        command.execute()

        self.assertEqual(self.todolist.todo(1).priority(), None)
        self.assertEqual(self.todolist.todo(1).source(),
                         self.today + " Fo(C)o")
        self.assertEqual(self.errors, "")

    def test_add_priority4(self):
        command = AddCommand.AddCommand(["(C) Foo"], self.todolist, self.out,
                                        self.error)
        command.execute()

        self.assertEqual(self.todolist.todo(1).priority(), 'C')
        self.assertEqual(self.todolist.todo(1).source(),
                         "(C) " + self.today + " Foo")
        self.assertEqual(self.errors, "")

    def test_add_dep01(self):
        command = AddCommand.AddCommand(["Foo"], self.todolist, self.out,
                                        self.error)
        command.execute()

        command = AddCommand.AddCommand(["Bar before:1"], self.todolist,
                                        self.out, self.error)
        command.execute()

        self.assertEqual(self.todolist.todo(1).source(),
                         self.today + " Foo id:1")
        self.assertEqual(self.todolist.todo(2).source(),
                         self.today + " Bar p:1")
        self.assertEqual(self.errors, "")

    def test_add_dep02(self):
        command = AddCommand.AddCommand(["Foo"], self.todolist, self.out,
                                        self.error)
        command.execute()

        command = AddCommand.AddCommand(["Bar partof:1"], self.todolist)
        command.execute()

        self.assertEqual(self.todolist.todo(1).source(),
                         self.today + " Foo id:1")
        self.assertEqual(self.todolist.todo(2).source(),
                         self.today + " Bar p:1")
        self.assertEqual(self.errors, "")

    def test_add_dep03(self):
        command = AddCommand.AddCommand(["Foo"], self.todolist)
        command.execute()

        command = AddCommand.AddCommand(["Bar after:1"], self.todolist,
                                        self.out, self.error)
        command.execute()

        self.assertEqual(self.todolist.todo(1).source(),
                         self.today + " Foo p:1")
        self.assertEqual(self.todolist.todo(2).source(),
                         self.today + " Bar id:1")
        self.assertEqual(self.errors, "")

    def test_add_de04(self):
        """ Test for using an after: tag with non-existing value. """
        command = AddCommand.AddCommand(["Foo after:1"], self.todolist,
                                        self.out, self.error)
        command.execute()

        self.assertFalse(self.todolist.todo(1).has_tag("after"))
        self.assertEqual(self.todolist.todo(1).source(), self.today + " Foo")
        self.assertEqual(self.output,
                         "|  1| " + self.todolist.todo(1).source() + "\n")
        self.assertEqual(self.errors, "")

    def test_add_dep05(self):
        """ Test for using an after: tag with non-existing value. """
        command = AddCommand.AddCommand(["Foo after:2"], self.todolist,
                                        self.out, self.error)
        command.execute()

        self.assertFalse(self.todolist.todo(1).has_tag("after"))
        self.assertEqual(self.todolist.todo(1).source(), self.today + " Foo")
        self.assertEqual(self.output,
                         "|  1| " + self.todolist.todo(1).source() + "\n")
        self.assertEqual(self.errors, "")

    def test_add_dep06(self):
        command = AddCommand.AddCommand(["Foo"], self.todolist, self.out,
                                        self.error)
        command.execute()

        command = AddCommand.AddCommand(["Bar"], self.todolist, self.out,
                                        self.error)
        command.execute()

        command = AddCommand.AddCommand(["Baz before:1 before:2"],
                                        self.todolist, self.out, self.error)
        command.execute()

        self.assertEqual(self.todolist.todo(1).source(),
                         self.today + " Foo id:1")
        self.assertEqual(self.todolist.todo(2).source(),
                         self.today + " Bar id:2")
        self.assertEqual(self.todolist.todo(3).source(),
                         self.today + " Baz p:1 p:2")
        self.assertEqual(self.errors, "")

    def test_add_dep07(self):
        command = AddCommand.AddCommand(["Foo"], self.todolist, self.out,
                                        self.error)
        command.execute()

        command = AddCommand.AddCommand(["Bar"], self.todolist, self.out,
                                        self.error)
        command.execute()

        command = AddCommand.AddCommand(["Baz after:1 after:2"], self.todolist,
                                        self.out, self.error)
        command.execute()

        self.assertEqual(self.todolist.todo(1).source(),
                         self.today + " Foo p:1")
        self.assertEqual(self.todolist.todo(2).source(),
                         self.today + " Bar p:1")
        self.assertEqual(self.todolist.todo(3).source(),
                         self.today + " Baz id:1")
        self.assertEqual(self.errors, "")

    def test_add_dep08(self):
        config("test/data/todolist-uid.conf")

        command = AddCommand.AddCommand(["Foo"], self.todolist, self.out,
                                        self.error)
        command.execute()

        command = AddCommand.AddCommand(["Bar after:7ui"], self.todolist,
                                        self.out, self.error)
        command.execute()

        self.assertEqual(self.todolist.todo('7ui').source(),
                         "{} Foo p:1".format(self.today))
        self.assertEqual(self.todolist.todo('8to').source(),
                         "{} Bar id:1".format(self.today))

    def test_add_dep09(self):
        """
        The text ID shown after adding and after an 'ls' must be equal.
        By appending the parent's projects, the textual ID may change.
        """
        config("test/data/todolist-uid-projects.conf")

        # pass identitiy function to for writing output, we're not interested
        # in this output
        command = AddCommand.AddCommand(["Foo +Project"], self.todolist,
                                        lambda t: t, self.error)
        command.execute()

        command = AddCommand.AddCommand(["Bar before:kh0"], self.todolist,
                                        self.out, self.error)
        command.execute()

        command = ListCommand.ListCommand(["Bar"], self.todolist, self.out,
                                          self.error)
        command.execute()

        self.assertEqual(self.output, "|kbn| {today} Bar p:1 +Project\n|kbn| {today} Bar +Project\n".format(today=self.today))

    def test_add_dep10(self):
        """
        The text ID shown after adding and after an 'ls' must be equal.
        By appending the parent's contexts, the textual ID may change.
        """
        config("test/data/todolist-uid-contexts.conf")

        # pass identitiy function to for writing output, we're not interested
        # in this output
        command = AddCommand.AddCommand(["Foo @Context"], self.todolist,
                                        lambda t: t, self.error)
        command.execute()

        command = AddCommand.AddCommand(["Bar before:2a2"], self.todolist,
                                        self.out, self.error)
        command.execute()

        command = ListCommand.ListCommand(["Bar"], self.todolist, self.out,
                                          self.error)
        command.execute()

        self.assertEqual(self.output, "|wb3| {today} Bar p:1 @Context\n|wb3| {today} Bar @Context\n".format(today=self.today))

    def test_add_reldate1(self):
        command = AddCommand.AddCommand(["Foo due:today"], self.todolist,
                                        self.out, self.error)
        command.execute()

        self.assertEqual(self.todolist.todo(1).source(),
                         self.today + " Foo due:" + self.today)
        self.assertEqual(self.errors, "")

    def test_add_reldate2(self):
        command = AddCommand.AddCommand(["Foo t:today due:today"],
                                        self.todolist, self.out, self.error)
        command.execute()

        result = "|  1| {} Foo t:{} due:{}\n".format(self.today, self.today,
                                                     self.today)
        self.assertEqual(self.output, result)
        self.assertEqual(self.errors, "")

    def test_add_empty(self):
        command = AddCommand.AddCommand([], self.todolist, self.out,
                                        self.error)
        command.execute()

        self.assertEqual(self.output, "")
        self.assertEqual(self.errors, command.usage() + "\n")

    def test_add_unicode(self):
        command = AddCommand.AddCommand([u("Special \u25c4")], self.todolist,
                                        self.out, self.error)
        command.execute()

        self.assertEqual(self.output,
                         u("|  1| {} Special \u25c4\n").format(self.today))
        self.assertEqual(self.errors, "")

    @mock.patch("topydo.commands.AddCommand.stdin",
                StringIO(u("Fo\u00f3 due:tod id:1\nB\u0105r before:1")))
    def test_add_from_stdin(self):
        command = AddCommand.AddCommand(["-f", "-"], self.todolist, self.out,
                                        self.error)
        command.execute()

        self.assertEqual(self.output, u("|  1| {tod} Fo\u00f3 due:{tod} id:1\n|  2| {tod} B\u0105r p:1\n".format(tod=self.today)))
        self.assertEqual(self.errors, "")

    def test_add_from_file(self):
        command = AddCommand.AddCommand(["-f", "test/data/AddCommandTest-from_file.txt"], self.todolist, self.out, self.error)
        command.execute()

        self.assertEqual(self.output, u("|  1| {tod} Foo @fo\u00f3b\u0105r due:{tod} id:1\n|  2| {tod} Bar +baz t:{tod} p:1\n".format(tod=self.today)))
        self.assertEqual(self.errors, "")

    def test_add_task_without_date(self):
        config(p_overrides={('add', 'auto_creation_date'): '0'})

        args = ["New todo"]
        command = AddCommand.AddCommand(args, self.todolist, self.out,
                                        self.error)
        command.execute()

        self.assertEqual(self.todolist.todo(1).source(), "New todo")
        self.assertEqual(self.errors, "")

    def test_help(self):
        command = AddCommand.AddCommand(["help"], self.todolist, self.out,
                                        self.error)
        command.execute()

        self.assertEqual(self.output, "")
        self.assertEqual(self.errors,
                         command.usage() + "\n\n" + command.help() + "\n")

if __name__ == '__main__':
    unittest.main()
