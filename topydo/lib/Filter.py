# Topydo - A todo.txt client written in Python.
# Copyright (C) 2014 Bram Schoenmakers <me@bramschoenmakers.nl>
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

import re

from topydo.lib.RelativeDate import relative_date_to_date
from topydo.lib.Utils import date_string_to_date

class Filter(object):
    def filter(self, p_todos):
        """
        Filters a list of todos. Truncates the list after p_limit todo
        items (or no maximum limit if omitted).
        """

        return [t for t in p_todos if self.match(t)]

    def match(self, _):
        raise NotImplementedError

class NegationFilter(Filter):
    def __init__(self, p_filter):
        self._filter = p_filter

    def match(self, p_todo):
        return not self._filter.match(p_todo)

class AndFilter(Filter):
    def __init__(self, p_filter1, p_filter2):
        self._filter1 = p_filter1
        self._filter2 = p_filter2

    def match(self, p_todo):
        return self._filter1.match(p_todo) and self._filter2.match(p_todo)

class OrFilter(Filter):
    def __init__(self, p_filter1, p_filter2):
        self._filter1 = p_filter1
        self._filter2 = p_filter2

    def match(self, p_todo):
        return self._filter1.match(p_todo) or self._filter2.match(p_todo)

class GrepFilter(Filter):
    """ Matches when the todo text contains a text. """

    def __init__(self, p_expression, p_case_sensitive=None):
        super(GrepFilter, self).__init__()

        # convert to string in case we receive integers
        self.expression = p_expression

        if p_case_sensitive != None:
            self.case_sensitive = p_case_sensitive
        else:
            # only be case sensitive when the expression contains at least one
            # capital character.
            self.case_sensitive = \
                len([c for c in self.expression if c.isupper()]) > 0

    def match(self, p_todo):
        expr = self.expression
        string = p_todo.source()
        if not self.case_sensitive:
            expr = expr.lower()
            string = string.lower()

        return string.find(expr) != -1

class RelevanceFilter(Filter):
    """
    Matches when the todo is relevant, i.e.:

    The item has not been completed AND
    The start date is blank, today or in the past, AND
    The priority is 'A' or the priority is B with due date within 30 days or
    the priority is C with due date within 14 days.
    """

    def match(self, p_todo):
        is_due = p_todo.is_active()
        is_due |= p_todo.due_date() == None
        is_due |= p_todo.priority() == 'A'
        is_due |= p_todo.priority() == 'B' and p_todo.days_till_due() <= 30
        is_due |= p_todo.priority() == 'C' and p_todo.days_till_due() <= 14

        return p_todo.is_active() and is_due

class DependencyFilter(Filter):
    """ Matches when a todo has no unfinished child tasks.  """
    def __init__(self, p_todolist):
        """
        Constructor.

        Pass on a TodoList instance such that the dependencies can be
        looked up.
        """
        super(DependencyFilter, self).__init__()
        self.todolist = p_todolist

    def match(self, p_todo):
        """
        Returns True when there are no children that are uncompleted yet.
        """
        children = self.todolist.children(p_todo)
        uncompleted = [todo for todo in children if not todo.is_completed()]

        return not uncompleted

class InstanceFilter(Filter):
    def __init__(self, p_todos):
        """
        Constructor.

        A filter which selects a number of Todo instances from a TodoList
        instance.

        This is handy for constructing a view given a plain list of Todo items.
        """
        super(InstanceFilter, self).__init__()
        self.todos = p_todos

    def match(self, p_todo):
        """
        Returns True when p_todo appears in the list of given todos.
        """
        try:
            self.todos.index(p_todo)
            return True
        except ValueError:
            return False

class LimitFilter(Filter):
    def __init__(self, p_limit):
        super(LimitFilter, self).__init__()
        self.limit = p_limit

    def filter(self, p_todos):
        return p_todos[:self.limit] if self.limit >= 0 else p_todos

ORDINAL_TAG_MATCH = r"(?P<key>[^:]*):(?P<operator><=?|=|>=?|!)?(?P<value>\S+)"

class OrdinalTagFilter(Filter):
    def __init__(self, p_expression):
        super(OrdinalTagFilter, self).__init__()

        self.expression = p_expression

        match = re.match(ORDINAL_TAG_MATCH, self.expression)
        if match:
            self.key = match.group('key')
            self.operator = match.group('operator') or '='
            self.value = match.group('value')

    def match(self, p_todo):
        """
        Performs a match on a key:value tag in the todo.

        First it tries to convert the value and the user-entered expression to
        a date and makes a comparison if it succeeds, based on the given
        operator (default ==).
        Upon failure, it falls back to converting value and user-entered
        expression to an integer and makes a numerical comparison based on the
        given operator (default ==)
        As a last resort, it falls back to using a Grep filter to see if the
        user given expression is contained in the todo text.
        """
        if not self.key or not p_todo.has_tag(self.key):
            return False

        try:
            operand1 = date_string_to_date(p_todo.tag_value(self.key))
            operand2 = relative_date_to_date(self.value)

            if not operand2:
                operand2 = date_string_to_date(self.value)

        except ValueError:
            operand1 = p_todo.tag_value(self.key)
            operand2 = self.value

            try:
                operand1 = int(operand1)
                operand2 = int(operand2)
            except ValueError:
                grep = GrepFilter(self.expression)
                return grep.match(p_todo)

        if self.operator == '<':
            return operand1 < operand2
        elif self.operator == '<=':
            return operand1 <= operand2
        elif self.operator == '=':
            return operand1 == operand2
        elif self.operator == '>=':
            return operand1 >= operand2
        elif self.operator == '>':
            return operand1 > operand2
        elif self.operator == '!':
            return operand1 != operand2

        return False

