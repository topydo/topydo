"""
This module provides the Todo class.
"""

import datetime

import Config
import Utils
import TodoBase

class Todo(TodoBase.TodoBase):
    """
    This class adds common functionality with respect to dates to the Todo
    base class, mainly by interpreting the start and due dates of task.
    """

    def __init__(self, p_str, p_number=-1):
        TodoBase.TodoBase.__init__(self, p_str, p_number)
        self.attributes = {}

    def get_date(self, p_tag):
        """ Given a date tag, return a date object. """
        string = self.tag_value(p_tag)
        return Utils.date_string_to_date(string) if string else None

    def start_date(self):
        """ Returns a date object of the todo's start date. """
        return self.get_date(Config.TAG_START)

    def due_date(self):
        """ Returns a date object of the todo's due date. """
        return self.get_date(Config.TAG_DUE)

    def is_active(self):
        """
        Returns True when the start date is today or in the past and the
        task has not yet been completed.
        """
        start = self.start_date()
        return not self.is_completed() and \
              (not start or start <= datetime.date.today())

    def is_overdue(self):
        """
        Returns True when the due date is in the past and the task has not
        yet been completed.
        """
        return not self.is_completed() and self.days_till_due() < 0

    def days_till_due(self):
        """
        Returns the number of days till the due date. Returns a negative number
        of days when the due date is in the past.
        Returns 0 when the task has no due date.
        """
        due = self.due_date()
        if due:
            diff = due - datetime.date.today()
            return diff.days
        return 0

    def length(self):
        """
        Returns the length (in days) of the task, by considering the start date
        and the due date. Returns 0 when one of these dates are missing.
        """
        start = self.start_date()
        due = self.due_date()

        if start and due and start < due:
            diff = due - start
            return diff.days
        else:
            return 0

