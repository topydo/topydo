from topydo.lib.Command import Command
import os


class ClearCommand(Command):
    def __init__(self, p_args, p_todolist, #pragma: no branch
                 p_out=lambda a: None,
                 p_err=lambda a: None,
                 p_prompt=lambda a: None):
        super().__init__(p_args, p_todolist, p_out, p_err, p_prompt)

    def execute(self):
        if not super().execute():
            return False

        os.environ['TERM'] = 'xterm-256color'
        os.system('clear' if os.name == 'posix' else 'cls')

    def usage(self):
        return """Synopsis: clr"""

    def help(self):
        return """Clears terminal screen."""
