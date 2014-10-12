import Command
from PrettyPrinter import pretty_print
from Utils import convert_todo_number, is_valid_priority

class PriorityCommand(Command.Command):
    def __init__(self, p_args, p_todolist,
                 p_out=lambda a: None,
                 p_err=lambda a: None,
                 p_prompt=lambda a: None):
        super(PriorityCommand, self).__init__(p_args, p_todolist, p_out, p_err, p_prompt)
        self.number = convert_todo_number(self.argument(0))
        self.todo = self.todolist.todo(self.number)
        self.priority = self.argument(1)

    def execute(self):
        if is_valid_priority(self.priority):
            old_priority = self.todo.priority()
            self.todolist.set_priority(self.number, self.priority)

            self.out("Priority changed from %s to %s" % (old_priority, self.priority))
            self.out(pretty_print(self.todo))
        else:
            self.error("Invalid priority given.")
