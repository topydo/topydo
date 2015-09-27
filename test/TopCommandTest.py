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

from six import u
import unittest

from topydo.lib.Config import config
from topydo.commands.TopCommand import TopCommand
from test.CommandTest import CommandTest
from test.TestFacilities import load_file_to_todolist


class TopCommandTest(CommandTest):

    def setUp(self):
        super(TopCommandTest, self).setUp()
        self.todolist = load_file_to_todolist("test/data/ListCommandTest.txt")

    def test_top01(self):
        command = TopCommand([""], self.todolist, self.out, self.error)
        command.execute()

        self.assertFalse(self.todolist.is_dirty())
        self.assertEqual(self.output, "|  1| C Foo @Context2 Not@Context +Project1 Not+Project\n|  4| C Drink beer @ home\n|  5| C 13 + 29 = 42\n|  2| D Bar @Context1 +Project2\n")
        self.assertEqual(self.errors, "")

    def test_top03(self):
        command = TopCommand(["Context1"], self.todolist, self.out, self.error)
        command.execute()

        self.assertFalse(self.todolist.is_dirty())
        self.assertEqual(self.output, "|  2| D Bar @Context1 +Project2\n")
        self.assertEqual(self.errors, "")

    def test_top04(self):
        command = TopCommand(["-x", "Context1"], self.todolist, self.out, self.error)
        command.execute()

        self.assertFalse(self.todolist.is_dirty())
        self.assertEqual(self.output, "|  3| C Baz @Context1 +Project1 key:value\n|  2| D Bar @Context1 +Project2\n")
        self.assertEqual(self.errors, "")

    def test_top05(self):
        command = TopCommand(["-x"], self.todolist, self.out, self.error)
        command.execute()

        self.assertFalse(self.todolist.is_dirty())
        self.assertEqual(self.output, "|  1| C Foo @Context2 Not@Context +Project1 Not+Project\n|  3| C Baz @Context1 +Project1 key:value\n|  4| C Drink beer @ home\n|  5| C 13 + 29 = 42\n|  2| D Bar @Context1 +Project2\n|  6|   x 2014-12-12 Completed but with date:2014-12-12\n")
        self.assertEqual(self.errors, "")

    def test_top06(self):
        command = TopCommand(["Project3"], self.todolist, self.out, self.error)
        command.execute()

        self.assertFalse(self.todolist.is_dirty())
        self.assertEqual(self.output, "")
        self.assertEqual(self.errors, "")

    def test_top07(self):
        command = TopCommand(["-s", "text", "-x", "Project1"], self.todolist, self.out, self.error)
        command.execute()

        self.assertFalse(self.todolist.is_dirty())
        self.assertEqual(self.output, "|  3| C Baz @Context1 +Project1 key:value\n|  1| C Foo @Context2 Not@Context +Project1 Not+Project\n")
        self.assertEqual(self.errors, "")

    def test_top08(self):
        command = TopCommand(["--", "-project1"], self.todolist, self.out, self.error)
        command.execute()

        self.assertFalse(self.todolist.is_dirty())
        self.assertEqual(self.output, "|  4| C Drink beer @ home\n|  5| C 13 + 29 = 42\n|  2| D Bar @Context1 +Project2\n")
        self.assertEqual(self.errors, "")

    def test_top09(self):
        command = TopCommand(["--", "-project1", "-Drink"], self.todolist, self.out, self.error)
        command.execute()

        self.assertFalse(self.todolist.is_dirty())
        self.assertEqual(self.output, "|  5| C 13 + 29 = 42\n|  2| D Bar @Context1 +Project2\n")
        self.assertEqual(self.errors, "")

    def test_top10(self):
        command = TopCommand(["text1", "2"], self.todolist, self.out, self.error)
        command.execute()

        self.assertFalse(self.todolist.is_dirty())
        self.assertEqual(self.output, "|  2| D Bar @Context1 +Project2\n")
        self.assertEqual(self.errors, "")

    def test_top11(self):
        config("test/data/listcommand.conf")

        command = TopCommand(["project"], self.todolist, self.out, self.error)
        command.execute()

        self.assertFalse(self.todolist.is_dirty())
        self.assertEqual(self.output, "|  1| C Foo @Context2 Not@Context +Project1 Not+Project\n")
        self.assertEqual(self.errors, "")

    def test_top12(self):
        config("test/data/listcommand.conf")

        command = TopCommand(["-x", "project"], self.todolist, self.out, self.error)
        command.execute()

        self.assertFalse(self.todolist.is_dirty())
        self.assertEqual(self.output, "|  1| C Foo @Context2 Not@Context +Project1 Not+Project\n|  3| C Baz @Context1 +Project1 key:value\n|  2| D Bar @Context1 +Project2\n")
        self.assertEqual(self.errors, "")

    def test_top13(self):
        command = TopCommand(["-x", "--", "-@Context1 +Project2"], self.todolist, self.out, self.error)
        command.execute()

        self.assertFalse(self.todolist.is_dirty())
        self.assertEqual(self.output, "|  1| C Foo @Context2 Not@Context +Project1 Not+Project\n|  3| C Baz @Context1 +Project1 key:value\n|  4| C Drink beer @ home\n|  5| C 13 + 29 = 42\n|  6|   x 2014-12-12 Completed but with date:2014-12-12\n")
        self.assertEqual(self.errors, "")

    def test_top14(self):
        config("test/data/listcommand2.conf")

        command = TopCommand([], self.todolist, self.out, self.error)
        command.execute()

        self.assertFalse(self.todolist.is_dirty())
        self.assertEqual(self.output, " |  1| C Foo @Context2 Not@Context +Project1 Not+Project\n |  4| C Drink beer @ home\n |  5| C 13 + 29 = 42\n |  2| D Bar @Context1 +Project2\n")
        self.assertEqual(self.errors, "")

    def test_top15(self):
        command = TopCommand(["p:<10"], self.todolist, self.out, self.error)
        command.execute()

        self.assertFalse(self.todolist.is_dirty())
        self.assertEqual(self.output, "|  2| D Bar @Context1 +Project2\n")
        self.assertEqual(self.errors, "")

    def test_top16(self):
        config("test/data/todolist-uid.conf")

        command = TopCommand([], self.todolist, self.out, self.error)
        command.execute()

        self.assertFalse(self.todolist.is_dirty())
        self.assertEqual(self.output, "|t5c| C Foo @Context2 Not@Context +Project1 Not+Project\n|wa5| C Drink beer @ home\n|z63| C 13 + 29 = 42\n|mfg| D Bar @Context1 +Project2\n")
        self.assertEqual(self.errors, "")

    def test_top17(self):
        command = TopCommand(["-x", "id:"], self.todolist, self.out, self.error)
        command.execute()

        self.assertFalse(self.todolist.is_dirty())
        self.assertEqual(self.output, "|  3| C Baz @Context1 +Project1 key:value\n")
        self.assertEqual(self.errors, "")

    def test_top18(self):
        command = TopCommand(["-x", "date:2014-12-12"], self.todolist, self.out, self.error)
        command.execute()

        self.assertFalse(self.todolist.is_dirty())
        self.assertEqual(self.output, "|  6|   x 2014-12-12 Completed but with date:2014-12-12\n")

    def test_top19(self):
        """ Force showing all tags. """
        config('test/data/listcommand-tags.conf')

        command = TopCommand(["-s", "text", "-x", "Project1"], self.todolist, self.out, self.error)
        command.execute()

        self.assertFalse(self.todolist.is_dirty())
        self.assertEqual(self.output, "|  3| C Baz @Context1 +Project1 key:value id:1\n|  1| C Foo @Context2 Not@Context +Project1 Not+Project\n")
        self.assertEqual(self.errors, "")

    def test_top20(self):
        command = TopCommand(["-f text"], self.todolist, self.out, self.error)
        command.execute()

        self.assertFalse(self.todolist.is_dirty())
        self.assertEqual(self.output, "|  1| C Foo @Context2 Not@Context +Project1 Not+Project\n|  4| C Drink beer @ home\n|  5| C 13 + 29 = 42\n|  2| D Bar @Context1 +Project2\n")
        self.assertEqual(self.errors, "")

    def test_top21(self):
        command = TopCommand(["-f invalid"], self.todolist, self.out, self.error)
        command.execute()

        self.assertFalse(self.todolist.is_dirty())
        self.assertEqual(self.output, "|  1| C Foo @Context2 Not@Context +Project1 Not+Project\n|  4| C Drink beer @ home\n|  5| C 13 + 29 = 42\n|  2| D Bar @Context1 +Project2\n")
        self.assertEqual(self.errors, "")

    # skip test_top22 through test_top29

    # To-Do: add tests with multiline todo items, add tests of human readable dates

    def test_help(self):
        command = TopCommand(["help"], self.todolist, self.out, self.error)
        command.execute()

        self.assertEqual(self.output, "")
        self.assertEqual(self.errors, command.usage() + "\n\n" + command.help() + "\n")


class TopCommandUnicodeTest(CommandTest):

    def setUp(self):
        super(TopCommandUnicodeTest, self).setUp()
        self.todolist = load_file_to_todolist("test/data/ListCommandUnicodeTest.txt")

    def test_top_unicode1(self):
        """ Unicode filters """
        command = TopCommand([u("\u25c4")], self.todolist, self.out, self.error)
        command.execute()

        self.assertFalse(self.todolist.is_dirty())

        expected = u("|  1| C And some sp\u00e9cial tag:\u25c4\n")

        self.assertEqual(self.output, expected)

if __name__ == '__main__':
    unittest.main()
