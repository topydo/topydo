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
        self._view = None

        # store a state for multi-key shortcuts (e.g. 'gg')
        self.keystate = None

        self._title_widget = urwid.Text(p_title, align='center')

        self.todolist = urwid.SimpleFocusListWalker([])
        self.listbox = urwid.ListBox(self.todolist)
        self.view = p_view

        pile = urwid.Pile([
            (1, urwid.Filler(self._title_widget)),
            (1, urwid.Filler(urwid.Divider('\u2500'))),
            ('weight', 1, self.listbox),
        ])

        pile.focus_position = 2

        super().__init__(pile)

        urwid.register_signal(TodoListWidget, ['execute_command'])

    @property
    def view(self):
        return self._view

    @view.setter
    def view(self, p_view):
        self._view = p_view
        self.update()

    @property
    def title(self):
        return self._title_widget.text

    @title.setter
    def title(self, p_title):
        self._title_widget.set_text(p_title)

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
            self.todolist.append(urwid.Divider('-'))

        if old_focus_position:
            self.todolist.set_focus(old_focus_position)

    def _scroll_to_top(self, p_size):
        self.listbox.set_focus(0)

        # see comment at _scroll_to_bottom
        self.listbox.calculate_visible(p_size)

    def _scroll_to_bottom(self, p_size):
        # -2 because the last Divider shouldn't be focused.
        end_pos = len(self.listbox.body) - 2
        self.listbox.set_focus(end_pos)

        # for some reason, set_focus doesn't rerender the list.
        # calculate_visible is the only public method (besides keypress) that
        # deals with pending focus changes.
        self.listbox.calculate_visible(p_size)

    def keypress(self, p_size, p_key):
        # first check whether 'g' was pressed previously
        if self.keystate == 'g':
            if p_key == 'g':
                self._scroll_to_top(p_size)

            # make sure to accept normal shortcuts again
            self.keystate = None
            return

        if p_key == 'x':
            self._complete_selected_item()
        elif p_key == 'j':
            self.listbox.keypress(p_size, 'down')
        elif p_key == 'k':
            self.listbox.keypress(p_size, 'up')
        elif p_key == 'home':
            self._scroll_to_top(p_size)
        elif p_key == 'G' or p_key == 'end':
            self._scroll_to_bottom(p_size)
        elif p_key == 'g':
            self.keystate = 'g'
        else:
            return self.listbox.keypress(p_size, p_key)

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
                str(self.view.todolist.number(todo))))
        except AttributeError:
            # No todo item selected
            pass
