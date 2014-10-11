class Command(object):
    def __init__(self, p_args, p_todolist):
        self.args = p_args
        self.todolist = p_todolist

        self.output = []
        self.errors = []

    def execute(self):
        """ The command to execute. """
        return (False, None, None)

    def argument(self, p_number):
        """ Retrieves a value from the argument list. """
        try:
            value = self.args[p_number]
        except IndexError:
            self.usage()

        return value

    def argumentShift(self, p_expr):
        """
        Returns true when the first argument equals the given expression.
        """
        if len(self.args) and self.argument(0) == p_expr:
            del self.args[0]
            return True

        return False

    def usage(self):
        return "No usage text defined for this command."

    def out(self, p_text): # TODO: make private
        self.output.append(p_text)

    def error(self, p_text): # TODO: make private
        self.errors.append(p_text)
