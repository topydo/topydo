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

"""
Provides functions to calculate the importance value of a task.

For those who are familiar with the Toodledo website, the importance value is a
combination of the priority and the todo's due date. Low priority tasks due
today may have a higher importance than high priority tasks in the distant
future.
"""

from datetime import date

from topydo.lib.Config import config

IMPORTANCE_VALUE = {'A': 3, 'B': 2, 'C': 1}


def is_due_next_monday(p_todo):
    """ Returns True when today is Friday (or the weekend) and the given task
    is due next Monday.
    """
    today = date.today()
    due = p_todo.due_date()

    return due and due.weekday() == 0 and today.weekday() >= 4 and \
        p_todo.days_till_due() <= 3


def importance(p_todo, p_ignore_weekend=config().ignore_weekends()):
    """
    Calculates the importance of the given task.
    Returns an importance of zero when the task has been completed.

    If p_ignore_weekend is True, the importance value of the due date will be
    calculated as if Friday is immediately followed by Monday. This in case of
    a todo list at the office and you don't work during the weekends (you
    don't, right?)
    """
    result = 2

    priority = p_todo.priority()
    result += IMPORTANCE_VALUE[priority] if priority in IMPORTANCE_VALUE else 0

    if p_todo.has_tag(config().tag_due()):
        days_left = p_todo.days_till_due()

        if days_left >= 7 and days_left < 14:
            result += 1
        elif days_left >= 2 and days_left < 7:
            result += 2
        elif days_left >= 1 and days_left < 2:
            result += 3
        elif days_left >= 0 and days_left < 1:
            result += 5
        elif days_left < 0:
            result += 6

    if p_ignore_weekend and is_due_next_monday(p_todo):
        result += 1

    if p_todo.has_tag(config().tag_star()):
        result += 1

    return result if not p_todo.is_completed() else 0


def average_importance(p_todo, p_ignore_weekend=config().ignore_weekends()):
    own_importance = importance(p_todo, p_ignore_weekend)

    average = 0
    parents = []

    try:
        sum_importance = own_importance
        parents = p_todo.parents()
        for parent in parents:
            sum_importance += importance(parent, p_ignore_weekend)

        average = float(sum_importance) / float(1 + len(parents))
    except AttributeError:
        pass

    return max(own_importance, average)
