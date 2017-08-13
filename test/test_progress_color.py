# Topydo - A todo.txt client written in Python.
# Copyright (C) 2016 Bram Schoenmakers <bram@topydo.org>
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

import unittest

from freezegun import freeze_time

from topydo.lib.Config import config
from topydo.lib.ProgressColor import progress_color
from topydo.lib.Todo import Todo
from topydo.lib.TodoList import TodoList

from .topydo_testcase import TopydoTest


def set_256_colors():
    config(p_overrides={('topydo', 'colors'): '256'})

@freeze_time('2016, 01, 01')
class ProgressColorTest(TopydoTest):

    def test_progress1(self):
        """ Test progress of task with no length """
        color = progress_color(Todo('Foo'))
        self.assertEqual(color.color, 2)

    def test_progress2(self):
        """ Test progress of task with no length (but with creation date). """
        color = progress_color(Todo('2016-02-11 Foo'))
        self.assertEqual(color.color, 2)

    def test_progress3(self):
        """ Test progress of task with no length """
        set_256_colors()

        color = progress_color(Todo('Foo'))
        self.assertEqual(color.color, 22)

    def test_progress4(self):
        """ Test progress of task with no length (but with creation date). """
        set_256_colors()

        color = progress_color(Todo('2016-02-11 Foo'))
        self.assertEqual(color.color, 22)

    def test_progress5(self):
        """ Test overdue tasks """
        color = progress_color(Todo('Foo due:2015-12-31'))
        self.assertEqual(color.color, 1)

    def test_progress6(self):
        """ Test overdue tasks """
        set_256_colors()

        color = progress_color(Todo('Foo due:2015-12-31'))
        self.assertEqual(color.color, 196)

    def test_progress7(self):
        """ Due today """
        color = progress_color(Todo('Foo due:2016-01-01'))
        self.assertEqual(color.color, 3)

    def test_progress8(self):
        """ Due today (256) """

        set_256_colors()
        color = progress_color(Todo('Foo due:2016-01-01'))
        self.assertEqual(color.color, 202)

    def test_progress9(self):
        """ Due tomorrow """
        color = progress_color(Todo('Foo due:2016-01-02'))
        # a length of 14 days is assumed
        self.assertEqual(color.color, 3)

    def test_progress10(self):
        set_256_colors()
        color = progress_color(Todo('Foo due:2016-01-02'))
        # a length of 14 days is assumed
        self.assertEqual(color.color, 208)

    def test_progress11(self):
        """ Due tomorrow (creation date) """
        color = progress_color(Todo('2016-01-01 Foo due:2016-01-02'))
        # a length of 14 days is assumed
        self.assertEqual(color.color, 2)

    def test_progress12(self):
        """ Due tomorrow (creation date) """
        set_256_colors()
        color = progress_color(Todo('2016-01-01 Foo due:2016-01-02'))
        self.assertEqual(color.color, 22)

    def test_progress13(self):
        """ Due tomorrow (recurrence) """
        color = progress_color(Todo('Foo due:2016-01-02 rec:1d'))
        self.assertEqual(color.color, 2)

    def test_progress14(self):
        """ Due tomorrow (recurrence) """
        set_256_colors()
        color = progress_color(Todo('Foo due:2016-01-02 rec:1d'))
        self.assertEqual(color.color, 22)

    def test_progress15(self):
        """ Due tomorrow (creation date + recurrence) """
        color = progress_color(Todo('2016-12-01 Foo due:2016-01-02 rec:1d'))
        self.assertEqual(color.color, 2)

    def test_progress16(self):
        """ Due tomorrow (creation date + recurrence) """
        set_256_colors()
        color = progress_color(Todo('2015-12-01 Foo due:2016-01-02 rec:1d'))
        self.assertEqual(color.color, 22)

    def test_progress17(self):
        """ Due tomorrow (creation date + recurrence + start date) """
        color = progress_color(Todo('2016-12-01 Foo due:2016-01-02 rec:1d t:2016-01-02'))
        self.assertEqual(color.color, 2)

    def test_progress18(self):
        """ Due tomorrow (creation date + recurrence + start date) """
        set_256_colors()
        color = progress_color(Todo('2015-12-01 Foo due:2016-01-02 rec:1d t:2016-01-02'))
        self.assertEqual(color.color, 22)

    def test_progress19(self):
        """ Due tomorrow (creation date + strict recurrence + start date) """
        color = progress_color(Todo('2016-12-01 Foo due:2016-01-02 rec:+1d t:2016-01-02'))
        self.assertEqual(color.color, 2)

    def test_progress20(self):
        """ Due tomorrow (creation date + strict recurrence + start date) """
        set_256_colors()
        color = progress_color(Todo('2015-12-01 Foo due:2016-01-02 rec:+1d t:2016-01-02'))
        self.assertEqual(color.color, 22)

    def test_progress21(self):
        """ Due tomorrow (creation date + start date) """
        color = progress_color(Todo('2016-12-01 Foo due:2016-01-02 t:2016-01-02'))
        self.assertEqual(color.color, 2)

    def test_progress22(self):
        """ Due tomorrow (creation date + start date) """
        set_256_colors()
        color = progress_color(Todo('2015-12-01 Foo due:2016-01-02 t:2016-01-02'))
        self.assertEqual(color.color, 22)

    def test_progress23(self):
        """ Due tomorrow (creation date + start date) """
        color = progress_color(Todo('2016-12-01 Foo due:2016-01-02 t:2015-12-31'))
        self.assertEqual(color.color, 10)

    def test_progress24(self):
        """ Due tomorrow (creation date + start date) """
        set_256_colors()
        color = progress_color(Todo('2015-12-01 Foo due:2016-01-02 t:2015-12-31'))
        self.assertEqual(color.color, 118)

    def test_progress25(self):
        """ Start date after due date """
        color = progress_color(Todo('Foo due:2016-01-02 t:2016-01-03'))
        # a length of 14 days is assumed
        self.assertEqual(color.color, 3)

    def test_progress26(self):
        """ Start date after due date """
        set_256_colors()
        color = progress_color(Todo('Foo due:2016-01-02 t:2016-01-03'))
        # a length of 14 days is assumed
        self.assertEqual(color.color, 208)

    def test_progress27(self):
        """ Creation date after due date """
        set_256_colors()
        color = progress_color(Todo('2016-01-03 Foo due:2016-01-02'))
        # a length of 14 days is assumed
        self.assertEqual(color.color, 208)

    def test_progress28(self):
        """ Progress color determined by parent """
        todolist = TodoList([
            "Overdue id:1 due:2015-12-31",
            "Bar p:1",
        ])

        color = progress_color(todolist.todo(2))

        # color the subitem red because it has no color of its own and its
        # parent is overdue
        self.assertEqual(color.color, 1)

    def test_progress29(self):
        """ Progress color determined by parent """
        todolist = TodoList([
            "Overdue id:1 due:2015-12-31",
            "Bar p:1 t:2016-01-01 due:2016-01-01",
        ])

        color = progress_color(todolist.todo(2))

        # the parent has no influence here
        self.assertEqual(color.color, 3)

    def test_progress30(self):
        """ Progress color determined by parent """
        todolist = TodoList([
            "Foo id:1",
            "Bar p:1",
        ])

        color = progress_color(todolist.todo(2))

        # the parent has no influence here
        self.assertEqual(color.color, 2)


if __name__ == '__main__':
    unittest.main()
