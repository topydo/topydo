class Command(object):
    def __init__(self, p_args, p_todolist):
        self.args = p_args
        self.todolist = p_todolist

    def execute(self):
        """ The command to execute. """
        return False
