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

import re

from topydo.lib.MultiCommand import MultiCommand
from topydo.lib.prettyprinters.Numbers import PrettyPrinterNumbers
from topydo.lib.Utils import is_valid_priority


class PriorityCommand(MultiCommand):
    def __init__(self, p_args, p_todolist,  # pragma: no branch
                 p_out=lambda a: None,
                 p_err=lambda a: None,
                 p_prompt=lambda a: None):
        super().__init__(
            p_args, p_todolist, p_out, p_err, p_prompt)

        self.last_argument = True
        self.delete = False

    def _execute_multi_specific(self):
        def normalize_priority(p_priority):
            match = re.search(r'\b([A-Z])\b', p_priority.upper())
            return match.group(1) if match else p_priority

        priority = None if self.delete else normalize_priority(self.args[-1])
        self.printer.add_filter(PrettyPrinterNumbers(self.todolist))

        if is_valid_priority(priority):
            for todo in self.todos:
                old_priority = todo.priority()
                self.todolist.set_priority(todo, priority)

                if old_priority and priority and old_priority != priority:
                    self.out("Priority changed from {} to {}".format(
                        old_priority, priority))
                elif not old_priority:
                    self.out("Priority set to {}.".format(priority))

                self.out(self.printer.print_todo(todo))
        elif priority is None:
            for todo in self.todos:
                old_priority = todo.priority()
                self.todolist.set_priority(todo, None)

                if old_priority:
                    self.out("Priority removed.")

                self.out(self.printer.print_todo(todo))
        else:
            self.error("Invalid priority given.")

    def get_flags(self):
        return ("d", [])

    def process_flag(self, p_option, p_value):
        if p_option == '-d':
            self.delete = True
            self.last_argument = False
        else:
            raise NotImplementedError

    def usage(self):
        return """\
Synopsis: pri [-d] <NUMBER 1> [<NUMBER 2> ...] <PRIORITY>
          pri [-d] [-x] -e <EXPRESSION>\
"""

    def help(self):
        return """\
Sets the priority of todo(s) the given NUMBER(s) to the given PRIORITY.

Use the -d flag to remove the priority. It is also possible to prioritize items
with an EXPRESSION using the -e flag.  Use -x to also process todo items that
are normally invisible (as with the 'ls' subcommand).\
"""
