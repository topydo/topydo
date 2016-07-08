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

class CommandLineWidget(urwid.Edit):
    def __init__(self, *args, **kwargs):

        self.history = []
        self.history_pos = None
        # temporary history storage for edits before cmd execution
        self.history_tmp = []

        super().__init__(*args, **kwargs)
        urwid.register_signal(CommandLineWidget, ['blur', 'execute_command'])

    def clear(self):
        self.set_edit_text("")

    def _blur(self):
        self.clear()
        urwid.emit_signal(self, 'blur')

    def _emit_command(self):
        if len(self.edit_text) > 0:
            urwid.emit_signal(self, 'execute_command', self.edit_text)
            self._save_to_history()
            self.clear()

    def _save_to_history(self):
        if len(self.edit_text) > 0:
            self.history.append(self.edit_text)

        self.history_pos = len(self.history)
        self.history_tmp = self.history[:] # sync temporary storage with real history
        self.history_tmp.append('')

    def _history_move(self, p_step):
        """
        Changes current value of the command-line to the value obtained from
        history_tmp list with index calculated by addition of p_step to the
        current position in the command history (history_pos attribute).

        Also saves value of the command-line (before changing it) to history_tmp
        for potential later access.
        """
        if len(self.history) > 0:
            # don't pollute real history - use temporary storage
            self.history_tmp[self.history_pos] = self.edit_text
            self.history_pos = self.history_pos + p_step
            self.set_edit_text(self.history_tmp[self.history_pos])

    def _history_next(self):
        if self.history_pos != len(self.history):
            self._history_move(1)

    def _history_back(self):
        if self.history_pos != 0:
            self._history_move(-1)

    def keypress(self, p_size, p_key):
        dispatch = {
            'enter': self._emit_command,
            'esc': self._blur,
            'up': self._history_back,
            'down': self._history_next
        }

        try:
            dispatch[p_key]()
        except KeyError:
            super().keypress(p_size, p_key)
