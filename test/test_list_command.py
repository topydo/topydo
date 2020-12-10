# Topydo - A todo.txt client written in Python.
# Copyright (C) 2014 - 2015 Bram Schoenmakers <bram@topydo.org>
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

import codecs
import os
import re
import sys
import unittest
from collections import namedtuple

import arrow
from freezegun import freeze_time

from topydo.commands.ListCommand import ListCommand
from topydo.lib.Config import config
from topydo.lib.TodoList import TodoList

from .command_testcase import CommandTest
from .facilities import load_file_to_todolist

# We're searching for 'mock'
# 'mock' was added as 'unittest.mock' in Python 3.3, but PyPy 3 is based on Python 3.2
# pylint: disable=no-name-in-module
try:
    from unittest import mock
except ImportError:
    import mock


class ListCommandTest(CommandTest):
    def setUp(self):
        super().setUp()
        self.todolist = load_file_to_todolist("test/data/ListCommandTest.txt")
        self.terminal_size = namedtuple('terminal_size', ['columns', 'lines'])

    def test_list01(self):
        command = ListCommand([""], self.todolist, self.out, self.error)
        command.execute()

        self.assertFalse(self.todolist.dirty)
        self.assertEqual(self.output, "|1| (C) 2015-11-05 Foo @Context2 Not@Context +Project1 Not+Project\n|4| (C) Drink beer @ home\n|5| (C) 13 + 29 = 42\n|2| (D) Bar @Context1 +Project2\n")
        self.assertEqual(self.errors, "")

    def test_list03(self):
        command = ListCommand(["Context1"], self.todolist, self.out,
                              self.error)
        command.execute()

        self.assertFalse(self.todolist.dirty)
        self.assertEqual(self.output, "|2| (D) Bar @Context1 +Project2\n")
        self.assertEqual(self.errors, "")

    def test_list04(self):
        command = ListCommand(["-x", "Context1"], self.todolist, self.out,
                              self.error)
        command.execute()

        self.assertFalse(self.todolist.dirty)
        self.assertEqual(self.output, "|3| (C) Baz @Context1 +Project1 key:value\n|2| (D) Bar @Context1 +Project2\n")
        self.assertEqual(self.errors, "")

    def test_list05(self):
        command = ListCommand(["-x"], self.todolist, self.out, self.error)
        command.execute()

        self.assertFalse(self.todolist.dirty)
        self.assertEqual(self.output, "|1| (C) 2015-11-05 Foo @Context2 Not@Context +Project1 Not+Project\n|3| (C) Baz @Context1 +Project1 key:value\n|4| (C) Drink beer @ home\n|5| (C) 13 + 29 = 42\n|2| (D) Bar @Context1 +Project2\n|7| hidden item h:1\n|6| x 2014-12-12 Completed but with date:2014-12-12\n")
        self.assertEqual(self.errors, "")

    def test_list06(self):
        command = ListCommand(["Project3"], self.todolist, self.out,
                              self.error)
        command.execute()

        self.assertFalse(self.todolist.dirty)
        self.assertEqual(self.output, "")
        self.assertEqual(self.errors, "")

    def test_list07(self):
        command = ListCommand(["-s", "text", "-x", "Project1"], self.todolist,
                              self.out, self.error)
        command.execute()

        self.assertFalse(self.todolist.dirty)
        self.assertEqual(self.output, "|3| (C) Baz @Context1 +Project1 key:value\n|1| (C) 2015-11-05 Foo @Context2 Not@Context +Project1 Not+Project\n")
        self.assertEqual(self.errors, "")

    def test_list08(self):
        command = ListCommand(["--", "-project1"], self.todolist, self.out,
                              self.error)
        command.execute()

        self.assertFalse(self.todolist.dirty)
        self.assertEqual(self.output, "|4| (C) Drink beer @ home\n|5| (C) 13 + 29 = 42\n|2| (D) Bar @Context1 +Project2\n")
        self.assertEqual(self.errors, "")

    def test_list09(self):
        command = ListCommand(["--", "-project1", "-Drink"], self.todolist,
                              self.out, self.error)
        command.execute()

        self.assertFalse(self.todolist.dirty)
        self.assertEqual(self.output, "|5| (C) 13 + 29 = 42\n|2| (D) Bar @Context1 +Project2\n")
        self.assertEqual(self.errors, "")

    def test_list10(self):
        command = ListCommand(["text1", "2"], self.todolist, self.out,
                              self.error)
        command.execute()

        self.assertFalse(self.todolist.dirty)
        self.assertEqual(self.output, "|2| (D) Bar @Context1 +Project2\n")
        self.assertEqual(self.errors, "")

    def test_list11(self):
        config("test/data/listcommand.conf")

        command = ListCommand(["project"], self.todolist, self.out, self.error)
        command.execute()

        self.assertFalse(self.todolist.dirty)
        self.assertEqual(self.output, "|1| (C) 2015-11-05 Foo @Context2 Not@Context +Project1 Not+Project\n")
        self.assertEqual(self.errors, "")

    def test_list12(self):
        config("test/data/listcommand.conf")

        command = ListCommand(["-x", "project"], self.todolist, self.out,
                              self.error)
        command.execute()

        self.assertFalse(self.todolist.dirty)
        self.assertEqual(self.output, "|1| (C) 2015-11-05 Foo @Context2 Not@Context +Project1 Not+Project\n|3| (C) Baz @Context1 +Project1 key:value\n|2| (D) Bar @Context1 +Project2\n")
        self.assertEqual(self.errors, "")

    def test_list13(self):
        command = ListCommand(["-x", "--", "-@Context1 +Project2"],
                              self.todolist, self.out, self.error)
        command.execute()

        self.assertFalse(self.todolist.dirty)
        self.assertEqual(self.output, "|1| (C) 2015-11-05 Foo @Context2 Not@Context +Project1 Not+Project\n|3| (C) Baz @Context1 +Project1 key:value\n|4| (C) Drink beer @ home\n|5| (C) 13 + 29 = 42\n|7| hidden item h:1\n|6| x 2014-12-12 Completed but with date:2014-12-12\n")
        self.assertEqual(self.errors, "")

    def test_list14(self):
        config("test/data/listcommand2.conf")

        command = ListCommand([], self.todolist, self.out, self.error)
        command.execute()

        self.assertFalse(self.todolist.dirty)
        self.assertEqual(self.output, " |1| (C) 2015-11-05 Foo @Context2 Not@Context +Project1 Not+Project\n |4| (C) Drink beer @ home\n |5| (C) 13 + 29 = 42\n |2| (D) Bar @Context1 +Project2\n")
        self.assertEqual(self.errors, "")

    def test_list15(self):
        command = ListCommand(["p:<10"], self.todolist, self.out, self.error)
        command.execute()

        self.assertFalse(self.todolist.dirty)
        self.assertEqual(self.output, "|2| (D) Bar @Context1 +Project2\n")
        self.assertEqual(self.errors, "")

    def test_list16(self):
        config("test/data/todolist-uid.conf")

        command = ListCommand([], self.todolist, self.out, self.error)
        command.execute()

        self.assertFalse(self.todolist.dirty)
        self.assertEqual(self.output, "|t5c| (C) 2015-11-05 Foo @Context2 Not@Context +Project1 Not+Project\n|wa5| (C) Drink beer @ home\n|z63| (C) 13 + 29 = 42\n|mfg| (D) Bar @Context1 +Project2\n")
        self.assertEqual(self.errors, "")

    def test_list17(self):
        command = ListCommand(["-x", "id:"], self.todolist, self.out,
                              self.error)
        command.execute()

        self.assertFalse(self.todolist.dirty)
        self.assertEqual(self.output,
                         "|3| (C) Baz @Context1 +Project1 key:value\n")
        self.assertEqual(self.errors, "")

    def test_list18(self):
        command = ListCommand(["-x", "date:2014-12-12"], self.todolist,
                              self.out, self.error)
        command.execute()

        self.assertFalse(self.todolist.dirty)
        self.assertEqual(self.output, "|6| x 2014-12-12 Completed but with date:2014-12-12\n")

    def test_list19(self):
        """ Force showing all tags. """
        config('test/data/listcommand-tags.conf')

        command = ListCommand(["-s", "text", "-x", "Project1"], self.todolist,
                              self.out, self.error)
        command.execute()

        self.assertFalse(self.todolist.dirty)
        self.assertEqual(self.output, "|3| (C) Baz @Context1 +Project1 id:1 key:value\n|1| (C) 2015-11-05 Foo @Context2 Not@Context +Project1 Not+Project\n")
        self.assertEqual(self.errors, "")

    def test_list20(self):
        command = ListCommand(["-f text"], self.todolist, self.out, self.error)
        command.execute()

        self.assertFalse(self.todolist.dirty)
        self.assertEqual(self.output, "|1| (C) 2015-11-05 Foo @Context2 Not@Context +Project1 Not+Project\n|4| (C) Drink beer @ home\n|5| (C) 13 + 29 = 42\n|2| (D) Bar @Context1 +Project2\n")
        self.assertEqual(self.errors, "")

    def test_list21(self):
        command = ListCommand(["-f invalid"], self.todolist, self.out,
                              self.error)
        command.execute()

        self.assertFalse(self.todolist.dirty)
        self.assertEqual(self.output, "|1| (C) 2015-11-05 Foo @Context2 Not@Context +Project1 Not+Project\n|4| (C) Drink beer @ home\n|5| (C) 13 + 29 = 42\n|2| (D) Bar @Context1 +Project2\n")
        self.assertEqual(self.errors, "")

    def test_list22(self):
        """ Handle tag lists with spaces and punctuation."""
        config(p_overrides={('ls', 'hide_tags'): 'p, id'})
        self.todolist = load_file_to_todolist('test/data/ListCommandTagTest.txt')

        command = ListCommand(["-x"], self.todolist, self.out, self.error)
        command.execute()

        self.assertFalse(self.todolist.dirty)
        self.assertEqual(self.output, '|1| Foo.\n')

    def test_list31(self):
        """ Don't show any todos with -n 0 """
        command = ListCommand(["-n", "0"], self.todolist, self.out, self.error)
        command.execute()

        self.assertEqual(self.output, "")
        self.assertEqual(self.errors, "")

    def test_list32(self):
        """ Only show the top todo. """
        command = ListCommand(["-n", "1"], self.todolist, self.out, self.error)
        command.execute()

        self.assertEqual(self.output, "|1| (C) 2015-11-05 Foo @Context2 Not@Context +Project1 Not+Project\n")
        self.assertEqual(self.errors, "")

    def test_list33(self):
        """ Negative values result in showing all relevent todos. """
        command = ListCommand(["-n", "-1"], self.todolist, self.out, self.error)
        command.execute()

        self.assertEqual(self.output, "|1| (C) 2015-11-05 Foo @Context2 Not@Context +Project1 Not+Project\n|4| (C) Drink beer @ home\n|5| (C) 13 + 29 = 42\n|2| (D) Bar @Context1 +Project2\n")
        self.assertEqual(self.errors, "")

    def test_list34(self):
        """ Test non-integer value for -n """
        config(p_overrides={('ls', 'list_limit'): '2'})

        command = ListCommand(["-n", "foo"], self.todolist, self.out, self.error)
        command.execute()

        self.assertEqual(self.output, "|1| (C) 2015-11-05 Foo @Context2 Not@Context +Project1 Not+Project\n|4| (C) Drink beer @ home\n")
        self.assertEqual(self.errors, "")

    def test_list35(self):
        """ -x flag takes precedence over -n """
        command = ListCommand(["-x", "-n", "foo"], self.todolist, self.out, self.error)
        command.execute()

        self.assertEqual(self.output, "|1| (C) 2015-11-05 Foo @Context2 Not@Context +Project1 Not+Project\n|3| (C) Baz @Context1 +Project1 key:value\n|4| (C) Drink beer @ home\n|5| (C) 13 + 29 = 42\n|2| (D) Bar @Context1 +Project2\n|7| hidden item h:1\n|6| x 2014-12-12 Completed but with date:2014-12-12\n")
        self.assertEqual(self.errors, "")

    def test_list36(self):
        command = ListCommand(["-i", "1"], self.todolist, self.out, self.error)
        command.execute()

        self.assertEqual(self.output, "|1| (C) 2015-11-05 Foo @Context2 Not@Context +Project1 Not+Project\n")
        self.assertEqual(self.errors, "")

    def test_list37(self):
        command = ListCommand(["-i", "1,foo,3"], self.todolist, self.out, self.error)
        command.execute()

        self.assertEqual(self.output, "|1| (C) 2015-11-05 Foo @Context2 Not@Context +Project1 Not+Project\n|3| (C) Baz @Context1 +Project1 key:value\n")
        self.assertEqual(self.errors, "")

    def test_list38(self):
        config("test/data/todolist-uid.conf")

        command = ListCommand(["-i", "1,foo,z63"], self.todolist, self.out, self.error)
        command.execute()

        self.assertEqual(self.output, "|t5c| (C) 2015-11-05 Foo @Context2 Not@Context +Project1 Not+Project\n|z63| (C) 13 + 29 = 42\n")
        self.assertEqual(self.errors, "")

    def test_list39(self):
        config("test/data/todolist-uid.conf")

        command = ListCommand(["-i", "t5c,foo"], self.todolist, self.out, self.error)
        command.execute()

        self.assertEqual(self.output, "|t5c| (C) 2015-11-05 Foo @Context2 Not@Context +Project1 Not+Project\n")
        self.assertEqual(self.errors, "")

    def test_list40(self):
        command = ListCommand(["(<C)"], self.todolist, self.out, self.error)
        command.execute()

        self.assertEqual(self.output, "|2| (D) Bar @Context1 +Project2\n")
        self.assertEqual(self.errors, "")

    def test_list41(self):
        command = ListCommand(["-z", "Zzz"], self.todolist, self.out, self.error)
        command.execute()

        self.assertEqual(self.output, "")
        self.assertEqual(self.errors, "option -z not recognized\n")

    def test_list42(self):
        command = ListCommand(["-x", "+Project1", "-id:1"], self.todolist,
                              self.out, self.error)
        command.execute()

        self.assertEqual(self.output, "|1| (C) 2015-11-05 Foo @Context2 Not@Context +Project1 Not+Project\n")
        self.assertEqual(self.errors, "")

    @mock.patch('topydo.commands.ListCommand.get_terminal_size')
    def test_list43(self, mock_terminal_size):
        """Test basic 'N' parameter."""
        mock_terminal_size.return_value = self.terminal_size(81, 100)

        command = ListCommand(["-N"], self.todolist, self.out, self.error)
        command.execute()

        self.assertEqual(self.output, "|1| (C) 2015-11-05 Foo @Context2 Not@Context +Project1 Not+Project\n|4| (C) Drink beer @ home\n|5| (C) 13 + 29 = 42\n|2| (D) Bar @Context1 +Project2\n")
        self.assertEqual(self.errors, "")

    @mock.patch('topydo.commands.ListCommand.get_terminal_size')
    @mock.patch.dict(os.environ, {'PROMPT':'', 'PS1':''})
    def test_list44(self, mock_terminal_size):
        """
        Test 'N' parameter with output longer than available terminal lines.
        """
        self.todolist = load_file_to_todolist("test/data/ListCommand_50_items.txt")
        if "win32" in sys.platform:
            mock_terminal_size.return_value = self.terminal_size(80, 23)
        else:
            mock_terminal_size.return_value = self.terminal_size(80, 22)

        command = ListCommand(["-N"], self.todolist, self.out, self.error)
        command.execute()

        self.assertEqual(self.output, "| 1| (A) item 1\n|27| (A) item 27\n| 2| (B) item 2\n|28| (B) item 28\n| 3| (C) item 3\n|29| (C) item 29\n| 4| (D) item 4\n|30| (D) item 30\n| 5| (E) item 5\n|31| (E) item 31\n| 6| (F) item 6\n|32| (F) item 32\n| 7| (G) item 7\n|33| (G) item 33\n| 8| (H) item 8\n|34| (H) item 34\n| 9| (I) item 9\n|35| (I) item 35\n|10| (J) item 10\n|36| (J) item 36\n|11| (K) item 11\n")
        self.assertEqual(self.errors, "")

    @mock.patch('topydo.commands.ListCommand.get_terminal_size')
    @mock.patch.dict(os.environ, {'PROMPT':'', 'PS1':''})
    def test_list45(self, mock_terminal_size):
        """Test basic 'N' parameter with nine line terminal."""
        # have 9 lines on the terminal will print 7 items and leave 2 lines
        # for the next prompt
        if "win32" in sys.platform:
            mock_terminal_size.return_value = self.terminal_size(100, 9)
        else:
            mock_terminal_size.return_value = self.terminal_size(100, 8)
        self.todolist = load_file_to_todolist("test/data/ListCommand_50_items.txt")

        command = ListCommand(["-N"], self.todolist, self.out, self.error)
        command.execute()

        self.assertEqual(self.output, "| 1| (A) item 1\n|27| (A) item 27\n| 2| (B) item 2\n|28| (B) item 28\n| 3| (C) item 3\n|29| (C) item 29\n| 4| (D) item 4\n")
        self.assertEqual(self.errors, "")

    @mock.patch('topydo.commands.ListCommand.get_terminal_size')
    @mock.patch.dict(os.environ, {'PROMPT':'', 'PS1':''})
    def test_list46(self, mock_terminal_size):
        """Test basic 'N' parameter with zero height terminal."""
        # we still print at least 1 item
        mock_terminal_size.return_value = self.terminal_size(100, 0)
        self.todolist = load_file_to_todolist("test/data/ListCommand_50_items.txt")

        command = ListCommand(["-N"], self.todolist, self.out, self.error)
        command.execute()

        self.assertEqual(self.output, "| 1| (A) item 1\n")
        self.assertEqual(self.errors, "")

    @mock.patch('topydo.commands.ListCommand.get_terminal_size')
    @mock.patch.dict(os.environ, {'PROMPT':'$E[1;34m%username%@%computername%$E[0m$S$E[1;32m$P$E[0m$_$E[1;37m--$E[0m$S',
                                  'PS1':'username@hostname\n--'})
    def test_list47(self, mock_terminal_size):
        """
        Test 'N' parameter with multiline prompt.
        """
        self.todolist = load_file_to_todolist("test/data/ListCommand_50_items.txt")
        if "win32" in sys.platform:
            mock_terminal_size.return_value = self.terminal_size(80, 23)
        else:
            mock_terminal_size.return_value = self.terminal_size(80, 22)

        command = ListCommand(["-N"], self.todolist, self.out, self.error)
        command.execute()

        self.assertEqual(self.output, "| 1| (A) item 1\n|27| (A) item 27\n| 2| (B) item 2\n|28| (B) item 28\n| 3| (C) item 3\n|29| (C) item 29\n| 4| (D) item 4\n|30| (D) item 30\n| 5| (E) item 5\n|31| (E) item 31\n| 6| (F) item 6\n|32| (F) item 32\n| 7| (G) item 7\n|33| (G) item 33\n| 8| (H) item 8\n|34| (H) item 34\n| 9| (I) item 9\n|35| (I) item 35\n|10| (J) item 10\n|36| (J) item 36\n")
        self.assertEqual(self.errors, "")

    def test_list48(self):
        command = ListCommand(["created:2015-11-05"], self.todolist, self.out, self.error)
        command.execute()

        self.assertEqual(self.output, "|1| (C) 2015-11-05 Foo @Context2 Not@Context +Project1 Not+Project\n")
        self.assertEqual(self.errors, "")

    def test_list49(self):
        """ Only show the top todo. """
        todolist = TodoList([
            "This item is hidden h:1",
            "This item is visible",
        ])

        command = ListCommand(["-n", "1"], todolist, self.out, self.error)
        command.execute()

        self.assertEqual(self.output, '|2| This item is visible\n')
        self.assertEqual(self.errors, "")

    def test_list50(self):
        """
        Fallback to normal alphabet for too short alphabets, fallback on
        default alphabet.
        """
        config(p_overrides={('topydo', 'identifier_alphabet'): 'a', ('topydo', 'identifiers'): 'text'})

        # self.todolist was loaded with old identifier settings
        todolist = load_file_to_todolist("test/data/ListCommandTest.txt")

        command = ListCommand(["-F", "%I", "Foo"], todolist, self.out, self.error)
        command.execute()

        self.assertEqual(self.output, "t5c\n")
        self.assertEqual(self.errors, '')

    def test_list51(self):
        """ Test hexadecimal IDs """
        config(p_overrides={('topydo', 'identifier_alphabet'): '0123456789abcdef', ('topydo', 'identifiers'): 'text'})

        # self.todolist was loaded with old identifier settings
        todolist = load_file_to_todolist("test/data/ListCommandTest.txt")

        command = ListCommand(["-F", "%i", "Foo"], todolist, self.out, self.error)
        command.execute()

        self.assertEqual(self.output, '2c8\n')
        self.assertEqual(self.errors, '')

    def test_list52(self):
        """ Alphabet is too short due to duplicate characters """
        config(p_overrides={('topydo', 'identifier_alphabet'): '0123456788', ('topydo', 'identifiers'): 'text'})

        # self.todolist was loaded with old identifier settings
        todolist = load_file_to_todolist("test/data/ListCommandTest.txt")

        command = ListCommand(["-F", "%i", "Foo"], todolist, self.out, self.error)
        command.execute()

        self.assertEqual(self.output, 't5c\n')
        self.assertEqual(self.errors, '')

    def test_list_name(self):
        name = ListCommand.name()

        self.assertEqual(name, 'list')

    def test_help(self):
        command = ListCommand(["help"], self.todolist, self.out, self.error)
        command.execute()

        self.assertEqual(self.output, "")
        self.assertEqual(self.errors,
                         command.usage() + "\n\n" + command.help() + "\n")


