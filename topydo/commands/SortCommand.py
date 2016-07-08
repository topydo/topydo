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

from topydo.lib.Command import Command, InvalidCommandArgument
from topydo.lib.Config import config
from topydo.lib.Sorter import Sorter


class SortCommand(Command):
    def __init__(self, p_args, p_todolist, #pragma: no branch
                 p_out=lambda a: None,
                 p_err=lambda a: None,
                 p_prompt=lambda a: None):
        super().__init__(
            p_args, p_todolist, p_out, p_err, p_prompt)

    def execute(self):
        if not super().execute():
            return False

        try:
            expression = self.argument(0)
        except InvalidCommandArgument:
            expression = config().sort_string()

        sorter = Sorter(expression)  # TODO: validate
        sorted_todos = sorter.sort(self.todolist.todos())

        self.todolist.replace(sorted_todos)

    def usage(self):
        return """Synopsis: sort [<EXPRESSION>]"""

    def help(self):
        return """\
Sorts the todo file according to the EXPRESSION. If no EXPRESSION is given, the
expression in the configuration is used.

The EXPRESSION is a comma separated list of attributes to sort on. The list is
evaluated in order, which means that the first attribute takes higher
precedence, then the second, etc.

The following sort attributes are supported:

* priority       - Sort by priority
* creation       - Sort by creation date
* completed      - Sort by completion state
* importance     - Sort by importance
* importance-avg - Sort by average importance (based on parent items)
* text           - Sort by text
* <TAG>          - Sort by values of the given TAG

Each item can optionally be prefixed with asc: and desc: to specify ascending
or descending sort respectively. If not specified, ascending sort is assumed.

Example:

    desc:importance,due,desc:priority\
"""
