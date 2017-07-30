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

from topydo.lib.Utils import translate_key_to_config

from .topydo_testcase import TopydoTest


class UtilsTest(TopydoTest):
    def test_key_to_cfg(self):
        ctrl_s = translate_key_to_config('ctrl s')
        meta_d = translate_key_to_config('meta d')
        esc = translate_key_to_config('esc')
        f4 = translate_key_to_config('f4')

        self.assertEqual(ctrl_s, '<C-s>')
        self.assertEqual(meta_d, '<M-d>')
        self.assertEqual(esc, '<Esc>')
        self.assertEqual(f4, '<F4>')

if __name__ == '__main__':
    unittest.main()
