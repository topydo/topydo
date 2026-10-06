# Topydo - A todo.txt client written in Python.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

"""Keyboard focus regression tests for the columns UI."""

import unittest
from importlib.util import find_spec
from unittest.mock import patch

if find_spec('urwid') is None or find_spec('watchdog') is None:
    raise unittest.SkipTest('The columns UI dependencies are not available')

import urwid

from topydo.lib.Config import config
from topydo.ui.columns.Main import UIApplication
from topydo.ui.columns.TodoWidget import TodoWidget

from .topydo_testcase import TopydoTest


class ColumnsFocusTest(TopydoTest):
    def setUp(self):
        config('')
        TodoWidget.wipe_cache()
        self.addCleanup(TodoWidget.wipe_cache)

        # Keep real widgets and event dispatch, but avoid terminal and file I/O.
        with patch('sys.argv', ['topydo', 'columns']), \
                patch('topydo.ui.columns.Main.TodoFileWatched') as todofile, \
                patch('topydo.ui.columns.Main.get_terminal_size'), \
                patch('topydo.ui.columns.Main.urwid.raw_display.Screen') as screen:
            todofile.return_value.read.return_value = ['First task', 'Second task']
            screen.return_value.get_cols_rows.return_value = (100, 30)
            self.app = UIApplication()

        layout = [{
            'title': title,
            'sortexpr': 'text',
            'groupexpr': '',
            'filterexpr': '',
            'show_all': True,
        } for title in ['First column', 'Second column']]

        # Build the normal startup layout, stopping before the terminal loop.
        with patch('topydo.ui.columns.Main.columns', return_value=layout), \
                patch.object(self.app.mainloop, 'run', side_effect=urwid.ExitMainLoop):
            with self.assertRaises(urwid.ExitMainLoop):
                self.app.run()

    def test_initial_focus(self):
        self.assertIs(self.app.mainwindow.focus, self.app.columns)
        self.assertEqual(self.app.columns.focus_position, 0)
        self.assertEqual(self.app.columns.focus.todolist.focus, 0)

    def test_colon_focuses_commandline(self):
        self.app.mainwindow.focus_position = 0
        self.app.mainloop.process_input([':', 'a'])

        self.assertIs(self.app.mainwindow.focus, self.app.cli_wrapper)
        self.assertEqual(self.app.commandline.edit_text, 'a')

    def test_escape_restores_selected_todo(self):
        self.app.columns.focus_position = 1
        self.app.columns.focus.todolist.set_focus(2)
        selected_todo = self.app.columns.focus.todolist.get_focus()[0]
        self.app.mainwindow.focus_position = 1
        self.app.mainloop.process_input(['a', 'esc'])

        self.assertIs(self.app.mainwindow.focus, self.app.columns)
        self.assertEqual(self.app.columns.focus_position, 1)
        self.assertIs(self.app.columns.focus.todolist.get_focus()[0], selected_todo)
        self.assertEqual(self.app.commandline.edit_text, '')

    def test_repeated_focus_switches(self):
        for _ in range(3):
            self.app.mainloop.process_input([':', 'a'])
            self.assertIs(self.app.mainwindow.focus, self.app.cli_wrapper)
            self.assertEqual(self.app.commandline.edit_text, 'a')

            self.app.mainloop.process_input(['esc'])
            self.assertIs(self.app.mainwindow.focus, self.app.columns)
            self.assertEqual(self.app.commandline.edit_text, '')

    def test_escape_hides_console(self):
        self.app._print_to_console('Command output')
        self.assertTrue(self.app._console_visible)
        self.app.mainwindow.focus_position = 1
        self.app.mainloop.process_input(['esc'])

        self.assertFalse(self.app._console_visible)
        self.assertIs(self.app.mainwindow.focus, self.app.columns)


if __name__ == '__main__':
    unittest.main()
