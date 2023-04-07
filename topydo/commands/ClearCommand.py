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

        os.environ['TERM'] = 'xterm'
        os.system("cls" if os.name == "nt" else "clear")
        # print('before try statement')
        # try:
        #     print('you have a mac!')
        #     os.system('clear')
        # except os.error:
        #     print('debug line')
        # else:
        #     print('you have windows!')
        #     os.system('cls')

    def usage(self):
        return """Synopsis: clr"""

    def help(self):
        return """Clears terminal screen."""
