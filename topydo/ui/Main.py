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

from topydo.cli.CLIApplicationBase import CLIApplicationBase
from topydo.Commands import get_subcommand
from topydo.ui.CommandLineWidget import CommandLineWidget
from topydo.ui.ConsoleWidget import ConsoleWidget
from topydo.ui.TodoListWidget import TodoListWidget
from topydo.lib.Config import config
from topydo.lib.Sorter import Sorter
from topydo.lib import TodoFile
from topydo.lib import TodoList

COLUMN_WIDTH = 40

class UIApplication(CLIApplicationBase):
    def __init__(self):
        super(UIApplication, self).__init__()

        self.columns = urwid.Columns([], dividechars=0, min_width=COLUMN_WIDTH)
        self.commandline = CommandLineWidget('topydo> ')
        self.console = ConsoleWidget()

        urwid.connect_signal(self.commandline, 'blur',
                             self._blur_commandline)
        urwid.connect_signal(self.commandline, 'execute_command',
                             self._execute_input)
        urwid.connect_signal(self.console, 'close', self._hide_console)

        self.mainwindow = urwid.Pile([
            ('weight', 1, self.columns),
            (1, urwid.Filler(self.commandline)),
        ])

        # the columns should have keyboard focus
        self._blur_commandline()

        self.mainloop = urwid.MainLoop(
            self.mainwindow,
            unhandled_input=self._handle_input,
            pop_ups=True
        )

    def _execute_input(self, p_command):
        """
        Callback for executing a command that was entered on the command line box.
        """
        (subcommand, args) = get_subcommand(p_command.split())

        try:
            command = subcommand(
                args,
                self.todolist,
                self._output,
                self._output,
                lambda _: None, # TODO input
            )

            if command.execute() != False:
                self._post_execute()

        except TypeError:
            # TODO: show error message
            pass

    def _focus_commandline(self):
        self.mainwindow.focus_item = 1

    def _blur_commandline(self):
        self.mainwindow.focus_item = 0

    def _focus_next_column(self):
        size = len(self.columns.contents)
        if self.columns.focus_position < size -1:
            self.columns.focus_position += 1

    def _focus_previous_column(self):
        if self.columns.focus_position > 0:
            self.columns.focus_position -= 1

    def _handle_input(self, p_input):
        dispatch = {
            ':': self._focus_commandline,
            'left': self._focus_previous_column,
            'h': self._focus_previous_column,
            'right': self._focus_next_column,
            'l': self._focus_next_column,
        }

        try:
            dispatch[p_input]()
        except KeyError:
            # the key is unknown, ignore
            pass

    def _add_column(self, p_view, p_title):
        todolist = TodoListWidget(p_view, p_title)

        options = self.columns.options(
            width_type='given',
            width_amount=COLUMN_WIDTH,
            box_widget=True
        )

        item = (todolist, options)
        self.columns.contents.append(item)
        self.columns.focus_position = len(self.columns.contents) - 1

    def _show_console(self):
        self.mainwindow.contents.append((self.console, ('pack', None)))
        self.mainwindow.focus_position = 2

    def _hide_console(self):
        if self._console_is_visible():
            self.console.clear()
            del self.mainwindow.contents[2]

    def _console_is_visible(self):
        return len(self.mainwindow.contents) == 3

    def _print_to_console(self, p_text):
        if not self._console_is_visible():
            self._show_console()

        self.console.print_text(p_text)

    def _output(self, p_text):
        self._print_to_console(p_text + "\n")

    def run(self):
        self.todofile = TodoFile.TodoFile(config().todotxt())
        self.todolist = TodoList.TodoList(self.todofile.read())

        view1 = self.todolist.view(Sorter(), [])
        self._add_column(view1, "View 1")

        self.mainloop.run()

if __name__ == '__main__':
    UIApplication().run()
