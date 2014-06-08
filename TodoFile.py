"""
This module deals with todo.txt files.
"""

import Todo

class TodoFile(object):
    """
    This class represents a todo.txt file, which can be read from or written
    to.
    """

    path = ""
    def __init__(self, p_path):
        self.path = p_path

    def read(self):
        """ Reads the todo.txt file and returns a list of todo items.  """
        todos = []

        todofile = open(self.path, 'r')

        for line in todofile:
            todos.append(Todo.Todo(line))

        todofile.close()
        return todos

    def write(self, p_todos):
        """
        Writes all the todo items in the p_todos array to a todo.txt file.
        """

        todofile = open(self.path, 'w')

        for todo in p_todos:
            todofile.write(todo.src + "\n")

        todofile.close()
