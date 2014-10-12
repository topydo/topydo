"""
This module deals with todo.txt files.
"""

class TodoFile(object):
    """
    This class represents a todo.txt file, which can be read from or written
    to.
    """

    def __init__(self, p_path):
        self.path = p_path

    def read(self):
        """ Reads the todo.txt file and returns a list of todo items.  """
        todos = []
        try:
            todofile = open(self.path, 'r')
            todos = todofile.readlines()
            todofile.close()
        except IOError:
            pass

        return todos

    def write(self, p_todos):
        """
        Writes all the todo items in the p_todos array to a todo.txt file.
        """

        todofile = open(self.path, 'w')

        if p_todos is list:
            for todo in p_todos:
                todofile.write(str(todo))
        else:
            todofile.write(p_todos)

        todofile.close()
