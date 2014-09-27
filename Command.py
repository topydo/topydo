class Command(object):
    def __init__(self, p_args, p_todolist):
        self.args = p_args
        self.todolist = p_todolist

    def execute(self):
        """ The command to execute. """
        return False

    def argument(self, p_number):
        """ Retrieves a value from the argument list. """
        try:
            value = self.args[p_number]
        except IndexError:
            self.usage()

        return value

    def usage(self):
        return ""
