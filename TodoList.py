"""
A list of todo items.
"""

import re

from PrettyPrinter import pretty_print
import Todo
import View

class TodoList(object):
    """
    Provides operations for a todo list, such as adding items, removing them,
    etc.

    The list is usually a complete list found in the program's input (e.g. a
    todo.txt file), not an arbitrary set of todo items.
    """

    def __init__(self, p_todostrings):
        """
        Should be given a list of strings, each element a single todo string.
        The string will be parsed.
        """
        self._todos = []
        for string in p_todostrings:
            self.add(string)

    def todo(self, p_number):
        """
        The _todos list has the same order as in the backend store (usually
        a todo.txt file. The user refers to the first task as number 1, so use
        index 0, etc.
        """
        result = None
        try:
            result = self._todos[p_number - 1]
        except IndexError:
            result = None

        return result

    def add(self, p_src):
        """
        Given a todo string, parse it and put it to the end of the list.
        """

        if re.search(r'\S', p_src):
            number = len(self._todos) + 1
            todo = Todo.Todo(p_src, number)
            self._todos.append(todo)

    def delete(self, p_number):
        """ Deletes a todo item from the list. """
        try:
            del self._todos[p_number - 1]
        except IndexError:
            pass # just ignore it

    def count(self):
        """ Returns the number of todos on this list. """
        return len(self._todos)

    def append(self, p_number, p_string):
        """
        Appends a text to the todo, specified by its number.
        The todo will be parsed again, such that tags and projects in de
        appended string are processed.
        """
        if len(p_string) > 0:
            todo = self.todo(p_number)
            new_text = todo.source() + ' ' + p_string
            todo.set_text(new_text)

    def projects(self):
        """ Returns a set of all projects in this list. """
        result = set()
        for todo in self._todos:
            projects = todo.projects()
            result = result.union(projects)

        return result

    def contexts(self):
        """ Returns a set of all contexts in this list. """
        result = set()
        for todo in self._todos:
            contexts = todo.contexts()
            result = result.union(contexts)

        return result

    def view(self, p_sorter, p_filters):
        """
        Constructs a view of the todo list.

        A view is a sorted and filtered todo list, where the properties are
        defined by the end user. Todos is this list should not be modified,
        modifications should occur through this class.
        """
        return View.View(p_sorter, p_filters, self._todos)

    def __str__(self):
        return '\n'.join(pretty_print(self._todos))

