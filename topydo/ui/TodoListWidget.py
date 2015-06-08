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

import urwid

class TodoListWidget(urwid.WidgetWrap):
    def __init__(self, p_view, p_title):
        self.view = p_view

        title_widget = urwid.Filler(urwid.Text(p_title, align='center'))

        todos = []

        for todo in self.view.todos:
            todos.append(('pack', urwid.Text(todo.source())))
            todos.append(urwid.Divider(u'-'))

        todo_pile = urwid.Pile(todos)

        pile = urwid.Pile([
            (1, title_widget),
            (1, urwid.Filler(urwid.Divider(u'\u2500'))),
            ('weight', 1, urwid.Filler(todo_pile, valign='top')),
        ])

        widget = urwid.LineBox(pile)

        super(TodoListWidget, self).__init__(widget)
