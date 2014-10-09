import re

import Command
from Utils import convert_todo_number

class PriorityCommand(Command.Command):
    def __init__(self, p_args, p_todolist):
        super(PriorityCommand, self).__init__(p_args, p_todolist)
        self.number = convert_todo_number(self.argument(0))
        self.todo = self.todolist.todo(self.number)
        self.priority = self.argument(1)

    def execute(self):
        if re.match('^[A-Z]$', self.priority):
            old_priority = self.todo.priority()
            self.todolist.set_priority(self.number, self.priority)

            print "Priority changed from %s to %s" \
                % (old_priority, self.priority) # FIXME
            # self.print_todo(number) # FIXME
        else:
            # error("Invalid priority given.") # TODO
            pass
