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

from topydo.ui.TodoWidget import TodoWidget

class TodoListWidget(urwid.LineBox):
    def __init__(self, p_view, p_title):
        self.view = p_view

        title_widget = urwid.Filler(urwid.Text(p_title, align='center'))

        self.todo_pile = urwid.Pile([])
        self.update()

        pile = urwid.Pile([
            (1, title_widget),
            (1, urwid.Filler(urwid.Divider(u'\u2500'))),
            ('weight', 1, urwid.Filler(self.todo_pile, valign='top')),
        ])

        pile.focus_position = 2

        super(TodoListWidget, self).__init__(pile)

    def update(self):
        """
        Updates the todo list according to the todos in the view associated
        with this list.
        """
        try:
            old_focus_position = self.todo_pile.focus_position
        except IndexError:
            old_focus_position = 0

        items = []

        for todo in self.view.todos:
            todowidget = TodoWidget(todo)
            items.append((todowidget, ('pack', None)))
            items.append((urwid.Divider(u'-'), ('weight', 1)))

        self.todo_pile.contents = items
        self.todo_pile.focus_position = min(old_focus_position, len(items) - 1)

    def _focus_down(self):
        size = len(self.todo_pile.contents)
        if self.todo_pile.focus_position < size - 2:
            self.todo_pile.focus_position += 2

    def _focus_up(self):
        if self.todo_pile.focus_position > 1:
            self.todo_pile.focus_position -= 2

    def keypress(self, p_size, p_key):
        if p_key == 'j' or p_key == 'down':
            self._focus_down()
        elif p_key == 'k' or p_key == 'up':
            self._focus_up()
        else:
            return super(TodoListWidget, self).keypress(p_size, p_key)

    def selectable(self):
        return True
