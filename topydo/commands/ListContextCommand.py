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

from topydo.lib.Command import Command


class ListContextCommand(Command):
    def __init__(self, p_args, p_todolist, #pragma: no branch
                 p_out=lambda a: None,
                 p_err=lambda a: None,
                 p_prompt=lambda a: None):
        super().__init__(
            p_args, p_todolist, p_out, p_err, p_prompt)

        self.counts = False
        self.sort_by = 'name'

    def _process_flags(self):
        flags, args = self.getopt("csS")
        for flag, _ in flags:
            if flag == "-c":
                self.counts = True
            elif flag == "-s":
                self.sort_by = 'counts'
            elif flag == "-S":
                self.sort_by = 'counts_inv'

    def execute(self):
        if not super().execute():
            return False

        self._process_flags()

        if self.counts:
            sorting_fns = {
                'name': lambda s: s[0].lower(),
                'counts': lambda s: s[1],
                'counts_inv': lambda s: -s[1]
            }

            for context, c in sorted(self.todolist.contexts_counts().items(),
                                     key=sorting_fns[self.sort_by]):
                self.out("{}\t{}".format(c, context))
        else:
            for context in sorted(self.todolist.contexts(),
                                  key=lambda s: s.lower()):
                self.out(context)

    def usage(self):
        return """Synopsis: lscon"""

    def help(self):
        return """Lists all contexts in the todo list."""
