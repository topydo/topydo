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

import unittest
from collections import namedtuple

import arrow
from freezegun import freeze_time

from topydo.commands.ListCommand import ListCommand
from topydo.lib.Config import config
from topydo.lib.TodoListBase import TodoListBase

from .command_testcase import CommandTest
from .facilities import load_file_to_todolist

# We're searching for 'mock'
# 'mock' was added as 'unittest.mock' in Python 3.3, but PyPy 3 is based on Python 3.2
# pylint: disable=no-name-in-module
try:
    from unittest import mock
except ImportError:
    import mock


@freeze_time("2015, 11, 06")
class ListFormatTest(CommandTest):
    def setUp(self):
        super().setUp()
        self.maxDiff = None
        self.todolist = load_file_to_todolist("test/data/ListFormat.txt")
        self.terminal_size = namedtuple('terminal_size', ['columns', 'lines'])

    def test_list_format01(self):
        config(p_overrides={('ls', 'list_format'): '|%I| %x %{(}p{)} %c %s %K'})
        command = ListCommand(["-x"], self.todolist, self.out, self.error)
        command.execute()

        result = """|1| (D) 2015-08-31 Bar @Context1 +Project2 due:2015-09-30 t:2015-09-29
|2| (Z) 2015-11-06 Lorem ipsum dolorem sit amet. Red @fox +jumped over the and jar due:2015-11-08 lazy:bar t:2015-11-07
|3| (C) 2015-07-12 Foo @Context2 Not@Context +Project1 Not+Project
|4| (C) Baz @Context1 +Project1 key:value
|5| Drink beer @ home ical:foobar id:1 p:2
|6| x 2014-12-12 Completed but with date:2014-12-12
"""
        self.assertEqual(self.output, result)

    @mock.patch('topydo.lib.ListFormat.get_terminal_size')
    def test_list_format02(self, mock_terminal_size):
        mock_terminal_size.return_value = self.terminal_size(80, 25)

        config(p_overrides={('ls', 'list_format'): '|%I| %x %{(}p{)} %c %S %K'})
        command = ListCommand(["-x"], self.todolist, self.out, self.error)
        command.execute()

        result = """|1| (D) 2015-08-31 Bar @Context1 +Project2 due:2015-09-30 t:2015-09-29
|2| (Z) 2015-11-06 Lorem ipsum dolorem ... due:2015-11-08 lazy:bar t:2015-11-07
|3| (C) 2015-07-12 Foo @Context2 Not@Context +Project1 Not+Project
|4| (C) Baz @Context1 +Project1 key:value
|5| Drink beer @ home ical:foobar id:1 p:2
|6| x 2014-12-12 Completed but with date:2014-12-12
"""
        self.assertEqual(self.output, result)

    @mock.patch('topydo.lib.ListFormat.get_terminal_size')
    def test_list_format03(self, mock_terminal_size):
        mock_terminal_size.return_value = self.terminal_size(100, 25)

        config(p_overrides={('ls', 'list_format'): '|%I| %x %{(}p{)} %c %S %K'})
        command = ListCommand(["-x"], self.todolist, self.out, self.error)
        command.execute()

        result = """|1| (D) 2015-08-31 Bar @Context1 +Project2 due:2015-09-30 t:2015-09-29
|2| (Z) 2015-11-06 Lorem ipsum dolorem sit amet. Red @fox +... due:2015-11-08 lazy:bar t:2015-11-07
|3| (C) 2015-07-12 Foo @Context2 Not@Context +Project1 Not+Project
|4| (C) Baz @Context1 +Project1 key:value
|5| Drink beer @ home ical:foobar id:1 p:2
|6| x 2014-12-12 Completed but with date:2014-12-12
"""
        self.assertEqual(self.output, result)

    @mock.patch('topydo.lib.ListFormat.get_terminal_size')
    def test_list_format04(self, mock_terminal_size):
        mock_terminal_size.return_value = self.terminal_size(100, 25)

        config(p_overrides={('ls', 'list_format'): '|%I| %x %{(}p{)} %c %S	%K'})
        command = ListCommand(["-x"], self.todolist, self.out, self.error)
        command.execute()

        result = """|1| (D) 2015-08-31 Bar @Context1 +Project2                              due:2015-09-30 t:2015-09-29
|2| (Z) 2015-11-06 Lorem ipsum dolorem sit amet. Red @fox +... due:2015-11-08 lazy:bar t:2015-11-07
|3| (C) 2015-07-12 Foo @Context2 Not@Context +Project1 Not+Project
|4| (C) Baz @Context1 +Project1                                                           key:value
|5| Drink beer @ home                                                          ical:foobar id:1 p:2
|6| x 2014-12-12 Completed but with                                                 date:2014-12-12
"""
        self.assertEqual(self.output, result)

    @mock.patch('topydo.lib.ListFormat.get_terminal_size')
    def test_list_format05(self, mock_terminal_size):
        mock_terminal_size.return_value = self.terminal_size(80, 25)

        config(p_overrides={('ls', 'list_format'): '|%I| %x %{(}p{)} %c %S	%K'})
        command = ListCommand(["-x"], self.todolist, self.out, self.error)
        command.execute()

        result = """|1| (D) 2015-08-31 Bar @Context1 +Project2          due:2015-09-30 t:2015-09-29
|2| (Z) 2015-11-06 Lorem ipsum dolorem ... due:2015-11-08 lazy:bar t:2015-11-07
|3| (C) 2015-07-12 Foo @Context2 Not@Context +Project1 Not+Project
|4| (C) Baz @Context1 +Project1                                       key:value
|5| Drink beer @ home                                      ical:foobar id:1 p:2
|6| x 2014-12-12 Completed but with                             date:2014-12-12
"""

        self.assertEqual(self.output, result)

    @mock.patch('arrow.now') # arrow.now() doesn't freeze at UTC
    @mock.patch('topydo.lib.ListFormat.get_terminal_size')
    def test_list_format06(self, mock_terminal_size, mock_arrow):
        mock_terminal_size.return_value = self.terminal_size(100, 25)
        mock_arrow.return_value = arrow.utcnow() # force arrow to UTC

        config(p_overrides={('ls', 'list_format'): '|%I| %x %p %S %k	%{(}H{)}'})
        command = ListCommand(["-x"], self.todolist, self.out, self.error)
        command.execute()

        result = """|1| D Bar @Context1 +Project2                  (3 months ago, due a month ago, started a month ago)
|2| Z Lorem ipsum dolorem sit amet. Red @fox +j... lazy:bar (today, due in 2 days, starts in a day)
|3| C Foo @Context2 Not@Context +Project1 Not+Project                                (4 months ago)
|4| C Baz @Context1 +Project1 key:value
|5| Drink beer @ home
|6| x 2014-12-12 Completed but with date:2014-12-12
"""
        self.assertEqual(self.output, result)

    @mock.patch('arrow.now')
    @mock.patch('topydo.lib.ListFormat.get_terminal_size')
    def test_list_format07(self, mock_terminal_size, mock_arrow):
        mock_terminal_size.return_value = self.terminal_size(100, 25)
        mock_arrow.return_value = arrow.utcnow()

        config(p_overrides={('ls', 'list_format'): '|%I| %x %p %S %k	%{(}h{)}'})
        command = ListCommand(["-x"], self.todolist, self.out, self.error)
        command.execute()

        result = """|1| D Bar @Context1 +Project2                                (due a month ago, started a month ago)
|2| Z Lorem ipsum dolorem sit amet. Red @fox +jumped o... lazy:bar (due in 2 days, starts in a day)
|3| C Foo @Context2 Not@Context +Project1 Not+Project
|4| C Baz @Context1 +Project1 key:value
|5| Drink beer @ home
|6| x 2014-12-12 Completed but with date:2014-12-12
"""
        self.assertEqual(self.output, result)

    @mock.patch('topydo.lib.ListFormat.get_terminal_size')
    def test_list_format08(self, mock_terminal_size):
        mock_terminal_size.return_value = self.terminal_size(100, 25)

        config(p_overrides={('ls', 'list_format'): '%c %d %t %x'})
        command = ListCommand(["-x"], self.todolist, self.out, self.error)
        command.execute()

        result = """2015-08-31 2015-09-30 2015-09-29
2015-11-06 2015-11-08 2015-11-07
2015-07-12


x 2014-12-12
"""
        self.assertEqual(self.output, result)

    @mock.patch('arrow.now')
    @mock.patch('topydo.lib.ListFormat.get_terminal_size')
    def test_list_format09(self, mock_terminal_size, mock_arrow):
        mock_terminal_size.return_value = self.terminal_size(100, 25)
        mock_arrow.return_value = arrow.utcnow()

        config(p_overrides={('ls', 'list_format'): '%C | %D | %T | %X'})
        command = ListCommand(["-x"], self.todolist, self.out, self.error)
        command.execute()

        result = """3 months ago | a month ago | a month ago |
today | in 2 days | in a day |
4 months ago | | |
| | |
| | |
| | | x 11 months ago
"""
        self.assertEqual(self.output, result)

    def test_list_format10(self):
        config(p_overrides={('ls', 'list_format'): '|%i| %k'})
        command = ListCommand(["-x"], self.todolist, self.out, self.error)
        command.execute()

        result = """|1|
|2| lazy:bar
|3|
|4| key:value
|5|
|6| date:2014-12-12
"""
        self.assertEqual(self.output, result)

    def test_list_format11(self):
        config(p_overrides={('ls', 'list_format'): '|%I| %K'})
        command = ListCommand(["-x"], self.todolist, self.out, self.error)
        command.execute()

        result = """|1| due:2015-09-30 t:2015-09-29
|2| due:2015-11-08 lazy:bar t:2015-11-07
|3|
|4| key:value
|5| ical:foobar id:1 p:2
|6| date:2014-12-12
"""
        self.assertEqual(self.output, result)

    def test_list_format12(self):
        config(p_overrides={('ls', 'list_format'): r'|%I| \%'})
        command = ListCommand(["-x"], self.todolist, self.out, self.error)
        command.execute()

        result = """|1| %
|2| %
|3| %
|4| %
|5| %
|6| %
"""
        self.assertEqual(self.output, result)

    def test_list_format13(self):
        command = ListCommand(["-x", "-F", "|%I| %x %{(}p{)} %c %s %K"],
                              self.todolist, self.out, self.error)
        command.execute()

        result = """|1| (D) 2015-08-31 Bar @Context1 +Project2 due:2015-09-30 t:2015-09-29
|2| (Z) 2015-11-06 Lorem ipsum dolorem sit amet. Red @fox +jumped over the and jar due:2015-11-08 lazy:bar t:2015-11-07
|3| (C) 2015-07-12 Foo @Context2 Not@Context +Project1 Not+Project
|4| (C) Baz @Context1 +Project1 key:value
|5| Drink beer @ home ical:foobar id:1 p:2
|6| x 2014-12-12 Completed but with date:2014-12-12
"""
        self.assertEqual(self.output, result)

    @mock.patch('topydo.lib.ListFormat.get_terminal_size')
    def test_list_format14(self, mock_terminal_size):
        mock_terminal_size.return_value = self.terminal_size(40, 25)
        command = ListCommand(["-x", "-F", "|%I| %x %{(}p{)} %c %s	%K", "@Context1"],
                              self.todolist, self.out, self.error)
        command.execute()

        result = """|1| (D) 2015-08-31 Bar @Context1 +Project2 due:2015-09-30 t:2015-09-29
|4| (C) Baz @Context1 +Project1 key:value
"""

        self.assertEqual(self.output, result)

    def test_list_format15(self):
        command = ListCommand(["-x", "-F", "%c"], self.todolist, self.out, self.error)
        command.execute()

        result = """2015-08-31
2015-11-06
2015-07-12



"""
        self.assertEqual(self.output, result)

    @mock.patch('arrow.now')
    def test_list_format16(self, mock_arrow):
        mock_arrow.return_value = arrow.utcnow()

        command = ListCommand(["-x", "-F", "%C"], self.todolist, self.out, self.error)
        command.execute()

        result = """3 months ago
today
4 months ago



"""
        self.assertEqual(self.output, result)

    def test_list_format17(self):
        command = ListCommand(["-x", "-F", "%d"], self.todolist, self.out, self.error)
        command.execute()

        result = """2015-09-30
2015-11-08




"""
        self.assertEqual(self.output, result)

    @mock.patch('arrow.now')
    def test_list_format18(self, mock_arrow):
        mock_arrow.return_value = arrow.utcnow()

        command = ListCommand(["-x", "-F", "%D"], self.todolist, self.out, self.error)
        command.execute()

        result = """a month ago
in 2 days




"""
        self.assertEqual(self.output, result)

    @mock.patch('arrow.now')
    def test_list_format19(self, mock_arrow):
        mock_arrow.return_value = arrow.utcnow()

        command = ListCommand(["-x", "-F", "%h"], self.todolist, self.out, self.error)
        command.execute()

        result = """due a month ago, started a month ago
due in 2 days, starts in a day




"""
        self.assertEqual(self.output, result)

    @mock.patch('arrow.now')
    def test_list_format20(self, mock_arrow):
        mock_arrow.return_value = arrow.utcnow()

        command = ListCommand(["-x", "-F", "%H"], self.todolist, self.out, self.error)
        command.execute()

        result = """3 months ago, due a month ago, started a month ago
today, due in 2 days, starts in a day
4 months ago



"""
        self.assertEqual(self.output, result)

    def test_list_format21(self):
        command = ListCommand(["-x", "-F", "%i"], self.todolist, self.out, self.error)
        command.execute()

        result = """1
2
3
4
5
6
"""
        self.assertEqual(self.output, result)

    def test_list_format22(self):
        command = ListCommand(["-x", "-F", "%I"], self.todolist, self.out, self.error)
        command.execute()

        result = """1
2
3
4
5
6
"""
        self.assertEqual(self.output, result)

    def test_list_format23(self):
        command = ListCommand(["-x", "-F", "%k"], self.todolist, self.out, self.error)
        command.execute()

        result = """
lazy:bar

key:value

date:2014-12-12
"""
        self.assertEqual(self.output, result)

    def test_list_format24(self):
        command = ListCommand(["-x", "-F", "%K"], self.todolist, self.out, self.error)
        command.execute()

        result = """due:2015-09-30 t:2015-09-29
due:2015-11-08 lazy:bar t:2015-11-07

key:value
ical:foobar id:1 p:2
date:2014-12-12
"""
        self.assertEqual(self.output, result)

    def test_list_format25(self):
        command = ListCommand(["-x", "-F", "%p"], self.todolist, self.out, self.error)
        command.execute()

        result = """D
Z
C
C


"""
        self.assertEqual(self.output, result)

    def test_list_format26(self):
        command = ListCommand(["-x", "-F", "%s"], self.todolist, self.out, self.error)
        command.execute()

        result = u"""Bar @Context1 +Project2
Lorem ipsum dolorem sit amet. Red @fox +jumped over the and jar
Foo @Context2 Not@Context +Project1 Not+Project
Baz @Context1 +Project1
Drink beer @ home
Completed but with
"""
        self.assertEqual(self.output, result)

    @mock.patch('topydo.lib.ListFormat.get_terminal_size')
    def test_list_format27(self, mock_terminal_size):
        mock_terminal_size.return_value = self.terminal_size(50, 25)

        command = ListCommand(["-x", "-F", "%S"], self.todolist, self.out, self.error)
        command.execute()

        result = """Bar @Context1 +Project2
Lorem ipsum dolorem sit amet. Red @fox +jumped...
Foo @Context2 Not@Context +Project1 Not+Project
Baz @Context1 +Project1
Drink beer @ home
Completed but with
"""
        self.assertEqual(self.output, result)

    def test_list_format28(self):
        command = ListCommand(["-x", "-F", "%t"], self.todolist, self.out, self.error)
        command.execute()

        result = """2015-09-29
2015-11-07




"""
        self.assertEqual(self.output, result)

    @mock.patch('arrow.now')
    def test_list_format29(self, mock_arrow):
        mock_arrow.return_value = arrow.utcnow()

        command = ListCommand(["-x", "-F", "%T"], self.todolist, self.out, self.error)
        command.execute()

        result = """a month ago
in a day




"""
        self.assertEqual(self.output, result)

    def test_list_format30(self):
        command = ListCommand(["-x", "-F", "%x"], self.todolist, self.out, self.error)
        command.execute()

        result = """




x 2014-12-12
"""
        self.assertEqual(self.output, result)

    def test_list_format31(self):
        command = ListCommand(["-x", "-F", "%X"], self.todolist, self.out, self.error)
        command.execute()

        result = """




x 11 months ago
"""
        self.assertEqual(self.output, result)

    def test_list_format32(self):
        command = ListCommand(["-x", "-s", "desc:priority", "-F", "%{{}p{}}"], self.todolist, self.out, self.error)
        command.execute()

        result = """{C}
{C}
{D}


{Z}
"""
        self.assertEqual(self.output, result)

    def test_list_format33(self):
        command = ListCommand(["-x", "-s", "desc:priority", "-F", r"%{\%p}p{\%p}"], self.todolist, self.out, self.error)
        command.execute()

        result = """%pC%p
%pC%p
%pD%p


%pZ%p
"""
        self.assertEqual(self.output, result)

    def test_list_format34(self):
        command = ListCommand(["-x", "-s", "desc:priority", "-F", "%p%p"], self.todolist, self.out, self.error)
        command.execute()

        result = """CC
CC
DD


ZZ
"""
        self.assertEqual(self.output, result)

    @mock.patch('topydo.lib.ListFormat.get_terminal_size')
    def test_list_format35(self, mock_terminal_size):
        mock_terminal_size.return_value = self.terminal_size(5, 25)
        command = ListCommand(["-x", "-s", "desc:priority", "-F", "%p{ }	%{ }p"], self.todolist, self.out, self.error)
        command.execute()

        result = """C  C
C  C
D  D


Z  Z
"""
        self.assertEqual(self.output, result)

    @mock.patch('topydo.lib.ListFormat.get_terminal_size')
    def test_list_format36(self, mock_terminal_size):
        """Tab expands to 1 character."""
        mock_terminal_size.return_value =  self.terminal_size(6, 25)
        command = ListCommand(["-x", "-s", "desc:priority", "-F", "%p{ }	%{ }p"], self.todolist, self.out, self.error)
        command.execute()

        result = """C   C
C   C
D   D


Z   Z
"""
        self.assertEqual(self.output, result)

    @mock.patch('topydo.lib.ListFormat.get_terminal_size')
    def test_list_format37(self, mock_terminal_size):
        mock_terminal_size.return_value = self.terminal_size(5, 25)
        command = ListCommand(["-x", "-s", "desc:priority", "-F", "	%{ }p"], self.todolist, self.out, self.error)
        command.execute()

        result = """   C
   C
   D


   Z
"""
        self.assertEqual(self.output, result)

    def test_list_format38(self):
        """
        Invalid placeholders should expand to an empty string.
        """
        command = ListCommand(["-x", "-s", "desc:priority", "-F", "%&"], self.todolist, self.out, self.error)
        command.execute()

        result = """





"""
        self.assertEqual(self.output, result)

    def test_list_format39(self):
        """
        Invalid placeholders without a character should expand to an empty
        string.
        """
        command = ListCommand(["-x", "-s", "desc:priority", "-F", "%"], self.todolist, self.out, self.error)
        command.execute()

        result = """





"""
        self.assertEqual(self.output, result)

    @mock.patch('topydo.lib.ListFormat.get_terminal_size')
    def test_list_format40(self, mock_terminal_size):
        mock_terminal_size.return_value = self.terminal_size(100, 25)

        config('test/data/listformat.conf')
        command = ListCommand(["-x"], self.todolist, self.out, self.error)
        command.execute()

        result = """|1| (D) 2015-08-31 Bar @Context1 +Project2                              due:2015-09-30 t:2015-09-29
|2| (Z) 2015-11-06 Lorem ipsum dolorem sit amet. Red @fox +... due:2015-11-08 lazy:bar t:2015-11-07
|3| (C) 2015-07-12 Foo @Context2 Not@Context +Project1 Not+Project
|4| (C) Baz @Context1 +Project1                                                           key:value
|5| Drink beer @ home                                                          ical:foobar id:1 p:2
|6| x 2014-12-12 Completed but with                                                 date:2014-12-12
"""
        self.assertEqual(self.output, result)

    @mock.patch('topydo.lib.ListFormat.get_terminal_size')
    def test_list_format41(self, mock_terminal_size):
        mock_terminal_size.return_value = self.terminal_size(100, 25)

        command = ListCommand(["-x", "-F", "|%I| %x %{(}p{)} %c %S\\t%K"], self.todolist, self.out, self.error)
        command.execute()

        result = """|1| (D) 2015-08-31 Bar @Context1 +Project2                              due:2015-09-30 t:2015-09-29
|2| (Z) 2015-11-06 Lorem ipsum dolorem sit amet. Red @fox +... due:2015-11-08 lazy:bar t:2015-11-07
|3| (C) 2015-07-12 Foo @Context2 Not@Context +Project1 Not+Project
|4| (C) Baz @Context1 +Project1                                                           key:value
|5| Drink beer @ home                                                          ical:foobar id:1 p:2
|6| x 2014-12-12 Completed but with                                                 date:2014-12-12
"""
        self.assertEqual(self.output, result)

    @mock.patch('topydo.lib.ListFormat.get_terminal_size')
    def test_list_format42(self, mock_terminal_size):
        mock_terminal_size.return_value = self.terminal_size(100, 25)

        config('test/data/listformat.conf', p_overrides={('ls', 'indent'): '3'})
        command = ListCommand(["-x"], self.todolist, self.out, self.error)
        command.execute()

        result = """   |1| (D) 2015-08-31 Bar @Context1 +Project2                           due:2015-09-30 t:2015-09-29
   |2| (Z) 2015-11-06 Lorem ipsum dolorem sit amet. Red @fo... due:2015-11-08 lazy:bar t:2015-11-07
   |3| (C) 2015-07-12 Foo @Context2 Not@Context +Project1 Not+Project
   |4| (C) Baz @Context1 +Project1                                                        key:value
   |5| Drink beer @ home                                                       ical:foobar id:1 p:2
   |6| x 2014-12-12 Completed but with                                              date:2014-12-12
"""
        self.assertEqual(self.output, result)

    def test_list_format43(self):
        command = ListCommand(["-x", "-F", "%P -"], self.todolist, self.out, self.error)
        command.execute()

        result = """D -
Z -
C -
C -
  -
  -
"""
        self.assertEqual(self.output, result)

    def test_list_format44(self):
        command = ListCommand(["-x", "-F", "%i %{(}P{)}"], self.todolist, self.out, self.error)
        command.execute()

        result = """1 (D)
2 (Z)
3 (C)
4 (C)
5 ( )
6 ( )
"""
        self.assertEqual(self.output, result)

    @mock.patch('arrow.now')
    @mock.patch('topydo.lib.ListFormat.get_terminal_size')
    def test_list_format45(self, mock_terminal_size, mock_arrow):
        """ Colorblocks should not affect truncating or right_alignment. """
        mock_terminal_size.return_value = self.terminal_size(100, 25)
        mock_arrow.return_value = arrow.utcnow()

        config(p_overrides={('ls', 'list_format'): '%z|%I| %x %p %S %k\\t%{(}h{)}'})
        command = ListCommand(["-x"], self.todolist, self.out, self.error)
        command.execute()

        result = u""" |1| D Bar @Context1 +Project2                               (due a month ago, started a month ago)
 |2| Z Lorem ipsum dolorem sit amet. Red @fox +jumped ... lazy:bar (due in 2 days, starts in a day)
 |3| C Foo @Context2 Not@Context +Project1 Not+Project
 |4| C Baz @Context1 +Project1 key:value
 |5| Drink beer @ home
 |6| x 2014-12-12 Completed but with date:2014-12-12
"""
        self.assertEqual(self.output, result)

    def test_list_format46(self):
        command = ListCommand(["-x", "-F", "%r"], self.todolist, self.out, self.error)
        command.execute()

        result = """(D) 2015-08-31 Bar @Context1 +Project2 due:2015-09-30 t:2015-09-29
(Z) 2015-11-06 Lorem ipsum dolorem sit amet. Red @fox +jumped over the lazy:bar and jar due:2015-11-08 t:2015-11-07
(C) 2015-07-12 Foo @Context2 Not@Context +Project1 Not+Project
(C) Baz @Context1 +Project1 key:value
Drink beer @ home id:1 p:2 ical:foobar
x 2014-12-12 Completed but with date:2014-12-12
"""
        self.assertEqual(self.output, result)

    def test_list_format47(self):
        command = ListCommand(["-x", "-F", "%(r)"], self.todolist, self.out, self.error)
        command.execute()

        error = 'Error while parsing format string (list_format config option or -F)\n'
        self.assertEqual(self.output, '')
        self.assertEqual(self.errors, error)

    def test_list_format48(self):
        """
        Test line numbers
        """
        command = ListCommand(["-F %n"], self.todolist, self.out, self.error)
        command.execute()

        result = """ 1
 3
 4
 5
"""
        self.assertEqual(self.output, result)
        self.assertEqual(self.errors, "")

    def test_list_format50(self):
        """
        Test line numbers
        """
        command = ListCommand(["-F %u"], self.todolist, self.out, self.error)
        command.execute()

        result = """ mfg
 t5c
 n8m
 wa5
"""
        self.assertEqual(self.output, result)
        self.assertEqual(self.errors, "")

    def test_list_format51(self):
        """
        Test padded identifiers
        """
        command = ListCommand(["-F %U"], self.todolist, self.out, self.error)
        command.execute()

        result = """ mfg
 t5c
 n8m
 wa5
"""
        self.assertEqual(self.output, result)
        self.assertEqual(self.errors, "")

    def test_list_format52(self):
        config(p_overrides={('topydo', 'identifier_alphabet'): '0123456789abcdef', ('topydo', 'identifiers'): 'text'})

        # make sure that it fallbacks to the default alphabet
        todolist = TodoListBase([str(i) for i in range(0, 100 * 16 * 10)])
        self.assertEqual(4, todolist.max_id_length())

if __name__ == '__main__':
    unittest.main()