class ListCommandUnicodeTest(CommandTest):
    def setUp(self):
        super().setUp()
        self.todolist = load_file_to_todolist("test/data/ListCommandUnicodeTest.txt")

    def test_list_unicode1(self):
        """ Unicode filters."""
        command = ListCommand([u"\u25c4"], self.todolist, self.out,
                              self.error)
        command.execute()

        self.assertFalse(self.todolist.dirty)

        expected = u"|1| (C) And some sp\u00e9cial tag:\u25c4\n"

        self.assertEqual(self.output, expected)


class ListCommandJsonTest(CommandTest):
    def test_json(self):
        todolist = load_file_to_todolist("test/data/ListCommandTest.txt")

        command = ListCommand(["-f", "json"], todolist, self.out, self.error)
        command.execute()

        self.assertFalse(todolist.dirty)

        jsontext = ""
        with codecs.open('test/data/ListCommandTest.json', 'r',
                         encoding='utf-8') as json:
            jsontext = json.read()

        self.assertEqual(self.output, jsontext)
        self.assertEqual(self.errors, "")

    def test_json_unicode(self):
        todolist = load_file_to_todolist("test/data/ListCommandUnicodeTest.txt")

        command = ListCommand(["-f", "json"], todolist, self.out, self.error)
        command.execute()

        self.assertFalse(todolist.dirty)

        jsontext = ""
        with codecs.open('test/data/ListCommandUnicodeTest.json', 'r',
                         encoding='utf-8') as json:
            jsontext = json.read()

        self.assertEqual(self.output, jsontext)
        self.assertEqual(self.errors, "")


