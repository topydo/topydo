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

from textwrap import wrap

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

        def node_label(p_todo):
            """
            Prints an HTML table for a node label with some todo details.
            """
            node_result = '<<TABLE CELLBORDER="0">'

            node_result += '<TR><TD><B>{}</B></TD><TD BALIGN="LEFT"><B>{}{}{}</B></TD></TR>'.format(
                self.todolist.number(p_todo),
                "<S>" if todo.is_completed() else "",
                "<BR />".join(wrap(p_todo.text(), 35)),
                "</S>" if todo.is_completed() else "",
            )
            node_result += '<HR/>'
            node_result += '<TR><TD ALIGN="LEFT">Prio:</TD><TD ALIGN="LEFT">{}</TD></TR>'.format(p_todo.priority())

            if p_todo.due_date():
                node_result += '<TR><TD ALIGN="LEFT">Due:</TD><TD ALIGN="LEFT">{}</TD></TR>'.format(p_todo.due_date().isoformat())

            node_result += '</TABLE>>'

            return node_result

        node_name = lambda t: '_' + str(self.todolist.number(t))
        node_tooltip = lambda t: escape(t.text())

        result = 'digraph {\n'
        result += 'node [ shape=plaintext ]\n';

        # print todos
        for todo in p_todos:
            result += '  {} [label={}, tooltip="{}"]\n'.format(
                node_name(todo),
                node_label(todo),
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

        result += '}\n'
        return result
