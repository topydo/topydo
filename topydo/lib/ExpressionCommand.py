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

import re

from topydo.lib.Command import Command
from topydo.lib.Config import config
from topydo.lib import Filter
from topydo.lib.Sorter import Sorter
from topydo.lib.View import View

class ExpressionCommand(Command):
    """
    A common class for commands operating on todos selected by expressions.
    """
    def __init__(self, p_args, p_todolist,
                 p_out=lambda a: None,
                 p_err=lambda a: None,
                 p_prompt=lambda a: None):
        super(ExpressionCommand, self).__init__(
            p_args, p_todolist, p_out, p_err, p_prompt)

        self.sort_expression = config().sort_string()
        self.show_all = False
        # Commands using last argument differently (i.e as something other than
        # todo ID/expression) have to set attribute below to True.
        self.last_argument = False

    def _filters(self):
        filters = []

        def arg_filters():
            result = []

            if self.last_argument:
                args = self.args[:-1]
            else:
                args = self.args

            for arg in args:
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

    def _view(self):
        sorter = Sorter(self.sort_expression)
        filters = self._filters()

        return View(sorter, filters, self.todolist)
