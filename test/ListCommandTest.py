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

from topydo.lib.Config import config
import CommandTest
from topydo.lib.ListCommand import ListCommand
import TestFacilities

class ListCommandTest(CommandTest.CommandTest):
    def setUp(self):
        super(ListCommandTest, self).setUp()
        self.todolist = TestFacilities.load_file_to_todolist("test/data/ListCommandTest.txt")

    def test_list1(self):
        command = ListCommand([""], self.todolist, self.out, self.error)
        command.execute()

        self.assertFalse(self.todolist.is_dirty())
        self.assertEquals(self.output, "|  1| (C) Foo @Context2 Not@Context +Project1 Not+Project\n|  4| (C) Drink beer @ home\n|  5| (C) 13 + 29 = 42\n|  2| (D) Bar @Context1 +Project2\n")
        self.assertEquals(self.errors, "")

    def test_list3(self):
        command = ListCommand(["Context1"], self.todolist, self.out, self.error)
        command.execute()

        self.assertFalse(self.todolist.is_dirty())
        self.assertEquals(self.output, "|  2| (D) Bar @Context1 +Project2\n")
        self.assertEquals(self.errors, "")

    def test_list4(self):
        command = ListCommand(["-x", "Context1"], self.todolist, self.out, self.error)
        command.execute()

        self.assertFalse(self.todolist.is_dirty())
        self.assertEquals(self.output, "|  3| (C) Baz @Context1 +Project1 key:value\n|  2| (D) Bar @Context1 +Project2\n")
        self.assertEquals(self.errors, "")

    def test_list5(self):
        command = ListCommand(["-x"], self.todolist, self.out, self.error)
        command.execute()

        self.assertFalse(self.todolist.is_dirty())
        self.assertEquals(self.output, "|  1| (C) Foo @Context2 Not@Context +Project1 Not+Project\n|  3| (C) Baz @Context1 +Project1 key:value\n|  4| (C) Drink beer @ home\n|  5| (C) 13 + 29 = 42\n|  2| (D) Bar @Context1 +Project2\n|  6| x 2014-12-12 Completed but with date:2014-12-12\n")
        self.assertEquals(self.errors, "")

    def test_list6(self):
        command = ListCommand(["Project3"], self.todolist, self.out, self.error)
        command.execute()

        self.assertFalse(self.todolist.is_dirty())
        self.assertEquals(self.output, "")
        self.assertEquals(self.errors, "")

    def test_list7(self):
        command = ListCommand(["-s", "text", "-x", "Project1"], self.todolist, self.out, self.error)
        command.execute()

        self.assertFalse(self.todolist.is_dirty())
        self.assertEquals(self.output, "|  3| (C) Baz @Context1 +Project1 key:value\n|  1| (C) Foo @Context2 Not@Context +Project1 Not+Project\n")
        self.assertEquals(self.errors, "")

    def test_list8(self):
        command = ListCommand(["--", "-project1"], self.todolist, self.out, self.error)
        command.execute()

        self.assertFalse(self.todolist.is_dirty())
        self.assertEquals(self.output, "|  4| (C) Drink beer @ home\n|  5| (C) 13 + 29 = 42\n|  2| (D) Bar @Context1 +Project2\n")
        self.assertEquals(self.errors, "")

    def test_list9(self):
        command = ListCommand(["--", "-project1", "-Drink"], self.todolist, self.out, self.error)
        command.execute()

        self.assertFalse(self.todolist.is_dirty())
        self.assertEquals(self.output, "|  5| (C) 13 + 29 = 42\n|  2| (D) Bar @Context1 +Project2\n")
        self.assertEquals(self.errors, "")

    def test_list10(self):
        command = ListCommand(["text1", "2"], self.todolist, self.out, self.error)
        command.execute()

        self.assertFalse(self.todolist.is_dirty())
        self.assertEquals(self.output, "|  2| (D) Bar @Context1 +Project2\n")
        self.assertEquals(self.errors, "")

    def test_list11(self):
        config("test/data/listcommand.conf")

        command = ListCommand(["project"], self.todolist, self.out, self.error)
        command.execute()

        self.assertFalse(self.todolist.is_dirty())
        self.assertEquals(self.output, "|  1| (C) Foo @Context2 Not@Context +Project1 Not+Project\n")
        self.assertEquals(self.errors, "")

    def test_list12(self):
        config("test/data/listcommand.conf")

        command = ListCommand(["-x", "project"], self.todolist, self.out, self.error)
        command.execute()

        self.assertFalse(self.todolist.is_dirty())
        self.assertEquals(self.output, "|  1| (C) Foo @Context2 Not@Context +Project1 Not+Project\n|  3| (C) Baz @Context1 +Project1 key:value\n|  2| (D) Bar @Context1 +Project2\n")
        self.assertEquals(self.errors, "")

    def test_list13(self):
        command = ListCommand(["-x", "--", "-@Context1 +Project2"], self.todolist, self.out, self.error)
        command.execute()

        self.assertFalse(self.todolist.is_dirty())
        self.assertEquals(self.output, "|  1| (C) Foo @Context2 Not@Context +Project1 Not+Project\n|  3| (C) Baz @Context1 +Project1 key:value\n|  4| (C) Drink beer @ home\n|  5| (C) 13 + 29 = 42\n|  6| x 2014-12-12 Completed but with date:2014-12-12\n")
        self.assertEquals(self.errors, "")

    def test_list14(self):
        config("test/data/listcommand2.conf")

        command = ListCommand([], self.todolist, self.out, self.error)
        command.execute()

        self.assertFalse(self.todolist.is_dirty())
        self.assertEquals(self.output, " |  1| (C) Foo @Context2 Not@Context +Project1 Not+Project\n |  4| (C) Drink beer @ home\n |  5| (C) 13 + 29 = 42\n |  2| (D) Bar @Context1 +Project2\n")
        self.assertEquals(self.errors, "")

    def test_list15(self):
        command = ListCommand(["p:<10"], self.todolist, self.out, self.error)
        command.execute()

        self.assertFalse(self.todolist.is_dirty())
        self.assertEquals(self.output, "|  2| (D) Bar @Context1 +Project2\n")
        self.assertEquals(self.errors, "")

    def test_list16(self):
        config("test/data/todolist-uid.conf")

        command = ListCommand([], self.todolist, self.out, self.error)
        command.execute()

        self.assertFalse(self.todolist.is_dirty())
        self.assertEquals(self.output, "|6iu| (C) Foo @Context2 Not@Context +Project1 Not+Project\n|til| (C) Drink beer @ home\n| c5| (C) 13 + 29 = 42\n|xvb| (D) Bar @Context1 +Project2\n")
        self.assertEquals(self.errors, "")

    def test_list17(self):
        command = ListCommand(["-x", "id:"], self.todolist, self.out, self.error)
        command.execute()

        self.assertFalse(self.todolist.is_dirty())
        self.assertEquals(self.output, "|  3| (C) Baz @Context1 +Project1 key:value\n")
        self.assertEquals(self.errors, "")

    def test_list18(self):
        command = ListCommand(["-x", "date:2014-12-12"], self.todolist, self.out, self.error)
        command.execute()

        self.assertFalse(self.todolist.is_dirty())
        self.assertEquals(self.output, "|  6| x 2014-12-12 Completed but with date:2014-12-12\n")

    def test_list19(self):
        """ Force showing all tags. """
        config('test/data/listcommand-tags.conf')

        command = ListCommand(["-s", "text", "-x", "Project1"], self.todolist, self.out, self.error)
        command.execute()

        self.assertFalse(self.todolist.is_dirty())
        self.assertEquals(self.output, "|  3| (C) Baz @Context1 +Project1 key:value id:1\n|  1| (C) Foo @Context2 Not@Context +Project1 Not+Project\n")
        self.assertEquals(self.errors, "")

    def test_help(self):
        command = ListCommand(["help"], self.todolist, self.out, self.error)
        command.execute()

        self.assertEquals(self.output, "")
        self.assertEquals(self.errors, command.usage() + "\n\n" + command.help() + "\n")

if __name__ == '__main__':
    unittest.main()
