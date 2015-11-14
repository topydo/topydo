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

from collections import namedtuple
from freezegun import freeze_time

from test.command_testcase import CommandTest
from test.facilities import load_file_to_todolist
from topydo.commands.ListCommand import ListCommand
from topydo.lib.Config import config

# We're searching for 'mock'
# pylint: disable=no-name-in-module
try:
    from unittest import mock
except ImportError:
    import mock

@freeze_time("2015, 11, 06")
class ListFormatTest(CommandTest):
    def setUp(self):
        super(ListFormatTest, self).setUp()
        self.todolist = load_file_to_todolist("test/data/ListFormat.txt")
        self.terminal_size = namedtuple('terminal_size', ['columns', 'lines'])

    def test_list_format01(self):
        config(p_overrides={('ls', 'list_format'): '|%I| %x %{(}p{)} %c %s %K'})
        command = ListCommand(["-x"], self.todolist, self.out, self.error)
        command.execute()

        result = u"""|  1| (D) 2015-08-31 Bar @Context1 +Project2 due:2015-09-30 t:2015-09-29
|  2| (Z) 2015-11-06 Lorem ipsum dolorem sit amet. Red @fox +jumped over the and jar due:2015-11-08 lazy:bar t:2015-11-07
|  3| (C) 2015-07-12 Foo @Context2 Not@Context +Project1 Not+Project
|  4| (C) Baz @Context1 +Project1 key:value
|  5| Drink beer @ home ical:foobar id:1 p:2
|  6| x 2014-12-12 Completed but with date:2014-12-12
"""
        self.assertEqual(self.output, result)

    @mock.patch('topydo.lib.ListFormat.get_terminal_size')
    def test_list_format02(self, mock_terminal_size):
        mock_terminal_size.return_value = self.terminal_size(80, 25)

        config(p_overrides={('ls', 'list_format'): '|%I| %x %{(}p{)} %c %S %K'})
        command = ListCommand(["-x"], self.todolist, self.out, self.error)
        command.execute()

        result = u"""|  1| (D) 2015-08-31 Bar @Context1 +Project2 due:2015-09-30 t:2015-09-29
|  2| (Z) 2015-11-06 Lorem ipsum dolore... due:2015-11-08 lazy:bar t:2015-11-07
|  3| (C) 2015-07-12 Foo @Context2 Not@Context +Project1 Not+Project
|  4| (C) Baz @Context1 +Project1 key:value
|  5| Drink beer @ home ical:foobar id:1 p:2
|  6| x 2014-12-12 Completed but with date:2014-12-12
"""
        self.assertEqual(self.output, result)

    @mock.patch('topydo.lib.ListFormat.get_terminal_size')
    def test_list_format03(self, mock_terminal_size):
        mock_terminal_size.return_value = self.terminal_size(100, 25)

        config(p_overrides={('ls', 'list_format'): '|%I| %x %{(}p{)} %c %S %K'})
        command = ListCommand(["-x"], self.todolist, self.out, self.error)
        command.execute()

        result = u"""|  1| (D) 2015-08-31 Bar @Context1 +Project2 due:2015-09-30 t:2015-09-29
|  2| (Z) 2015-11-06 Lorem ipsum dolorem sit amet. Red @fox... due:2015-11-08 lazy:bar t:2015-11-07
|  3| (C) 2015-07-12 Foo @Context2 Not@Context +Project1 Not+Project
|  4| (C) Baz @Context1 +Project1 key:value
|  5| Drink beer @ home ical:foobar id:1 p:2
|  6| x 2014-12-12 Completed but with date:2014-12-12
"""
        self.assertEqual(self.output, result)

    @mock.patch('topydo.lib.ListFormat.get_terminal_size')
    def test_list_format04(self, mock_terminal_size):
        mock_terminal_size.return_value = self.terminal_size(100, 25)

        config(p_overrides={('ls', 'list_format'): '|%I| %x %{(}p{)} %c %S	%K'})
        command = ListCommand(["-x"], self.todolist, self.out, self.error)
        command.execute()

        result = u"""|  1| (D) 2015-08-31 Bar @Context1 +Project2                            due:2015-09-30 t:2015-09-29
|  2| (Z) 2015-11-06 Lorem ipsum dolorem sit amet. Red @fox... due:2015-11-08 lazy:bar t:2015-11-07
|  3| (C) 2015-07-12 Foo @Context2 Not@Context +Project1 Not+Project
|  4| (C) Baz @Context1 +Project1                                                         key:value
|  5| Drink beer @ home                                                        ical:foobar id:1 p:2
|  6| x 2014-12-12 Completed but with                                               date:2014-12-12
"""
        self.assertEqual(self.output, result)

    @mock.patch('topydo.lib.ListFormat.get_terminal_size')
    def test_list_format05(self, mock_terminal_size):
        mock_terminal_size.return_value = self.terminal_size(80, 25)

        config(p_overrides={('ls', 'list_format'): '|%I| %x %{(}p{)} %c %S	%K'})
        command = ListCommand(["-x"], self.todolist, self.out, self.error)
        command.execute()

        result = u"""|  1| (D) 2015-08-31 Bar @Context1 +Project2        due:2015-09-30 t:2015-09-29
|  2| (Z) 2015-11-06 Lorem ipsum dolore... due:2015-11-08 lazy:bar t:2015-11-07
|  3| (C) 2015-07-12 Foo @Context2 Not@Context +Project1 Not+Project
|  4| (C) Baz @Context1 +Project1                                     key:value
|  5| Drink beer @ home                                    ical:foobar id:1 p:2
|  6| x 2014-12-12 Completed but with                           date:2014-12-12
"""

    @mock.patch('topydo.lib.ListFormat.get_terminal_size')
    def test_list_format06(self, mock_terminal_size):
        mock_terminal_size.return_value = self.terminal_size(100, 25)

        config(p_overrides={('ls', 'list_format'): '|%I| %x %p %S %k	%{(}H{)}'})
        command = ListCommand(["-x"], self.todolist, self.out, self.error)
        command.execute()

        result = u"""|  1| D Bar @Context1 +Project2                (3 months ago, due a month ago, started a month ago)
|  2| Z Lorem ipsum dolorem sit amet. Red @f... lazy:bar (just now, due in 2 days, starts in a day)
|  3| C Foo @Context2 Not@Context +Project1 Not+Project                              (4 months ago)
|  4| C Baz @Context1 +Project1 key:value
|  5| Drink beer @ home
|  6| x 2014-12-12 Completed but with date:2014-12-12
"""
        self.assertEqual(self.output, result)

    @mock.patch('topydo.lib.ListFormat.get_terminal_size')
    def test_list_format07(self, mock_terminal_size):
        mock_terminal_size.return_value = self.terminal_size(100, 25)

        config(p_overrides={('ls', 'list_format'): '|%I| %x %p %S %k	%{(}h{)}'})
        command = ListCommand(["-x"], self.todolist, self.out, self.error)
        command.execute()

        result = u"""|  1| D Bar @Context1 +Project2                              (due a month ago, started a month ago)
|  2| Z Lorem ipsum dolorem sit amet. Red @fox +jumped... lazy:bar (due in 2 days, starts in a day)
|  3| C Foo @Context2 Not@Context +Project1 Not+Project
|  4| C Baz @Context1 +Project1 key:value
|  5| Drink beer @ home
|  6| x 2014-12-12 Completed but with date:2014-12-12
"""
        self.assertEqual(self.output, result)

    @mock.patch('topydo.lib.ListFormat.get_terminal_size')
    def test_list_format08(self, mock_terminal_size):
        mock_terminal_size.return_value = self.terminal_size(100, 25)

        config(p_overrides={('ls', 'list_format'): '%c %d %t %x'})
        command = ListCommand(["-x"], self.todolist, self.out, self.error)
        command.execute()

        result = u"""2015-08-31 2015-09-30 2015-09-29
2015-11-06 2015-11-08 2015-11-07
2015-07-12


x 2014-12-12
"""
        self.assertEqual(self.output, result)

    @mock.patch('topydo.lib.ListFormat.get_terminal_size')
    def test_list_format09(self, mock_terminal_size):
        mock_terminal_size.return_value = self.terminal_size(100, 25)

        config(p_overrides={('ls', 'list_format'): '%C | %D | %T | %X'})
        command = ListCommand(["-x"], self.todolist, self.out, self.error)
        command.execute()

        result = u"""3 months ago | a month ago | a month ago |
just now | in 2 days | in a day |
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

        result = u"""|1|
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

        result = u"""|  1| due:2015-09-30 t:2015-09-29
|  2| due:2015-11-08 lazy:bar t:2015-11-07
|  3|
|  4| key:value
|  5| ical:foobar id:1 p:2
|  6| date:2014-12-12
"""
        self.assertEqual(self.output, result)

    def test_list_format12(self):
        config(p_overrides={('ls', 'list_format'): '|%I| \%'})
        command = ListCommand(["-x"], self.todolist, self.out, self.error)
        command.execute()

        result = u"""|  1| %
|  2| %
|  3| %
|  4| %
|  5| %
|  6| %
"""
        self.assertEqual(self.output, result)

    def test_list_format13(self):
        command = ListCommand(["-x", "-F", "|%I| %x %{(}p{)} %c %s %K"],
                              self.todolist, self.out, self.error)
        command.execute()

        result = u"""|  1| (D) 2015-08-31 Bar @Context1 +Project2 due:2015-09-30 t:2015-09-29
|  2| (Z) 2015-11-06 Lorem ipsum dolorem sit amet. Red @fox +jumped over the and jar due:2015-11-08 lazy:bar t:2015-11-07
|  3| (C) 2015-07-12 Foo @Context2 Not@Context +Project1 Not+Project
|  4| (C) Baz @Context1 +Project1 key:value
|  5| Drink beer @ home ical:foobar id:1 p:2
|  6| x 2014-12-12 Completed but with date:2014-12-12
"""
        self.assertEqual(self.output, result)

    @mock.patch('topydo.lib.ListFormat.get_terminal_size')
    def test_list_format14(self, mock_terminal_size):
        mock_terminal_size.return_value = self.terminal_size(40, 25)
        command = ListCommand(["-x", "-F", "|%I| %x %{(}p{)} %c %s	%K", "@Context1"],
                              self.todolist, self.out, self.error)
        command.execute()

        result = u"""|  1| (D) 2015-08-31 Bar @Context1 +Project2 due:2015-09-30 t:2015-09-29
|  4| (C) Baz @Context1 +Project1 key:value
"""

        self.assertEqual(self.output, result)

    def test_list_format15(self):
        command = ListCommand(["-x", "-F", "%c"], self.todolist, self.out, self.error)
        command.execute()

        result = u"""2015-08-31
2015-11-06
2015-07-12



"""
        self.assertEqual(self.output, result)

    def test_list_format16(self):
        command = ListCommand(["-x", "-F", "%C"], self.todolist, self.out, self.error)
        command.execute()

        result = u"""3 months ago
just now
4 months ago



"""
        self.assertEqual(self.output, result)

    def test_list_format17(self):
        command = ListCommand(["-x", "-F", "%d"], self.todolist, self.out, self.error)
        command.execute()

        result = u"""2015-09-30
2015-11-08




"""
        self.assertEqual(self.output, result)

    def test_list_format18(self):
        command = ListCommand(["-x", "-F", "%D"], self.todolist, self.out, self.error)
        command.execute()

        result = u"""a month ago
in 2 days




"""
        self.assertEqual(self.output, result)

    def test_list_format19(self):
        command = ListCommand(["-x", "-F", "%h"], self.todolist, self.out, self.error)
        command.execute()

        result = u"""due a month ago, started a month ago
due in 2 days, starts in a day




"""
        self.assertEqual(self.output, result)

    def test_list_format20(self):
        command = ListCommand(["-x", "-F", "%H"], self.todolist, self.out, self.error)
        command.execute()

        result = u"""3 months ago, due a month ago, started a month ago
just now, due in 2 days, starts in a day
4 months ago



"""
        self.assertEqual(self.output, result)

    def test_list_format21(self):
        command = ListCommand(["-x", "-F", "%i"], self.todolist, self.out, self.error)
        command.execute()

        result = u"""1
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

        result = u"""  1
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

        result = u"""
lazy:bar

key:value

date:2014-12-12
"""
        self.assertEqual(self.output, result)

    def test_list_format24(self):
        command = ListCommand(["-x", "-F", "%K"], self.todolist, self.out, self.error)
        command.execute()

        result = u"""due:2015-09-30 t:2015-09-29
due:2015-11-08 lazy:bar t:2015-11-07

key:value
ical:foobar id:1 p:2
date:2014-12-12
"""
        self.assertEqual(self.output, result)

    def test_list_format25(self):
        command = ListCommand(["-x", "-F", "%p"], self.todolist, self.out, self.error)
        command.execute()

        result = u"""D
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

        result = u"""Bar @Context1 +Project2
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

        result = u"""2015-09-29
2015-11-07




"""
        self.assertEqual(self.output, result)

    def test_list_format29(self):
        command = ListCommand(["-x", "-F", "%T"], self.todolist, self.out, self.error)
        command.execute()

        result = u"""a month ago
in a day




"""
        self.assertEqual(self.output, result)

    def test_list_format30(self):
        command = ListCommand(["-x", "-F", "%x"], self.todolist, self.out, self.error)
        command.execute()

        result = u"""




x 2014-12-12
"""
        self.assertEqual(self.output, result)

    def test_list_format31(self):
        command = ListCommand(["-x", "-F", "%X"], self.todolist, self.out, self.error)
        command.execute()

        result = u"""




x 11 months ago
"""
        self.assertEqual(self.output, result)

    def test_list_format32(self):
        command = ListCommand(["-x", "-s", "desc:priority", "-F", "%{{}p{}}"], self.todolist, self.out, self.error)
        command.execute()

        result = u"""{C}
{C}
{D}
{Z}


"""
        self.assertEqual(self.output, result)

    def test_list_format33(self):
        command = ListCommand(["-x", "-s", "desc:priority", "-F", "%{\%p}p{\%p}"], self.todolist, self.out, self.error)
        command.execute()

        result = u"""%pC%p
%pC%p
%pD%p
%pZ%p


"""
        self.assertEqual(self.output, result)

    def test_list_format34(self):
        command = ListCommand(["-x", "-s", "desc:priority", "-F", "%p%p"], self.todolist, self.out, self.error)
        command.execute()

        result = u"""CC
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

        result = u"""C  C
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

        result = u"""C   C
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

        result = u"""   C
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

        result = u"""





"""
        self.assertEqual(self.output, result)

    def test_list_format39(self):
        """
        Invalid placeholders without a character should expand to an empty
        string.
        """
        command = ListCommand(["-x", "-s", "desc:priority", "-F", "%"], self.todolist, self.out, self.error)
        command.execute()

        result = u"""





"""
        self.assertEqual(self.output, result)

    @mock.patch('topydo.lib.ListFormat.get_terminal_size')
    def test_list_format40(self, mock_terminal_size):
        mock_terminal_size.return_value = self.terminal_size(100, 25)

        config('test/data/listformat.conf')
        command = ListCommand(["-x"], self.todolist, self.out, self.error)
        command.execute()

        result = u"""|  1| (D) 2015-08-31 Bar @Context1 +Project2                            due:2015-09-30 t:2015-09-29
|  2| (Z) 2015-11-06 Lorem ipsum dolorem sit amet. Red @fox... due:2015-11-08 lazy:bar t:2015-11-07
|  3| (C) 2015-07-12 Foo @Context2 Not@Context +Project1 Not+Project
|  4| (C) Baz @Context1 +Project1                                                         key:value
|  5| Drink beer @ home                                                        ical:foobar id:1 p:2
|  6| x 2014-12-12 Completed but with                                               date:2014-12-12
"""
        self.assertEqual(self.output, result)

    @mock.patch('topydo.lib.ListFormat.get_terminal_size')
    def test_list_format41(self, mock_terminal_size):
        mock_terminal_size.return_value = self.terminal_size(100, 25)

        command = ListCommand(["-x", "-F", "|%I| %x %{(}p{)} %c %S\\t%K"], self.todolist, self.out, self.error)
        command.execute()

        result = u"""|  1| (D) 2015-08-31 Bar @Context1 +Project2                            due:2015-09-30 t:2015-09-29
|  2| (Z) 2015-11-06 Lorem ipsum dolorem sit amet. Red @fox... due:2015-11-08 lazy:bar t:2015-11-07
|  3| (C) 2015-07-12 Foo @Context2 Not@Context +Project1 Not+Project
|  4| (C) Baz @Context1 +Project1                                                         key:value
|  5| Drink beer @ home                                                        ical:foobar id:1 p:2
|  6| x 2014-12-12 Completed but with                                               date:2014-12-12
"""
        self.assertEqual(self.output, result)

    @mock.patch('topydo.lib.ListFormat.get_terminal_size')
    def test_list_format42(self, mock_terminal_size):
        mock_terminal_size.return_value = self.terminal_size(100, 25)

        config('test/data/listformat.conf', p_overrides={('ls', 'indent'): '3'})
        command = ListCommand(["-x"], self.todolist, self.out, self.error)
        command.execute()

        result = u"""   |  1| (D) 2015-08-31 Bar @Context1 +Project2                         due:2015-09-30 t:2015-09-29
   |  2| (Z) 2015-11-06 Lorem ipsum dolorem sit amet. Red @... due:2015-11-08 lazy:bar t:2015-11-07
   |  3| (C) 2015-07-12 Foo @Context2 Not@Context +Project1 Not+Project
   |  4| (C) Baz @Context1 +Project1                                                      key:value
   |  5| Drink beer @ home                                                     ical:foobar id:1 p:2
   |  6| x 2014-12-12 Completed but with                                            date:2014-12-12
"""
        self.assertEqual(self.output, result)

if __name__ == '__main__':
    unittest.main()
