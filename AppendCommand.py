from Command import *
from PrettyPrinter import pretty_print
import TodoList
from Utils import convert_todo_number, InvalidTodoNumberException

class AppendCommand(Command):
    def __init__(self, p_args, p_todolist,
                 p_out=lambda a: None,
                 p_err=lambda a: None,
                 p_prompt=lambda a: None):
        super(AppendCommand, self).__init__(p_args, p_todolist, p_out, p_err, p_prompt=lambda a: None)

    def execute(self):
        try:
            number = convert_todo_number(self.argument(0))
            text = " ".join(self.args[1:])

            if text:
                todo = self.todolist.todo(number)
                self.todolist.append(todo, text)
                self.out(pretty_print(todo, [self.todolist.pp_number()]))
            else:
                self.error(self.usage())
        except (InvalidCommandArgument, InvalidTodoNumberException):
            self.error(self.usage())
        except TodoList.InvalidTodoException:
            self.error("Invalid todo number given.")

