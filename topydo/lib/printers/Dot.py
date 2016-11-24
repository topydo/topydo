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

from topydo.lib.printers.PrettyPrinter import Printer
from topydo.lib.ProgressColor import progress_color
from topydo.lib.Utils import humanize_date


class DotPrinter(Printer):
    """
    A printer that converts a list of Todo items to a string in Dot format.
    """

    def __init__(self, p_todolist):
        super(DotPrinter, self).__init__()
        self.todolist = p_todolist

    def print_list(self, p_todos):
        def node_label(p_todo):
            """
            Prints an HTML table for a node label with some todo details.
            """
            node_result = '<<TABLE CELLBORDER="0" CELLSPACING="1" VALIGN="top">'

            def print_row(p_value1, p_value2):
                return '<TR><TD ALIGN="RIGHT">{}</TD><TD ALIGN="LEFT">{}</TD></TR>'.format(p_value1, p_value2)

            node_result += '<TR><TD><B>{}</B></TD><TD BALIGN="LEFT"><B>{}{}{}</B></TD></TR>'.format(
                self.todolist.number(p_todo),
                "<S>" if todo.is_completed() else "",
                "<BR />".join(wrap(p_todo.text(), 35)),
                "</S>" if todo.is_completed() else "",
            )

            priority = p_todo.priority()
            start_date = p_todo.start_date()
            due_date = p_todo.due_date()

            if priority or start_date or due_date:
                node_result += '<HR/>'

            if priority:
                node_result += print_row('Prio:', p_todo.priority())

            if start_date:
                node_result += print_row('Starts:', "{} ({})".format(
                    start_date.isoformat(),
                    humanize_date(start_date)
                ))

            if due_date:
                node_result += print_row('Due:', "{} ({})".format(
                    due_date.isoformat(),
                    humanize_date(due_date)
                ))

            node_result += '</TABLE>>'

            return node_result

        def foreground(p_background):
            """
            Chooses a suitable foreground color (black or white) given a
            background color.
            """

            (r, g, b) = p_background.as_rgb()
            brightness = (r * 299 + g * 587 + b * 114) / ( 255 * 1000 )

            return '#ffffff' if brightness < 0.5 else '#000000'

        node_name = lambda t: '_' + str(self.todolist.number(t))

        result = 'digraph topydo {\n'
        result += 'node [ shape="none" margin="0" fontsize="9" fontname="Helvetica" ]\n';

        # print todos
        for todo in p_todos:
            background_color = progress_color(todo)

            result += '  {} [label={} style=filled fillcolor="{}" fontcolor="{}"]\n'.format(
                node_name(todo),
                node_label(todo),
                background_color.as_html(),
                foreground(background_color),
            )

        # print edges
        for todo in p_todos:
            # only print the children that are actually in the list of todos
            children = set(p_todos) & set(self.todolist.children(todo,
                p_only_direct=True))

            for child in sorted(list(children), key=lambda t: t.text()):
                result += '  {} -> {}\n'.format(
                    node_name(todo),
                    node_name(child)
                )

        todos_without_dependencies = [todo for todo in p_todos if not self.todolist.children(todo) and not self.todolist.parents(todo)]
        for index in range(0, len(todos_without_dependencies) - 1):
            this_todo = todos_without_dependencies[index]
            next_todo = todos_without_dependencies[index + 1]
            result += '  {} -> {} [style="invis"]\n'.format(node_name(this_todo), node_name(next_todo))

        result += '}\n'
        return result
