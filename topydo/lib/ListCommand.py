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

import re

from topydo.lib.Command import Command
from topydo.lib.Config import config
from topydo.lib import Filter
from topydo.lib.PrettyPrinter import pp_indent
from topydo.lib.Sorter import Sorter

class ListCommand(Command):
    def __init__(self, p_args, p_todolist,
                 p_out=lambda a: None,
                 p_err=lambda a: None,
                 p_prompt=lambda a: None):
        super(ListCommand, self).__init__(
            p_args, p_todolist, p_out, p_err, p_prompt)

        self.sort_expression = config().sort_string()
        self.show_all = False

    def _process_flags(self):
        opts, args = self.getopt('s:x')

        for opt, value in opts:
            if opt == '-x':
                self.show_all = True
            elif opt == '-s':
                self.sort_expression = value

        self.args = args

    def _filters(self):
        filters = []

        def arg_filters():
            result = []
            for arg in self.args:
                if re.match(Filter.ORDINAL_TAG_MATCH, arg):
                    argfilter = Filter.OrdinalTagFilter(arg)
                elif len(arg) > 1 and arg[0] == '-':
                    # when a word starts with -, exclude it
                    argfilter = Filter.GrepFilter(arg[1:])
                    argfilter = Filter.NegationFilter(argfilter)
                else:
                    argfilter = Filter.GrepFilter(arg)

                result.append(argfilter)

            return result

        if not self.show_all:
            filters.append(Filter.DependencyFilter(self.todolist))
            filters.append(Filter.RelevanceFilter())

        filters += arg_filters()

        if not self.show_all:
            filters.append(Filter.LimitFilter(config().list_limit()))

        return filters

    def execute(self):
        if not super(ListCommand, self).execute():
            return False

        self._process_flags()

        sorter = Sorter(self.sort_expression)
        filters = self._filters()

        pp_filters = [pp_indent(config().list_indent())]
        self.out(self.todolist.view(sorter, filters).pretty_print(pp_filters))

    def usage(self):
        return """Synopsis: ls [-x] [-s <sort_expression>] [expression]"""

    def help(self):
        return """\
Lists all relevant todos. A todo is relevant when:

* has not been completed yet;
* the start date (if present) has passed;
* there are no subitems that need to be completed.

When an expression is given, only the todos matching that expression are shown.

-s : Sort the list according to a sort expression. Defaults to the expression
     in the configuration.
-x : Show all todos (i.e. do not filter on dependencies or relevance).
"""
