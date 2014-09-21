""" This module deals with recurring tasks. """

from datetime import date, timedelta

import Config
from RelativeDate import relative_date_to_date
import Todo

class NoRecurrenceException(Exception):
  pass

def _get_due_date(p_todo):
    """
    Gets the due date of a todo as a date object. Defaults to today when the
    todo has no due date, or when the due date was in the past.
    """

    due = p_todo.due_date()
    return due if (due and due >= date.today()) else date.today()

def advance_recurring_todo(p_todo):
    """
    Given a Todo item, return a new instance of a Todo item with the dates
    shifted according to the recurrence rule.

    When no recurrence tag is present, an exception is raised.
    """

    todo = Todo.Todo(p_todo.source())
    pattern = todo.tag_value('rec')

    if not pattern:
        raise NoRecurrenceException()

    due = _get_due_date(todo)
    length = todo.length()

    new_due = relative_date_to_date(pattern, due)
    todo.set_tag(Config.TAG_DUE, new_due.isoformat())

    if todo.start_date():
        new_start = new_due - timedelta(length)
        todo.set_tag(Config.TAG_START, new_start.isoformat())

    todo.set_creation_date(date.today())

    return todo
