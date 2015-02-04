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

import re
import unittest

from topydo.lib.Config import config
import CommandTest
from topydo.lib.IcalCommand import IcalCommand
import TestFacilities

class IcalCommandTest(CommandTest.CommandTest):
    def setUp(self):
        super(IcalCommandTest, self).setUp()
        self.todolist = TestFacilities.load_file_to_todolist("test/data/ListCommandTest.txt")

    def test_ical(self):
        def replace_ical_tags(p_text):
            # replace identifiers with dots, since they're random.
            result = re.sub(r'\bical:....\b', 'ical:....', p_text)
            result = re.sub(r'\bUID:....\b', 'UID:....', result)

            return result

        command = IcalCommand([""], self.todolist, self.out, self.error)
        command.execute()

        self.assertTrue(self.todolist.is_dirty())

        icaltext = ""
        with open('test/data/ListCommandTest.ics', 'r') as ical:
            icaltext = "".join(ical.readlines())

        self.assertEquals(replace_ical_tags(self.output), replace_ical_tags(icaltext))
        self.assertEquals(self.errors, "")

    def test_help(self):
        command = IcalCommand(["help"], self.todolist, self.out, self.error)
        command.execute()

        self.assertEquals(self.output, "")
        self.assertEquals(self.errors, command.usage() + "\n\n" + command.help() + "\n")

if __name__ == '__main__':
    unittest.main()
