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
Provides a printer that transforms a list of Todo items to a graph in Dot
notation. Useful for displaying dependencies.
"""

from topydo.lib.PrettyPrinter import Printer


class DotPrinter(Printer):
    """
    A printer that converts a list of Todo items to a string in Dot format.
    """

    def __init__(self, p_todolist):
        super(DotPrinter, self).__init__()
        self.todolist = p_todolist

    def print_list(self, p_todos):
        def escape(p_text):
            """ Escapes double quotes as they are special in attributes. """
            return p_text.replace('"', '\\"')

        def legend():
            """
            Generates a legend for each todo item thas is to be printed.
            """
            return '\n'.join(sorted([escape('{} {}'.format(
                self.todolist.number(t), t.text()
            )) for t in p_todos]))

        node_name = lambda t: str(self.todolist.number(t))
        node_tooltip = lambda t: escape(t.text())

        result = 'digraph {\n'

        # print todos
        for todo in p_todos:
            result += '  {} [tooltip="{}"]\n'.format(
                node_name(todo),
                node_tooltip(todo),
            )

        # print edges
        for todo in p_todos:
            # only print the children that are actually in the list of todos
            children = set(p_todos) & set(self.todolist.children(todo,
                p_only_direct=True))

            for child in children:
                result += '  {} -> {}\n'.format(
                    node_name(todo),
                    node_name(child)
                )

        # print legend
        result += 'rank=sink\n'
        result += 'legend [ fontsize=8, shape=box, label="{}" ]\n'.format(legend())

        result += '}\n'
        return result
