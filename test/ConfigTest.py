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
from test.TopydoTest import TopydoTest

class ConfigTest(TopydoTest):
    def test_config1(self):
        self.assertEquals(config("test/data/config1").default_command(), 'do')

    def test_config2(self):
        self.assertNotEquals(config("").default_command(), 'do')

    def test_config3(self):
        self.assertTrue(config("test/data/config2").ignore_weekends())

if __name__ == '__main__':
    unittest.main()
