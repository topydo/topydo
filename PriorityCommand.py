from Command import *
from PrettyPrinter import pretty_print
from TodoList import InvalidTodoException
from Utils import *

class PriorityCommand(Command):
    def __init__(self, p_args, p_todolist,
                 p_out=lambda a: None,
                 p_err=lambda a: None,
                 p_prompt=lambda a: None):
        super(PriorityCommand, self).__init__(p_args, p_todolist, p_out, p_err, p_prompt)

    def execute(self):
        number = None
        priority = None
        try:
            number = convert_todo_number(self.argument(0))
            priority = self.argument(1)
            todo = self.todolist.todo(number)

            if is_valid_priority(priority):
                old_priority = todo.priority()
                self.todolist.set_priority(todo, priority)

                if old_priority and priority:
                    self.out("Priority changed from %s to %s" % (old_priority, priority))
                else:
                    self.out("Priority set to %s." % priority)

                self.out(pretty_print(todo))
            else:
                self.error("Invalid priority given.")
        except InvalidCommandArgument:
            self.error(self.usage())
        except (InvalidTodoNumberException, InvalidTodoException):
            if number and priority:
                self.error( "Invalid todo number given.")
            else:
                self.error(self.usage())
