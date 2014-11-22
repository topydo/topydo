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

from datetime import date, timedelta
import unittest

from topydo.lib.RelativeDate import relative_date_to_date

class RelativeDateTester(unittest.TestCase):
    def setUp(self):
        self.today = date.today()
        self.tomorrow = self.today + timedelta(1)

        self.monday = self.today
        if self.monday.weekday() != 0:
            self.monday += timedelta(7 - self.today.weekday() % 7)

    def test_zero_days(self):
        result = relative_date_to_date('0d')
        self.assertEquals(result, self.today)

    def test_one_day(self):
        result = relative_date_to_date('1d')
        self.assertEquals(result, self.tomorrow)

    def test_one_week(self):
        result = relative_date_to_date('1w')
        self.assertEquals(result, date.today() + timedelta(weeks=1))

    def test_one_month(self):
        result = relative_date_to_date('1m')
        self.assertEquals(result, date.today() + timedelta(30))

    def test_one_year(self):
        result = relative_date_to_date('1y')
        self.assertEquals(result, date.today() + timedelta(365))

    def test_zero_months(self):
        result = relative_date_to_date('0m')
        self.assertEquals(result, self.today)

    def test_zero_years(self):
        result = relative_date_to_date('0y')
        self.assertEquals(result, self.today)

    def test_garbage1(self):
        result = relative_date_to_date('0dd')
        self.assertFalse(result)

    def test_garbage2(self):
        result = relative_date_to_date('-0d')
        self.assertFalse(result)

    def test_one_day_capital(self):
        result = relative_date_to_date('1D')
        self.assertEquals(result, self.tomorrow)

    def test_today1(self):
        result = relative_date_to_date('today')
        self.assertEquals(result, self.today)

    def test_today2(self):
        result = relative_date_to_date('tod')
        self.assertEquals(result, self.today)

    def test_today3(self):
        result = relative_date_to_date('today', \
            date.today() + timedelta(1))
        self.assertEquals(result, self.today)

    def test_tomorrow1(self):
        result = relative_date_to_date('Tomorrow')
        self.assertEquals(result, self.tomorrow)

    def test_tomorrow2(self):
        result = relative_date_to_date('tom')
        self.assertEquals(result, self.tomorrow)

    def test_monday1(self):
        result = relative_date_to_date('monday')
        self.assertEquals(result, self.monday)

    def test_monday2(self):
        result = relative_date_to_date('mo')
        self.assertEquals(result, self.monday)

    def test_monday3(self):
        result = relative_date_to_date('mon')
        self.assertEquals(result, self.monday)

    def test_monday4(self):
        result = relative_date_to_date('mondayy')
        self.assertFalse(result)

    def test_offset1(self):
        result = relative_date_to_date('1d', self.tomorrow)
        self.assertEquals(result, date.today() + timedelta(2))
