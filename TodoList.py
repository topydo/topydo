"""
A list of todo items.
"""

class TodoList(object):
    """
    Provides operations for a todo list, such as adding items, removing them,
    etc.

    The list is usually a complete list found in the program's input (e.g. a
    todo.txt file), not an arbitrary set of todo items.
    """
    _todos = []

    def __init__(self, todos):
        """
        Should be given a list of Todo objects (already read and parsed from
        file or standard input.
        """
        self._todos = todos

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

    def todos(self):
        """ Returns the list of all todos. """
        return self._todos

    def add(self, p_item):
        """
        Given a Todo(Base) item, add it to the end of the list.
        """
        self._todos.append(p_item)

    def delete(self, p_number):
        """ Deletes a todo item from the list. """
        del self._todos[p_number - 1]

    def append(self, p_number, p_string):
        """
        Appends a text to the todo, specified by its number.
        The todo will be parsed again, such that tags and projects in de
        appended string are processed.
        """
        if len(p_string) > 0:
            todo = self.todo(p_number)
            new_text = todo.text() + ' ' + p_string
            todo.set_text(new_text)

    def set_completed(self, p_number):
        """ Marks the todo with the given number as complete. """
        self.todo(p_number).set_completed()

    def projects(self):
        """ Returns a set of all projects in this list. """
        result = set()
        for todo in self._todos:
            projects = todo.projects()
            result = result.union(projects)

    def contexts(self):
        """ Returns a set of all contexts in this list. """
        result = set()
        for todo in self._todos:
            contexts = todo.contexts()
            result = result.union(contexts)

    def set_priority(self, p_number, p_priority):
        """ Sets the priority of the todo with the given number. """
        self.todo(p_number).set_priority(p_priority)

    def view(self, p_sorter, p_filter):
        """
        Constructs a view of the todo list.

        A view is a sorted and filtered todo list, where the properties are
        defined by the end user. Todos is this list should not be modified,
        modifications should occur through this class.
        """
        return p_filter.filter(p_sorter.sort(self._todos))

    def __print__(self):
        result = ""
        for todo in self._todos:
            result = "%s" % todo

        return result

