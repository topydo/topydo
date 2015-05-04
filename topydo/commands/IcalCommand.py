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

"""
Implements a subcommand that outputs an iCalendar file.
"""

from topydo.lib.IcalPrinter import IcalPrinter
from topydo.commands.ListCommand import ListCommand

class IcalCommand(ListCommand):
    def __init__(self, p_args, p_todolist,
                 p_out=lambda a: None,
                 p_err=lambda a: None,
                 p_prompt=lambda a: None):
        super(IcalCommand, self).__init__(
            p_args, p_todolist, p_out, p_err, p_prompt)

        self.printer = IcalPrinter(p_todolist)

    def _print(self):
        self.out(str(self._view()))

    def execute(self):
        try:
            import icalendar as _
        except ImportError:
            self.error("icalendar package is not installed.")
            return False

        return super(IcalCommand, self).execute()

    def usage(self):
        return """Synopsis: ical [-x] [expression]"""

    def help(self):
        return """\
Similar to the 'ls' subcommand, except that the todos are printed in iCalendar
format (RFC 2445) that can be imported by other calendar applications.

By default prints the active todo items, possibly filtered by the given
expression.

For the supported options, please refer to the help text of 'ls'
(topydo help ls).

While specifying the sort order is supported (-s flag), like in 'ls', this is
not meaningful in the context of an iCalendar file.

Note: be aware that this is not necessarily a read-only operation. This
subcommand may add ical tags to the printed todo items containing a unique ID.
Completed todo items may be archived.

Note: topydo does not support reading iCal files, this is merely a dump.
Changes made with other iCalendar enabled applications will not be processed.
Suggested usage is to use the output as a read-only calendar.
"""