def replace_ical_tags(p_text):
    # replace identifiers with dots, since they're random.
    result = re.sub(r'\bical:....\b', 'ical:....', p_text)
    result = re.sub(r'\bUID:....\b', 'UID:....', result)

    return result


class ListCommandIcalTest(CommandTest):
    def setUp(self):
        self.maxDiff = None

    def test_ical(self):
        try:
            import icalendar
        except ImportError:
            raise unittest.SkipTest("The icalendar module is not available")

        todolist = load_file_to_todolist("test/data/ListCommandIcalTest.txt")

        command = ListCommand(["-x", "-f", "ical"], todolist, self.out,
                              self.error)
        command.execute()

        self.assertTrue(todolist.dirty)

        icaltext = ""
        with codecs.open('test/data/ListCommandTest.ics', 'r',
                         encoding='utf-8') as ical:
            icaltext = ical.read()

        self.assertEqual(replace_ical_tags(self.output),
                         replace_ical_tags(icaltext))
        self.assertEqual(self.errors, "")

    def test_ical_unicode(self):
        try:
            import icalendar
        except ImportError:
            raise unittest.SkipTest("The icalendar module is not available")

        todolist = load_file_to_todolist("test/data/ListCommandUnicodeTest.txt")

        command = ListCommand(["-f", "ical"], todolist, self.out, self.error)
        command.execute()

        self.assertTrue(todolist.dirty)

        icaltext = ""
        with codecs.open('test/data/ListCommandUnicodeTest.ics', 'r',
                         encoding='utf-8') as ical:
            icaltext = ical.read()

        self.assertEqual(replace_ical_tags(self.output),
                         replace_ical_tags(icaltext))
        self.assertEqual(self.errors, "")


