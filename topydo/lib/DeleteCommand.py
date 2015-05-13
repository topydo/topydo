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

from topydo.lib.DCommand import DCommand

class DeleteCommand(DCommand):
    def __init__(self, p_args, p_todolist,
                 p_out=lambda a: None,
                 p_err=lambda a: None,
                 p_prompt=lambda a: None):
        super(DeleteCommand, self).__init__(
            p_args, p_todolist, p_out, p_err, p_prompt)

    def prompt_text(self):
        return "Also remove subtasks? [y/N] "

    def prefix(self):
        return "Removed: "

    def execute_specific_core(self, p_todo):
        self.todolist.delete(p_todo)

    def execute_specific(self, p_todo):
        self.out(self.prefix() + self.printer.print_todo(p_todo))
        self.execute_specific_core(p_todo)

    def usage(self):
        return """Synopsis: del [-f] <NUMBER1> [<NUMBER2> ...]"""

    def help(self):
        return """\
Deletes the todo item(s) with the given number(s) from the list."""
