class InvalidCommandArgument(Exception):
    pass

class Command(object):
    def __init__(self, p_args, p_todolist,
                 p_out=lambda a: None,
                 p_err=lambda a: None,
                 p_prompt=lambda a: None):
        """
        Sets up the basic properties for executing a subcommand.

        p_args is a list of arguments that can be passed to this subcommand.
        These can be retrieved with argument(), or the existence of an argument
        using argumentShift().

        p_todolist is a reference to the todolist instance to operate on.

        p_out is a function to be called to print (standard) output. Defaults
        to a noop.

        p_err is a function to be called to print errors. Defaults to a noop.

        p_prompt is a function that accepts a prompt string as its own argument
        and returns the answer to that prompt (normally entered by the user in
        some way). The default is a noop prompt.
        """
        self.args = p_args
        self.todolist = p_todolist

        # inputs and outputs
        self.out = p_out
        self.error = p_err
        self.prompt = p_prompt

    def execute(self):
        """
        Execute the command.

        Returns True when the command succeeded or False on failure.
        """
        return False

    def argument(self, p_number, p_error=None):
        """ Retrieves a value from the argument list at the given position. """
        value = None
        try:
            value = self.args[p_number]
        except IndexError:
            raise InvalidCommandArgument

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

