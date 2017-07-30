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

from os.path import commonprefix

import urwid

from topydo.ui.columns.CompletionBoxWidget import CompletionBoxWidget


class CommandLineWidget(urwid.Edit):
    def __init__(self, p_completer, *args, **kwargs):

        self.history = []
        self.history_pos = None
        # temporary history storage for edits before cmd execution
        self.history_tmp = []

        self.completer = p_completer
        self.completion_box = CompletionBoxWidget()
        self._surrounding_text = None  # text before insertion of completion

        super().__init__(*args, **kwargs)
        urwid.register_signal(CommandLineWidget, ['blur',
                                                  'execute_command',
                                                  'show_completions',
                                                  'hide_completions'])

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

    def insert_completion(self, p_insert):
        """
        Inserts currently chosen completion (p_insert parameter) into proper
        place in edit_text and adjusts cursor position accordingly.
        """
        start, end = self._surrounding_text
        final_text = start + p_insert + end
        self.set_edit_text(final_text)
        self.set_edit_pos(len(start) + len(p_insert))

    @property
    def completion_mode(self):
        return len(self.completion_box) > 1

    @completion_mode.setter
    def completion_mode(self, p_enable):
        if p_enable is True:
            urwid.emit_signal(self, 'show_completions')
        elif p_enable is False:
            self._surrounding_text = None
            if self.completion_mode:
                self.completion_box.clear()
                urwid.emit_signal(self, 'hide_completions')

    def _complete(self):
        """
        Main completion function.

        Gets list of potential completion candidates for currently edited word,
        completes it to the longest common part, and shows convenient completion
        widget (if multiple completions are returned) with currently selected
        candidate highlighted.
        """
        def find_word_start(p_text, p_pos):
            """ Returns position of the beginning of a word ending in p_pos. """
            return p_text.lstrip().rfind(' ', 0, p_pos) + 1

        def get_word_before_pos(p_text, p_pos):
            start = find_word_start(p_text, p_pos)

            return (p_text[start:p_pos], start)

        pos = self.edit_pos
        text = self.edit_text
        completer = self.completer

        word_before_cursor, start = get_word_before_pos(text, pos)
        completions = completer.get_completions(word_before_cursor, start == 0)
        # store slices before and after place for completion
        self._surrounding_text = (text[:start], text[pos:])

        single_completion = len(completions) == 1
        completion_done = single_completion and completions[0] == word_before_cursor

        if completion_done or not completions:
            self.completion_mode = False
            return
        elif single_completion:
            replacement = completions[0]
        else:
            replacement = commonprefix(completions)
            zero_candidate = replacement if replacement else word_before_cursor

            if zero_candidate != completions[0]:
                completions.insert(0, zero_candidate)

            self.completion_box.add_completions(completions)

        self.insert_completion(replacement)
        self.completion_mode = not single_completion

    def _completion_move(self, p_step, p_size):
        """
        Visually selects completion specified by p_step (positive numbers
        forwards, negative numbers backwards) and inserts it into edit_text.

        If p_step results in value out of range of currently evaluated
        completion candidates, list is rewinded to the start (if cycling
        forwards) or to the end (if cycling backwards).
        """
        current_position = self.completion_box.focus_position

        try:
            self.completion_box.set_focus(current_position + p_step)
        except IndexError:
            position = 0 if p_step > 0 else len(self.completion_box) - 1
            self.completion_box.set_focus(position)

        maxcols, = p_size
        size = (maxcols, self.completion_box.height)
        self.completion_box.calculate_visible(size)

        candidate = self.completion_box.focus.original_widget.text
        self.insert_completion(candidate)

    def _prev_completion(self, p_size):
        if self.completion_mode:
            self._completion_move(-1, p_size)

    def _next_completion(self, p_size):
        self._completion_move(1, p_size)

    def _home(self):
        """ Moves cursor to the beginning of the line. """
        self.set_edit_pos(0)

    def _end(self):
        """ Moves cursor to the end of the line. """
        end = len(self.edit_text)
        self.set_edit_pos(end)

    def _home_del(self):
        """ Deletes the line content before the cursor  """
        text = self.edit_text[self.edit_pos:]
        self.set_edit_text(text)
        self._home()

    def _end_del(self):
        """ Deletes the line content after the cursor  """
        text = self.edit_text[:self.edit_pos]
        self.set_edit_text(text)

    def keypress(self, p_size, p_key):
        tab_handler = self._complete

        if self.completion_mode:
            tab_handler = lambda: self._next_completion(p_size)

            if p_key not in {'tab', 'shift tab'}:
                self.completion_mode = False

        dispatch = {
            'enter': self._emit_command,
            'esc': self._blur,
            'up': self._history_back,
            'down': self._history_next,
            'ctrl a': self._home,
            'ctrl e': self._end,
            'ctrl u': self._home_del,
            'ctrl k': self._end_del,
            'tab': tab_handler,
            'shift tab': lambda: self._prev_completion(p_size)
        }

        try:
            dispatch[p_key]()
        except KeyError:
            super().keypress(p_size, p_key)
