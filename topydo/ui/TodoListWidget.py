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

from six import text_type
import urwid

from topydo.ui.TodoWidget import TodoWidget

class TodoListWidget(urwid.LineBox):
    def __init__(self, p_view, p_title):
        self.view = p_view

        title_widget = urwid.Filler(urwid.Text(p_title, align='center'))

        self.todolist = urwid.SimpleFocusListWalker([])
        self.listbox = urwid.ListBox(self.todolist)
        self.update()

        pile = urwid.Pile([
            (1, title_widget),
            (1, urwid.Filler(urwid.Divider(u'\u2500'))),
            ('weight', 1, self.listbox),
        ])

        pile.focus_position = 2

        super(TodoListWidget, self).__init__(pile)

        urwid.register_signal(TodoListWidget, ['execute_command'])

    def update(self):
        """
        Updates the todo list according to the todos in the view associated
        with this list.
        """
        old_focus_position = self.todolist.focus

        del self.todolist[:]

        for todo in self.view.todos:
            todowidget = TodoWidget(todo, self.view.todolist.number(todo))
            self.todolist.append(todowidget)
            self.todolist.append(urwid.Divider(u'-'))

        if old_focus_position:
            self.todolist.set_focus(old_focus_position)

    def keypress(self, p_size, p_key):
        if p_key == 'x':
            self._complete_selected_item()
        elif p_key == 'j':
            self.listbox.keypress(p_size, 'down')
        elif p_key == 'k':
            self.listbox.keypress(p_size, 'up')
        else:
            if self.listbox.keypress(p_size, p_key):
                return super(TodoListWidget, self).keypress(p_size, p_key)

    def selectable(self):
        return True

    def _complete_selected_item(self):
        """
        Marks the highlighted todo item as complete.
        """
        try:
            todo = self.listbox.focus.todo
            self.view.todolist.number(todo)

            urwid.emit_signal(self, 'execute_command', "do {}".format(
                text_type(self.view.todolist.number(todo))))
        except AttributeError:
            # No todo item selected
            pass
