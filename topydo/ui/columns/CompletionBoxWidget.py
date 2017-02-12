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

from topydo.ui.columns.Utils import PaletteItem


class CompletionBoxWidget(urwid.ListBox):
    def __init__(self):
        self.body = urwid.SimpleFocusListWalker([])

        super().__init__(self.body)
        urwid.register_signal(CompletionBoxWidget, ['close_completion_box',
                                                    'send_completion_candidate'])

    def add_completions(self, p_completions):
        for completion in p_completions:
            w = urwid.Text(completion)
            self.body.append(urwid.AttrMap(w, None, focus_map=PaletteItem.MARKED))
            self.body.set_focus(0)

    def keypress(self, p_size, p_key):
        if p_key == 'tab':
            try:
                self.focus_position += 1
            except IndexError:
                self.focus_position = 0
            self.calculate_visible(p_size)
            candidate = self.focus.original_widget.text
            urwid.emit_signal(self, 'send_completion_candidate', candidate)
        elif p_key == 'shift tab':
            try:
                self.focus_position -= 1
            except IndexError:
                self.focus_position = len(self.body) - 1
            self.calculate_visible(p_size)
            candidate = self.focus.original_widget.text
            urwid.emit_signal(self, 'send_completion_candidate', candidate)
        else:
            self.body.clear()
            urwid.emit_signal(self, 'close_completion_box', p_size, p_key)
