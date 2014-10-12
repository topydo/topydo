import Command
from PrettyPrinter import pretty_print
from Utils import convert_todo_number

class AppendCommand(Command.Command):
    def __init__(self, p_args, p_todolist,
                 p_out=lambda a: None,
                 p_err=lambda a: None,
                 p_prompt=lambda a: None):
        super(AppendCommand, self).__init__(p_args, p_todolist, p_out, p_err, p_prompt=lambda a: None)

    def execute(self):
        number = convert_todo_number(self.argument(0))
        text = self.argument(1)

        self.todolist.append(number, text)

        self.out(pretty_print(self.todo, [self.todolist.pp_number]))
