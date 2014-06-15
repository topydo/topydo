"""
Provides a function to calculate the importance value of a task.

For those who are familiar with the Toodledo website, the importance value is a
combination of the priority and the todo's due date. Low priority tasks due
today may have a higher importance than high priority tasks in the distant
future.
"""

import datetime

import Config

IMPORTANCE_VALUE = {'A': 3, 'B': 2, 'C': 1}

def is_due_next_monday(p_todo):
    """ Returns True when the given task is due next Monday. """
    today = datetime.date.today()
    due = p_todo.due_date()

    return due and due.weekday() == 0 and today.weekday() >= 4 and \
        p_todo.days_till_due()

def importance(p_todo, p_ignore_weekend=False):
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

    if p_todo.has_tag(Config.TAG_DUE):
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

    if p_todo.has_tag(Config.TAG_STAR):
        result += 1

    return result if not p_todo.is_completed() else 0
