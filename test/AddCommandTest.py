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

from datetime import date
import unittest

from topydo.lib import AddCommand
from topydo.lib import ListCommand
import CommandTest
from topydo.lib.Config import config
from topydo.lib import TodoList

class AddCommandTest(CommandTest.CommandTest):
    def setUp(self):
        super(AddCommandTest, self).setUp()
        self.todolist = TodoList.TodoList([])
        self.today = date.today().isoformat()

    def test_add_task(self):
        args = ["New todo"]
        command = AddCommand.AddCommand(args, self.todolist, self.out, self.error)
        command.execute()

        self.assertEquals(self.todolist.todo(1).source(), self.today + " New todo")
        self.assertEquals(self.errors, "")

    def test_add_multiple_args(self):
        args = ["New", "todo"]
        command = AddCommand.AddCommand(args, self.todolist, self.out, self.error)
        command.execute()

        self.assertEquals(self.todolist.todo(1).source(), self.today + " New todo")
        self.assertEquals(self.errors, "")

    def test_add_priority1(self):
        command = AddCommand.AddCommand(["Foo (C)"], self.todolist, self.out, self.error)
        command.execute()

        self.assertEquals(self.todolist.todo(1).priority(), 'C')
        self.assertEquals(self.todolist.todo(1).source(), "(C) " + self.today + " Foo")
        self.assertEquals(self.errors, "")

    def test_add_priority2(self):
        command = AddCommand.AddCommand(["Foo (CC)"], self.todolist, self.out, self.error)
        command.execute()

        self.assertEquals(self.todolist.todo(1).priority(), None)
        self.assertEquals(self.todolist.todo(1).source(), self.today + " Foo (CC)")
        self.assertEquals(self.errors, "")

    def test_add_priority3(self):
        command = AddCommand.AddCommand(["Fo(C)o"], self.todolist, self.out, self.error)
        command.execute()

        self.assertEquals(self.todolist.todo(1).priority(), None)
        self.assertEquals(self.todolist.todo(1).source(), self.today + " Fo(C)o" )
        self.assertEquals(self.errors, "")

    def test_add_priority4(self):
        command = AddCommand.AddCommand(["(C) Foo"], self.todolist, self.out, self.error)
        command.execute()

        self.assertEquals(self.todolist.todo(1).priority(), 'C')
        self.assertEquals(self.todolist.todo(1).source(), "(C) " + self.today + " Foo")
        self.assertEquals(self.errors, "")

    def test_add_dep1(self):
        command = AddCommand.AddCommand(["Foo"], self.todolist, self.out, self.error)
        command.execute()

        command = AddCommand.AddCommand(["Bar before:1"], self.todolist, self.out, self.error)
        command.execute()

        self.assertEquals(self.todolist.todo(1).source(), self.today + " Foo id:1")
        self.assertEquals(self.todolist.todo(2).source(), self.today + " Bar p:1")
        self.assertEquals(self.errors, "")

    def test_add_dep2(self):
        command = AddCommand.AddCommand(["Foo"], self.todolist, self.out, self.error)
        command.execute()

        command = AddCommand.AddCommand(["Bar partof:1"], self.todolist)
        command.execute()

        self.assertEquals(self.todolist.todo(1).source(), self.today + " Foo id:1")
        self.assertEquals(self.todolist.todo(2).source(), self.today + " Bar p:1")
        self.assertEquals(self.errors, "")

    def test_add_dep3(self):
        command = AddCommand.AddCommand(["Foo"], self.todolist)
        command.execute()

        command = AddCommand.AddCommand(["Bar after:1"], self.todolist, self.out, self.error)
        command.execute()

        self.assertEquals(self.todolist.todo(1).source(), self.today + " Foo p:1")
        self.assertEquals(self.todolist.todo(2).source(), self.today + " Bar id:1")
        self.assertEquals(self.errors, "")

    def test_add_dep4(self):
        """ Test for using an after: tag with non-existing value. """
        command = AddCommand.AddCommand(["Foo after:1"], self.todolist, self.out, self.error)
        command.execute()

        self.assertFalse(self.todolist.todo(1).has_tag("after"))
        self.assertEquals(self.todolist.todo(1).source(), self.today + " Foo")
        self.assertEquals(self.output, "|  1| " + str(self.todolist.todo(1)) + "\n")
        self.assertEquals(self.errors, "")

    def test_add_dep5(self):
        """ Test for using an after: tag with non-existing value. """
        command = AddCommand.AddCommand(["Foo after:2"], self.todolist, self.out, self.error)
        command.execute()

        self.assertFalse(self.todolist.todo(1).has_tag("after"))
        self.assertEquals(self.todolist.todo(1).source(), self.today + " Foo")
        self.assertEquals(self.output, "|  1| " + str(self.todolist.todo(1)) + "\n")
        self.assertEquals(self.errors, "")

    def test_add_dep6(self):
        command = AddCommand.AddCommand(["Foo"], self.todolist, self.out, self.error)
        command.execute()

        command = AddCommand.AddCommand(["Bar"], self.todolist, self.out, self.error)
        command.execute()

        command = AddCommand.AddCommand(["Baz before:1 before:2"], self.todolist, self.out, self.error)
        command.execute()

        self.assertEquals(self.todolist.todo(1).source(), self.today + " Foo id:1")
        self.assertEquals(self.todolist.todo(2).source(), self.today + " Bar id:2")
        self.assertEquals(self.todolist.todo(3).source(), self.today + " Baz p:1 p:2")
        self.assertEquals(self.errors, "")

    def test_add_dep7(self):
        command = AddCommand.AddCommand(["Foo"], self.todolist, self.out, self.error)
        command.execute()

        command = AddCommand.AddCommand(["Bar"], self.todolist, self.out, self.error)
        command.execute()

        command = AddCommand.AddCommand(["Baz after:1 after:2"], self.todolist, self.out, self.error)
        command.execute()

        self.assertEquals(self.todolist.todo(1).source(), self.today + " Foo p:1")
        self.assertEquals(self.todolist.todo(2).source(), self.today + " Bar p:1")
        self.assertEquals(self.todolist.todo(3).source(), self.today + " Baz id:1")
        self.assertEquals(self.errors, "")

    def test_add_dep8(self):
        config("test/data/todolist-uid.conf")

        command = AddCommand.AddCommand(["Foo"], self.todolist, self.out, self.error)
        command.execute()

        command = AddCommand.AddCommand(["Bar after:tpi"], self.todolist, self.out, self.error)
        command.execute()

        self.assertEquals(self.todolist.todo('tpi').source(), "{} Foo p:1".format(self.today))
        self.assertEquals(self.todolist.todo('b0n').source(), "{} Bar id:1".format(self.today))

    def test_add_dep9(self):
        """
        The text ID shown after adding and after an 'ls' must be equal."
        By appending the parent's projects, the textual ID may change.
        """
        config("test/data/todolist-uid-projects.conf")

        # pass identitiy function to for writing output, we're not interested
        # in this output
        command = AddCommand.AddCommand(["Foo +Project"], self.todolist, lambda t: t, self.error)
        command.execute()

        command = AddCommand.AddCommand(["Bar before:eqk"], self.todolist, self.out, self.error)
        command.execute()

        command = ListCommand.ListCommand(["Bar"], self.todolist, self.out, self.error)
        command.execute()

        self.assertEquals(self.output, "|5dh| {today} Bar p:1 +Project\n|5dh| {today} Bar +Project\n".format(today=self.today))

    def test_add_dep10(self):
        """
        The text ID shown after adding and after an 'ls' must be equal."
        By appending the parent's contexts, the textual ID may change.
        """
        config("test/data/todolist-uid-contexts.conf")

        # pass identitiy function to for writing output, we're not interested
        # in this output
        command = AddCommand.AddCommand(["Foo @Context"], self.todolist, lambda t: t, self.error)
        command.execute()

        command = AddCommand.AddCommand(["Bar before:x2k"], self.todolist, self.out, self.error)
        command.execute()

        command = ListCommand.ListCommand(["Bar"], self.todolist, self.out, self.error)
        command.execute()

        self.assertEquals(self.output, "|5dc| {today} Bar p:1 @Context\n|5dc| {today} Bar @Context\n".format(today=self.today))

    def test_add_reldate1(self):
        command = AddCommand.AddCommand(["Foo due:today"], self.todolist, self.out, self.error)
        command.execute()

        self.assertEquals(self.todolist.todo(1).source(), self.today + " Foo due:" + self.today)
        self.assertEquals(self.errors, "")

    def test_add_reldate2(self):
        command = AddCommand.AddCommand(["Foo t:today due:today"], self.todolist, self.out, self.error)
        command.execute()

        result = "|  1| {} Foo t:{} due:{}\n".format(self.today, self.today, self.today)
        self.assertEquals(self.output, result)
        self.assertEquals(self.errors, "")

    def test_add_empty(self):
        command = AddCommand.AddCommand([], self.todolist, self.out, self.error)
        command.execute()

        self.assertEquals(self.output, "")
        self.assertEquals(self.errors, command.usage() + "\n")

    def test_help(self):
        command = AddCommand.AddCommand(["help"], self.todolist, self.out, self.error)
        command.execute()

        self.assertEquals(self.output, "")
        self.assertEquals(self.errors, command.usage() + "\n\n" + command.help() + "\n")

if __name__ == '__main__':
    unittest.main()
