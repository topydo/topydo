import Todo
import TodoFile

def load_file(p_filename):
    """
    Loads a todo file from the given filename and returns a list of todos.
    """
    todofile = TodoFile.TodoFile(p_filename)
    return [Todo.Todo(src) for src in todofile.read()]

def todolist_to_string(p_list):
    """ Converts a todo list to a single string. """
    return '\n'.join([str(t) for t in p_list])
