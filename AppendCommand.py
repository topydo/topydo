import Command
from Utils import convert_todo_number

class AppendCommand(Command.Command):
    def __init__(self, p_args, p_todolist):
        super(AppendCommand, self).__init__(p_args, p_todolist)

    def execute(self):
        number = convert_todo_number(self.argument(0))
        text = self.argument(1)

        self.todolist.append(number, text)

        return True
