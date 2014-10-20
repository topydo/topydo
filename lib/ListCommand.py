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

import getopt

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

        self.sort_expression = Config.SORT_STRING
        self.show_all = False

    def _process_flags(self):
        try:
            opts, args = getopt.getopt(self.args, 's:x')
        except getopt.GetoptError:
            return self.args

        for o, a in opts:
            if o == '-x':
                self.show_all = True
            elif o == '-s':
                self.sort_expression = a

        return args

    def execute(self):
        if not super(ListCommand, self).execute():
            return False

        args = self._process_flags()

        sorter = Sorter.Sorter(self.sort_expression)
        filters = [] if self.show_all else [Filter.DependencyFilter(self.todolist), Filter.RelevanceFilter()]

        if len(args) > 0:
            filters.append(Filter.GrepFilter(args[0]))

        filters.append(Filter.LimitFilter(Config.LIST_LIMIT))

        self.out(self.todolist.view(sorter, filters).pretty_print())

    def usage(self):
        return """Synopsis: ls [-x] [-s <sort_expression>] [expression]"""

    def help(self):
        return """Lists all relevant todos. A todo is relevant when:

* has not been completed yet;
* the start date (if present) has passed;
* there are no subitems that need to be completed.

When an expression is given, only the todos matching that expression are shown.

-s : Sort the list according to a sort expression. Defaults to the expression
     in the configuration.
-x : Show all todos (i.e. do not filter on dependencies or relevance)."""
