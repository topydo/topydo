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

from test.topydo_testcase import TopydoTest
from topydo.lib.PrettyPrinterFilter import PrettyPrinterBasicPriorityFilter


class TestPrettyPrinterFilter(TopydoTest):
    def test_basicpriority01(self):
        """ Neither id or priority match. """
        in__todo = "nothing here"
        out_todo = "  nothing here"
        pp = PrettyPrinterBasicPriorityFilter()
        self.assertEqual(pp.filter(in__todo, None), out_todo)

    def test_basicpriority02(self):
        """ Id doesn't match, but priority does. """
        in__todo = "(B) something important"
        out_todo = "B something important"
        pp = PrettyPrinterBasicPriorityFilter()
        self.assertEqual(pp.filter(in__todo, None), out_todo)

    def test_basicpriority03(self):
        """ (Number) Id matches, but priority doesn't. """
        in__todo = "| 45| do me sometime..."
        out_todo = "| 45|   do me sometime..."
        pp = PrettyPrinterBasicPriorityFilter()
        self.assertEqual(pp.filter(in__todo, None), out_todo)

    def test_basicpriority04(self):
        """ (Hash) Id matches, but priority doesn't. """
        in__todo = "|b4v| more stuff needs done"
        out_todo = "|b4v|   more stuff needs done"
        pp = PrettyPrinterBasicPriorityFilter()
        self.assertEqual(pp.filter(in__todo, None), out_todo)

    def test_basicpriority05(self):
        """ Both id (number) and priority match. """
        in__todo = "|873| (G) important thing"
        out_todo = "|873| G important thing"
        pp = PrettyPrinterBasicPriorityFilter()
        self.assertEqual(pp.filter(in__todo, None), out_todo)

    def test_basicpriority06(self):
        """ Both id (hash) and priority match. """
        in__todo = "|jv9| (P) what is a P priority anyway?"
        out_todo = "|jv9| P what is a P priority anyway?"
        pp = PrettyPrinterBasicPriorityFilter()
        self.assertEqual(pp.filter(in__todo, None), out_todo)

if __name__ == "__main__":
    unittest.main()
