# Topydo - A todo.txt client written in Python.
# Copyright (C) 2015 Bram Schoenmakers <bram@topydo.org>
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

from topydo.lib.Config import config


class ViewWidget(urwid.LineBox):
    def __init__(self, p_todolist):
        self._todolist = p_todolist

        self.titleedit = urwid.Edit("Title: ", "")
        self.sortedit = urwid.Edit("Sort expression: ", "")
        self.groupedit = urwid.Edit("Group expression: ", "")
        self.filteredit = urwid.Edit("Filter expression: ", "")

        radiogroup = []
        self.relevantradio = urwid.RadioButton(radiogroup, "Only show relevant todo items", True)
        self.allradio = urwid.RadioButton(radiogroup, "Show all todo items")

        self.pile = urwid.Pile([
            self.filteredit,
            self.titleedit,
            self.sortedit,
            self.groupedit,
            self.relevantradio,
            self.allradio,
            urwid.Button("Save", lambda _: urwid.emit_signal(self, 'save')),
            urwid.Button("Cancel", lambda _: self.close()),
        ])

        self.reset()

        super().__init__(self.pile)

        urwid.register_signal(ViewWidget, ['save', 'close'])

    @property
    def data(self):
        return {
            'title': self.titleedit.edit_text or self.filteredit.edit_text,
            'sortexpr': self.sortedit.edit_text or config().sort_string(),
            'groupexpr': self.groupedit.edit_text or config().group_string(),
            'filterexpr': self.filteredit.edit_text,
            'show_all': self.allradio.state,
        }

    @data.setter
    def data(self, p_data):
        self.titleedit.edit_text = p_data['title']
        self.sortedit.edit_text = p_data['sortexpr']
        self.groupedit.edit_text = p_data['groupexpr']
        self.filteredit.edit_text = p_data['filterexpr']
        self.relevantradio.set_state(not p_data['show_all'])
        self.allradio.set_state(p_data['show_all'])

    def reset(self):
        """ Resets the form. """
        self.titleedit.set_edit_text("")
        self.sortedit.set_edit_text("")
        self.filteredit.set_edit_text("")
        self.relevantradio.set_state(True)
        self.pile.focus_item = 0

    def close(self):
        urwid.emit_signal(self, 'close')

    def keypress(self, p_size, p_key):
        if p_key == 'esc':
            self.close()
        else:
            return super().keypress(p_size, p_key)  # pylint: disable=E1102
