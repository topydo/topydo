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

from topydo.lib.MultiCommand import MultiCommand
from topydo.lib.prettyprinters.Numbers import PrettyPrinterNumbers


class DepriCommand(MultiCommand):
    def __init__(self, p_args, p_todolist, #pragma: no branch
                 p_out=lambda a: None,
                 p_err=lambda a: None,
                 p_prompt=lambda a: None):
        super().__init__(
            p_args, p_todolist, p_out, p_err, p_prompt)

    def _execute_multi_specific(self):
        self.printer.add_filter(PrettyPrinterNumbers(self.todolist))

        for todo in self.todos:
            if todo.priority() != None:
                self.todolist.set_priority(todo, None)
                self.out("Priority removed.")
                self.out(self.printer.print_todo(todo))

    def usage(self):
        return """\
Synopsis: depri <NUMBER 1> [<NUMBER 2> ...]
          depri [-x] -e <EXPRESSION>\
"""

    def help(self):
        return """Removes the priority of the given todo item(s).

It is also possible to deprioritize items as complete with an EXPRESSION using
the -e flag. Use -x to also process todo items that are normally invisible (as
with the 'ls' subcommand).\
"""
