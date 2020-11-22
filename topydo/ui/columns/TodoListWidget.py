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

from topydo.lib.HashListValues import max_id_length
from topydo.lib.Utils import translate_key_to_config
from topydo.ui.columns.TodoWidget import TodoWidget
from topydo.ui.columns.Utils import PaletteItem


def get_execute_signal(p_prefix):
    if p_prefix == 'cmdv':
        signal = 'execute_command'
    else:
        signal = 'execute_command_silent'

    return signal


class TodoListWidget(urwid.LineBox):
    def __init__(self, p_view, p_title, p_keymap):
        self._view = None

        self.keymap = p_keymap
        # store a state for multi-key shortcuts (e.g. 'gg')
        self.keystate = None
        # store offset length for postpone command (e.g. '3' for 'p3w')
        self._pp_offset = None

        self._title = urwid.Text(p_title, align='center')
        self._title_widget = urwid.AttrMap(self._title, PaletteItem.DEFAULT)

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

        urwid.register_signal(TodoListWidget, ['execute_command_silent',
                                               'execute_command',
                                               'refresh',
                                               'add_pending_action',
                                               'remove_pending_action',
                                               'repeat_cmd',
                                               'column_action',
                                               'show_keystate',
                                               'toggle_mark',
                                               ])

    @property
    def view(self):
        return self._view

    @view.setter
    def view(self, p_view):
        self._view = p_view
        self.update()

    @property
    def title(self):
        return self._title.text

    @title.setter
    def title(self, p_title):
        self._title.set_text(p_title)

    def update(self):
        """
        Updates the todo list according to the todos in the view associated
        with this list.
        """
        old_focus_position = self.todolist.focus
        id_length = max_id_length(self.view.todolist.count())

        del self.todolist[:]

        for group, todos in self.view.groups.items():
            if len(self.view.groups) > 1:
                grouplabel = ", ".join(group)
                self.todolist.append(urwid.Text(grouplabel))
                self.todolist.append(urwid.Divider('-'))

            for todo in todos:
                todowidget = TodoWidget.create(todo, id_length)
                todowidget.number = self.view.todolist.number(todo)
                self.todolist.append(todowidget)
                self.todolist.append(urwid.Divider('-'))

        if old_focus_position:
            try:
                self.todolist.set_focus(old_focus_position)
            except IndexError:
                # scroll to the bottom if the last item disappeared from column
                # -2 for the same reason as in self._scroll_to_bottom()
                self.todolist.set_focus(len(self.todolist) - 2)

    def _go_down(self, p_size):
        self.listbox.keypress(p_size, 'down')
        self.listbox.set_focus_valign('bottom')

    def _scroll_to_top(self, p_size):
        if isinstance(self.todolist[0], urwid.Text):
            self.listbox.set_focus(2)
        else:
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

    @property
    def keystate(self):
        return self._keystate

    @keystate.setter
    def keystate(self, p_keystate):
        self._keystate = p_keystate
        keystate_to_show = p_keystate if p_keystate else ''
        urwid.emit_signal(self, 'show_keystate', keystate_to_show)

    def keypress(self, p_size, p_key):
        urwid.emit_signal(self, 'remove_pending_action')
        requires_further_input = ['postpone', 'postpone_s', 'pri']

        keymap, keystates = self.keymap

        shortcut = self.keystate or ''
        shortcut += translate_key_to_config(p_key)

        try:
            action = keymap[shortcut]
        except KeyError:
            action = None

        if action:
            if shortcut in keystates:
                # Supplied key-shortcut matches keystate and action. Save the
                # keystate in case user will hit another key and add an action
                # waiting for execution if user won't type anything further.
                self.keystate = shortcut
                if action not in requires_further_input:
                    self._add_pending_action(action, p_size)
            else:
                # Only action is matched. Handle it and reset keystate.
                self.resolve_action(action, p_size)
                self.keystate = None
            return
        else:
            if shortcut in keystates:
                self.keystate = shortcut
            else:
                try:
                    # Check whether current keystate matches built-in 'postpone'
                    # action.
                    mode = keymap[self.keystate]
                    if mode in ['postpone', 'postpone_s']:
                        if self._postpone_selected(p_key, mode) is not None:
                            self.keystate = None
                        else:
                            urwid.emit_signal(self, 'show_keystate',
                                              self.keystate + self._pp_offset)
                    else:
                        self.keystate = None
                    return
                except KeyError:
                    if not self.keystate:
                        # Single key that is not described in keymap config.
                        return self.listbox.keypress(p_size, p_key)
                    self.keystate = None
            return

    def mouse_event(self, p_size, p_event, p_button, p_column, p_row, p_focus):
        if p_event == 'mouse press':
            if p_button == 4:  # up
                self.listbox.keypress(p_size, 'up')
                return
            elif p_button == 5:  # down:
                self._go_down(p_size)
                return

        return super().mouse_event(p_size,  # pylint: disable=E1102
                                   p_event,
                                   p_button,
                                   p_column,
                                   p_row,
                                   p_focus)

    # pylint: disable=no-self-use
    def selectable(self):
        return True

    def _toggle_marked_status(self):
        try:
            todo = self.listbox.focus.todo
            todo_id = str(self.view.todolist.number(todo))
            if urwid.emit_signal(self, 'toggle_mark', todo_id):
                self.listbox.focus.mark()
            else:
                self.listbox.focus.unmark()
        except AttributeError:
            # No todo item selected
            pass

    def _mark_all(self):
        for todo in self.listbox.body:
            if isinstance(todo, TodoWidget):
                todo_id = str(self.view.todolist.number(todo.todo))
                urwid.emit_signal(self, 'toggle_mark', todo_id, 'mark')
                todo.mark()

    def _execute_on_selected(self, p_cmd_str, p_execute_signal):
        """
        Executes command specified by p_cmd_str on selected todo item.

        p_cmd_str should be a string with one replacement field ('{}') which
        will be substituted by id of the selected todo item.

        p_execute_signal is the signal name passed to the main loop. It should
        be one of 'execute_command' or 'execute_command_silent'.
        """
        try:
            todo = self.listbox.focus.todo
            todo_id = str(self.view.todolist.number(todo))

            urwid.emit_signal(self, p_execute_signal, p_cmd_str, todo_id)

            # force screen redraw after editing
            if p_cmd_str.startswith('edit'):
                urwid.emit_signal(self, 'refresh')
        except AttributeError:
            # No todo item selected
            pass

    def resolve_action(self, p_action_str, p_size=None):
        """
        Checks whether action specified in p_action_str is "built-in" or
        contains topydo command (i.e. starts with 'cmd') and forwards it to
        proper executing methods.

        p_size should be specified for some of the builtin actions like 'up' or
        'home' as they can interact with urwid.ListBox.keypress or
        urwid.ListBox.calculate_visible.
        """
        if p_action_str.startswith(('cmd ', 'cmdv ')):
            prefix, cmd = p_action_str.split(' ', 1)
            execute_signal = get_execute_signal(prefix)

            if '{}' in cmd:
                self._execute_on_selected(cmd, execute_signal)
            else:
                urwid.emit_signal(self, execute_signal, cmd)
        else:
            self.execute_builtin_action(p_action_str, p_size)

    def execute_builtin_action(self, p_action_str, p_size=None):
        """
        Executes built-in action specified in p_action_str.

        Currently supported actions are: 'up', 'down', 'home', 'end',
        'first_column', 'last_column', 'prev_column', 'next_column',
        'append_column', 'insert_column', 'edit_column', 'delete_column',
        'copy_column', swap_right', 'swap_left', 'postpone', 'postpone_s',
        'pri', 'mark', 'mark_all, 'reset' and 'repeat'.
        """
        column_actions = ['first_column',
                          'last_column',
                          'prev_column',
                          'next_column',
                          'append_column',
                          'insert_column',
                          'edit_column',
                          'delete_column',
                          'copy_column',
                          'swap_left',
                          'swap_right',
                          'reset',
                          ]

        if p_action_str in column_actions:
            urwid.emit_signal(self, 'column_action', p_action_str)
        elif p_action_str == 'up':
            self.listbox.keypress(p_size, p_action_str)
        elif p_action_str == 'down':
            self._go_down(p_size)
        elif p_action_str == 'home':
            self._scroll_to_top(p_size)
        elif p_action_str == 'end':
            self._scroll_to_bottom(p_size)
        elif p_action_str in ['postpone', 'postpone_s']:
            pass
        elif p_action_str == 'pri':
            pass
        elif p_action_str == 'mark':
            self._toggle_marked_status()
        elif p_action_str == 'mark_all':
            self._mark_all()
        elif p_action_str == 'repeat':
            self._repeat_cmd()

    def _add_pending_action(self, p_action, p_size):
        """
        Creates action waiting for execution and forwards it to the mainloop.
        """
        def generate_callback():
            def callback(*args):
                self.resolve_action(p_action, p_size)
                self.keystate = None

            return callback

        urwid.emit_signal(self, 'add_pending_action', generate_callback())

    def _postpone_selected(self, p_pattern, p_mode):
        """
        Postpones selected todo item by <COUNT><PERIOD>.

        Returns True after 'postpone' command is called (i.e. p_pattern is valid
        <PERIOD>), False when p_pattern is invalid and None if p_pattern is
        digit (i.e. part of <COUNT>).

        p_pattern accepts digit (<COUNT>) or one of the <PERIOD> letters:
        'd'(ay), 'w'(eek), 'm'(onth), 'y'(ear). If digit is specified, it is
        appended to _pp_offset attribute. If p_pattern contains one of the
        <PERIOD> letters, 'postpone' command is forwarded to execution with
        value of _pp_offset attribute used as <COUNT>. If _pp_offset is None,
        <COUNT> is set to 1.

        p_mode should be one of 'postpone_s' or 'postpone'. It decides whether
        'postpone' command should be called with or without '-s' flag.
        """
        if p_pattern.isdigit():
            if not self._pp_offset:
                self._pp_offset = ''
            self._pp_offset += p_pattern
            result = None
        else:
            if p_pattern in ['d', 'w', 'm', 'y', 'b']:
                offset = self._pp_offset or '1'
                if p_mode == 'postpone':
                    pp_cmd = 'cmd postpone {} '
                else:
                    pp_cmd = 'cmd postpone -s {} '
                pp_cmd += offset + p_pattern
                self.resolve_action(pp_cmd)
                result = True
            self._pp_offset = None
            result = False
        return result

    def _repeat_cmd(self):
        try:
            todo = self.listbox.focus.todo
            todo_id = str(self.view.todolist.number(todo))
        except AttributeError:
            todo_id = None

        urwid.emit_signal(self, 'repeat_cmd', todo_id)

    def highlight(self, p_highlight):
        if p_highlight:
            self._title_widget.set_attr_map({None: PaletteItem.DEFAULT_FOCUS})
        else:
            self._title_widget.set_attr_map({None: PaletteItem.DEFAULT})
