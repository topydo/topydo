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

import Command
import Config
import Filter
import Sorter

class ListCommand(Command.Command):
    def __init__(self, p_args, p_todolist,
                 p_out=lambda a: None,
                 p_err=lambda a: None,
                 p_prompt=lambda a: None):
        super(ListCommand, self).__init__(p_args, p_todolist, p_out, p_err, p_prompt)

    def execute(self):
        if not super(ListCommand, self).execute():
            return False

        show_all = self.argument_shift("-x")

        sorter = Sorter.Sorter(Config.SORT_STRING)
        filters = [] if show_all else [Filter.DependencyFilter(self.todolist), Filter.RelevanceFilter()]

        if len(self.args) > 0:
            filters.append(Filter.GrepFilter(self.argument(0)))

        self.out(self.todolist.view(sorter, filters).pretty_print())

    def usage(self):
        return """Synopsis: ls [-x] [expression]"""

    def help(self):
        return """Lists all relevant todos. A todo is relevant when:

* has not been completed yet;
* the start date (if present) has passed;
* there are no subitems that need to be completed.

When an expression is given, only the todos matching that expression are shown.

-x : Show all todos (i.e. do not filter on dependencies or relevance)."""
