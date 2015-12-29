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
from unittest import skip

from test.topydo_testcase import TopydoTest
from topydo.lib.Config import config


class ConfigTest(TopydoTest):
    def test_config01(self):
        self.assertEqual(config("test/data/ConfigTest1.conf").default_command(), 'do')

    def test_config02(self):
        self.assertNotEqual(config("").default_command(), 'do')

    def test_config03(self):
        self.assertTrue(config("test/data/ConfigTest2.conf").ignore_weekends())

    def test_config04(self):
        """ Test that value in file is overridden by parameter. """
        overrides = {
            ('topydo', 'default_command'): 'edit'
        }

        self.assertEqual(config("test/data/ConfigTest1.conf",
                                p_overrides=overrides).default_command(),
                         'edit')

    def test_config05(self):
        """ Bad colour switch value. """
        # boolean settings must first be typecast to integers, because all
        #  strings evaulate to 'True'
        self.assertEqual(config("test/data/ConfigTest4.conf").colors(),
                         bool(int(config().defaults["topydo"]["colors"])))

    def test_config06(self):
        """ Bad auto creation date switch value. """
        self.assertEqual(config("test/data/ConfigTest4.conf").auto_creation_date(),
                         bool(int(config().defaults["add"]["auto_creation_date"])))

    def test_config07(self):
        """ Bad indent value. """
        self.assertEqual(config("test/data/ConfigTest4.conf").list_indent(),
                         int(config().defaults["ls"]["indent"]))

    def test_config08(self):
        """ Bad list limit value. """
        self.assertEqual(config("test/data/ConfigTest4.conf").list_limit(),
                         int(config().defaults["ls"]["list_limit"]))

    def test_config10(self):
        """ Bad keep sorted switch value. """
        self.assertEqual(config("test/data/ConfigTest4.conf").keep_sorted(),
                         bool(int(config().defaults["sort"]["keep_sorted"])))

    def test_config11(self):
        """ Bad ignore weekends switch value. """
        self.assertEqual(config("test/data/ConfigTest4.conf").ignore_weekends(),
                         bool(int(config().defaults["sort"]["ignore_weekends"])))

    def test_config12(self):
        """ Bad append parent projects switch value. """
        self.assertEqual(config("test/data/ConfigTest4.conf").append_parent_projects(),
                         bool(int(config().defaults["dep"]["append_parent_projects"])))

    def test_config13(self):
        """ Bad append parent project contexts switch value. """
        self.assertEqual(config("test/data/ConfigTest4.conf").append_parent_contexts(),
                         bool(int(config().defaults["dep"]["append_parent_contexts"])))

    @skip("Error checking not yet implemented")
    def test_config14(self):
        """ Bad priority color value. """
        self.assertEqual(config("test/data/ConfigTest4.conf").priority_colors(),
                         config().defaults["colorscheme"]["priority_colors"])

    @skip("Error checking not yet implemented")
    def test_config15(self):
        """ Bad project color value. """
        self.assertEqual(config("test/data/ConfigTest4.conf").project_color(),
                         config().defaults["colorscheme"]["project_color"])

    @skip("Error checking not yet implemented")
    def test_config16(self):
        """ Bad context color value. """
        self.assertEqual(config("test/data/ConfigTest4.conf").context_color(),
                         config().defaults["colorscheme"]["context_color"])

    @skip("Error checking not yet implemented")
    def test_config17(self):
        """ Bad metadata color value. """
        self.assertEqual(config("test/data/ConfigTest4.conf").metadata_color(),
                         config().defaults["colorscheme"]["metadata_color"])

    @skip("Error checking not yet implemented")
    def test_config18(self):
        """ Bad link color value. """
        self.assertEqual(config("test/data/ConfigTest4.conf").link_color(),
                         config().defaults["colorscheme"]["link_color"])

    @skip("Test not yet implemented")
    # the test needs to be of the internal function _str_to_dict
    def test_config19(self):
        """ No priority color value. """
        self.assertEqual(config("test/data/ConfigTest4.conf").priority_colors(),
                         config().defaults["colorscheme"]["priority_colors"])

    def test_config20(self):
        """ No project color value. """
        self.assertEqual(config("test/data/ConfigTest5.conf").project_color(),
                         config().defaults["colorscheme"]["project_color"])

    def test_config21(self):
        """ No context color value. """
        self.assertEqual(config("test/data/ConfigTest5.conf").context_color(),
                         config().defaults["colorscheme"]["context_color"])

    def test_config22(self):
        """ No metadata color value. """
        self.assertEqual(config("test/data/ConfigTest5.conf").metadata_color(),
                         config().defaults["colorscheme"]["metadata_color"])

    def test_config23(self):
        """ No link color value. """
        self.assertEqual(config("test/data/ConfigTest5.conf").link_color(),
                         config().defaults["colorscheme"]["link_color"])

if __name__ == '__main__':
    unittest.main()
