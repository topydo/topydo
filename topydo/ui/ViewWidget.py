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
from six import u

from topydo.lib.Filter import get_filter_list, DependencyFilter, RelevanceFilter
from topydo.lib.Sorter import Sorter

class ViewWidget(urwid.LineBox):
    def __init__(self, p_todolist):
        self._todolist = p_todolist

        self.titleedit = urwid.Edit(u("Title: "), u(""))
        self.sortedit = urwid.Edit(u("Sort expression: "), u(""))
        self.filteredit = urwid.Edit(u("Filter expression: "), u(""))

        group = []
        self.relevantradio = urwid.RadioButton(group, u("Only show relevant todo items"), True)
        self.allradio = urwid.RadioButton(group, u("Show all todo items"))

        self.pile = urwid.Pile([
            self.titleedit,
            self.sortedit,
            self.filteredit,
            self.relevantradio,
            self.allradio,
            urwid.Button(u("Save"), lambda _: urwid.emit_signal(self, 'save')),
            urwid.Button(u("Cancel"), lambda _: urwid.emit_signal(self, 'close')),
        ])

        self.reset()

        super(ViewWidget, self).__init__(self.pile)

        urwid.register_signal(ViewWidget, ['save', 'close'])

    @property
    def view(self):
        """ Returns a tuple (title, view). """
        sorter = Sorter(self.sortedit.edit_text)
        filters = []

        if self.relevantradio.state == True:
            filters.append(DependencyFilter(self._todolist))
            filters.append(RelevanceFilter())

        filters += get_filter_list(self.filteredit.edit_text.split())

        return self._todolist.view(sorter, filters)

    @view.setter
    def view(self, p_view):
        pass # TODO

    @property
    def title(self):
        return self.titleedit.edit_text

    @title.setter
    def title(self, p_title):
        self.titleedit.edit_text = p_title

    def reset(self):
        """ Resets the form. """
        self.titleedit.set_edit_text(u(""))
        self.sortedit.set_edit_text(u(""))
        self.filteredit.set_edit_text(u(""))
        self.relevantradio.set_state(True)
        self.pile.focus_item = 0
