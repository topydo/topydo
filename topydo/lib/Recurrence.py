# Topydo - A todo.txt client written in Python.
# Copyright (C) 2014 - 2015 Bram Schoenmakers <bram@topydo.org>
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

""" This module deals with recurring tasks. """

from datetime import date, timedelta

from topydo.lib.Config import config
from topydo.lib.RelativeDate import relative_date_to_date
from topydo.lib.Todo import Todo


class NoRecurrenceException(Exception):
    pass


def advance_recurring_todo(p_todo, p_offset=None, p_strict=False):
    """
    Given a Todo item, return a new instance of a Todo item with the dates
    shifted according to the recurrence rule.

    Strict means that the real due date is taken as a offset, not today or a
    future date to determine the offset.

    When the todo item has no due date, then the date is used passed by the
    caller (defaulting to today).

    When no recurrence tag is present, an exception is raised.
    """
    todo = Todo(p_todo.source())
    pattern = todo.tag_value('rec')

    if not pattern:
        raise NoRecurrenceException()
    elif pattern.startswith('+'):
        p_strict = True
        # strip off the +
        pattern = pattern[1:]

    if p_strict:
        offset = p_todo.due_date() or p_offset or date.today()
    else:
        offset = p_offset or date.today()

    length = todo.length()
    new_due = relative_date_to_date(pattern, offset)

    if not new_due:
        raise NoRecurrenceException()

    # pylint: disable=E1103
    todo.set_tag(config().tag_due(), new_due.isoformat())

    if todo.start_date():
        new_start = new_due - timedelta(length)
        todo.set_tag(config().tag_start(), new_start.isoformat())

    todo.set_creation_date(date.today())

    return todo
