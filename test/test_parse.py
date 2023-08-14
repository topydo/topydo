# Topydo - A todo.txt client written in Python.
# Copyright (C) 2023 David Steele <dsteele@gmail.com>
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

from topydo.lib.TodoParser import parse_line

complete_tasks = [
    "x 2023-08-12",
    "x 2023-08-12 ",
    "x 2023-08-12 2023-08-12",
    "x 2023-08-12 2023-08-12 ",
    "x 2023-08-12 2023-08-12 task text",
    "x 2023-08-12 2023-08-12 task text",
    "x 2023-08-12 task text",
    "x task text",
    "x ",
]

incomplete_tasks = [
    "",
    " ",
    " x",
    " x ",
    "x",
    "incomplete task",
]


def gen_test(task, result):
    def test_fn(self):
        task_dict = parse_line(task)

        self.assertEqual(task_dict["completed"], result, f'Failed "{task}"')

    return test_fn


def populate_tasks(cls):
    for i, task in enumerate(complete_tasks):
        setattr(cls, f"test_complete_{i}", gen_test(task, True))

    for i, task in enumerate(incomplete_tasks):
        setattr(cls, f"test_incomplete_{i}", gen_test(task, False))

    return cls


@populate_tasks
class ParseTodoTest(unittest.TestCase):
    pass


if __name__ == "__main__":
    unittest.main()