@freeze_time('2016, 11, 17')
class ListCommandDotTest(CommandTest):
    def setUp(self):
        self.maxDiff = None

    @mock.patch('arrow.now') # arrow.now() doesn't freeze at UTC
    def test_dot(self, mock_arrow):
        mock_arrow.return_value = arrow.utcnow() # force arrow to UTC

        todolist = load_file_to_todolist("test/data/ListCommandDotTest.txt")

        command = ListCommand(["-x", "-f", "dot"], todolist, self.out,
                              self.error)
        command.execute()

        self.assertFalse(todolist.dirty)

        dottext = ""
        with codecs.open('test/data/ListCommandTest.dot', 'r',
                         encoding='utf-8') as dot:
            dottext = dot.read()

        self.assertEqual(self.output, dottext)
        self.assertEqual(self.errors, "")


@freeze_time('2016, 12, 6')
class ListCommandGroupTest(CommandTest):
    def test_group1(self):
        todolist = load_file_to_todolist("test/data/ListCommandGroupTest.txt")

        command = ListCommand(["-g", "project", "test:test_group1"], todolist, self.out, self.error)
        command.execute()

        self.assertFalse(todolist.dirty)

        self.assertEqual(self.output, """\
Project: A
==========
| 1| +A only test:test_group1
| 3| +A and +B test:test_group1

Project: B
==========
| 3| +A and +B test:test_group1
| 2| +B only test:test_group1

Project: None
=============
| 4| No project test:test_group1
""")

    def test_group2(self):
        todolist = load_file_to_todolist("test/data/ListCommandGroupTest.txt")

        command = ListCommand(["-g", "l", "test:test_group2"], todolist, self.out, self.error)
        command.execute()

        self.assertFalse(todolist.dirty)

        self.assertEqual(self.output, """\
l: 0
====
| 6| Another item l:0 test:test_group2

l: 1
====
| 5| Different item l:1 test:test_group2
""")

    @mock.patch('arrow.now')
    def test_group3(self, mock_arrow):
        mock_arrow.return_value = arrow.utcnow()

        todolist = load_file_to_todolist("test/data/ListCommandGroupTest.txt")

        command = ListCommand(["-g", "due", "test:test_group3"], todolist, self.out, self.error)
        command.execute()

        self.assertFalse(todolist.dirty)

        self.assertEqual(self.output, """\
due: today
==========
| 7| Test 1 test:test_group3 due:2016-12-06

due: in a day
=============
| 8| Test 2 test:test_group3 due:2016-12-07
""")

    @mock.patch('arrow.now')
    def test_group4(self, mock_arrow):
        mock_arrow.return_value = arrow.utcnow()

        todolist = load_file_to_todolist("test/data/ListCommandGroupTest.txt")

        command = ListCommand(["-g", "t", "test:test_group4"], todolist, self.out, self.error)
        command.execute()

        self.assertFalse(todolist.dirty)

        self.assertEqual(self.output, """\
t: today
========
| 9| Test 1 test:test_group4 test:test_group5 t:2016-12-06
""")

    @mock.patch('arrow.now')
    def test_group5(self, mock_arrow):
        mock_arrow.return_value = arrow.utcnow()

        todolist = load_file_to_todolist("test/data/ListCommandGroupTest.txt")

        command = ListCommand(["-x", "-g", "t", "test:test_group5"], todolist, self.out, self.error)
        command.execute()

        self.assertFalse(todolist.dirty)

        self.assertEqual(self.output, """\
t: today
========
| 9| Test 1 test:test_group4 test:test_group5 t:2016-12-06

t: in a day
===========
|10| Test 2 test:test_group4 test:test_group5 t:2016-12-07
""")

    def test_group6(self):
        todolist = load_file_to_todolist("test/data/ListCommandGroupTest.txt")

        command = ListCommand(["-x", "-g", "fake", "test_group6"], todolist, self.out, self.error)
        command.execute()

        self.assertFalse(todolist.dirty)

        self.assertEqual(self.output, """\
fake: No value
==============
|11| Group by non-existing tag test:test_group6
""")

    def test_group7(self):
        todolist = load_file_to_todolist("test/data/ListCommandGroupTest.txt")

        command = ListCommand(["-x", "-g", "desc:project", "test_group7"], todolist, self.out, self.error)
        command.execute()

        self.assertFalse(todolist.dirty)

        self.assertEqual(self.output, """\
Project: B
==========
|13| Sort descending +B test:test_group7

Project: A
==========
|12| Sort descending +A test:test_group7
""")

    def test_group8(self):
        todolist = load_file_to_todolist("test/data/ListCommandGroupTest.txt")

        command = ListCommand(["-x", "-g", "project,desc:context", "test_group8"], todolist, self.out, self.error)
        command.execute()

        self.assertFalse(todolist.dirty)

        self.assertEqual(self.output, """\
Project: A, Context: B
======================
|15| Inner sort 2 +A @B test:test_group8

Project: A, Context: A
======================
|14| Inner sort 1 +A @A test:test_group8

Project: B, Context: B
======================
|17| Inner sort 4 +B @B test:test_group8

Project: B, Context: A
======================
|16| Inner sort 3 +B @A test:test_group8
""")

    def test_group9(self):
        todolist = load_file_to_todolist("test/data/ListCommandGroupTest.txt")

        command = ListCommand(["-x", "-g", "project", "-s", "desc:text", "test_group9"], todolist, self.out, self.error)
        command.execute()

        self.assertFalse(todolist.dirty)

        self.assertEqual(self.output, """\
Project: A
==========
|19| Inner sort 2 +A test:test_group9
|18| Inner sort 1 +A test:test_group9
""")

    def test_group10(self):
        todolist = load_file_to_todolist("test/data/ListCommandGroupTest.txt")

        command = ListCommand(["-x", "-g"], todolist, self.out, self.error)
        command.execute()

        self.assertFalse(todolist.dirty)

        self.assertEqual(self.output, "")
        self.assertEqual(self.errors, "option -g requires argument\n")

    def test_group11(self):
        config(p_overrides={('sort', 'group_string'): 'project'})
        todolist = load_file_to_todolist("test/data/ListCommandGroupTest.txt")

        command = ListCommand(["test:test_group1"], todolist, self.out, self.error)
        command.execute()

        self.assertFalse(todolist.dirty)

        self.assertEqual(self.output, """\
Project: A
==========
| 1| +A only test:test_group1
| 3| +A and +B test:test_group1

Project: B
==========
| 3| +A and +B test:test_group1
| 2| +B only test:test_group1

Project: None
=============
| 4| No project test:test_group1
""")
        self.assertEqual(self.errors, "")

    def test_group12(self):
        todolist = load_file_to_todolist("test/data/ListCommandGroupTest.txt")

        command = ListCommand(["-g", ",", "test:test_group1"], todolist, self.out, self.error)
        command.execute()

        self.assertFalse(todolist.dirty)

        self.assertEqual(self.output, """\
| 1| +A only test:test_group1
| 2| +B only test:test_group1
| 3| +A and +B test:test_group1
| 4| No project test:test_group1
""")
        self.assertEqual(self.errors, "")

if __name__ == '__main__':
    unittest.main()
