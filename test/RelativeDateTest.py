from datetime import date, timedelta
import unittest

import RelativeDate

class RelativeDateTester(unittest.TestCase):
    def setUp(self):
        self.today = date.today()
        self.tomorrow = self.today + timedelta(1)

        self.monday = self.today
        if self.monday.weekday() != 0:
            self.monday += timedelta(7 - self.today.weekday() % 7)

    def test_zero_days(self):
        result = RelativeDate.relative_date_to_date('0d')
        self.assertEquals(result, self.today)

    def test_one_day(self):
        result = RelativeDate.relative_date_to_date('1d')
        self.assertEquals(result, self.tomorrow)

    def test_one_week(self):
        result = RelativeDate.relative_date_to_date('1w')
        self.assertEquals(result, date.today() + timedelta(weeks=1))

    def test_one_month(self):
        result = RelativeDate.relative_date_to_date('1m')
        self.assertEquals(result, date.today() + timedelta(30))

    def test_one_year(self):
        result = RelativeDate.relative_date_to_date('1y')
        self.assertEquals(result, date.today() + timedelta(365))

    def test_zero_months(self):
        result = RelativeDate.relative_date_to_date('0m')
        self.assertEquals(result, self.today)

    def test_zero_years(self):
        result = RelativeDate.relative_date_to_date('0y')
        self.assertEquals(result, self.today)

    def test_garbage1(self):
        result = RelativeDate.relative_date_to_date('0dd')
        self.assertFalse(result)

    def test_garbage2(self):
        result = RelativeDate.relative_date_to_date('-0d')
        self.assertFalse(result)

    def test_one_day_capital(self):
        result = RelativeDate.relative_date_to_date('1D')
        self.assertEquals(result, self.tomorrow)

    def test_today1(self):
        result = RelativeDate.relative_date_to_date('today')
        self.assertEquals(result, self.today)

    def test_today2(self):
        result = RelativeDate.relative_date_to_date('tod')
        self.assertEquals(result, self.today)

    def test_today3(self):
        result = RelativeDate.relative_date_to_date('today', \
            date.today() + timedelta(1))
        self.assertEquals(result, self.today)

    def test_tomorrow1(self):
        result = RelativeDate.relative_date_to_date('Tomorrow')
        self.assertEquals(result, self.tomorrow)

    def test_tomorrow2(self):
        result = RelativeDate.relative_date_to_date('tom')
        self.assertEquals(result, self.tomorrow)

    def test_monday1(self):
        result = RelativeDate.relative_date_to_date('monday')
        self.assertEquals(result, self.monday)

    def test_monday2(self):
        result = RelativeDate.relative_date_to_date('mo')
        self.assertEquals(result, self.monday)

    def test_monday3(self):
        result = RelativeDate.relative_date_to_date('mon')
        self.assertEquals(result, self.monday)

    def test_monday4(self):
        result = RelativeDate.relative_date_to_date('mondayy')
        self.assertFalse(result)

    def test_offset1(self):
        result = RelativeDate.relative_date_to_date('1d', self.tomorrow)
        self.assertEquals(result, date.today() + timedelta(2))
