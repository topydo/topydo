import re

import Command
from Recurrence import advance_recurring_todo
from Utils import convert_todo_number

class DoCommand(Command.Command):
    def __init__(self, p_args, p_todolist):
        super(DoCommand, self).__init__(p_args, p_todolist)
        self.number = convert_todo_number(self.argument(0))
        self.todo = self.todolist.todo(self.number)

    def _complete_children(self):
            children = [t.attributes['number'] for t in self.todolist.children(self.number) if not t.is_completed()]
            if children:
                for child in children:
                    # self.print_todo(child) # FIXME
                    pass

                confirmation = raw_input("Also mark subtasks as done? [n] "); # FIXME

                if re.match('^y(es)?$', confirmation, re.I):
                    for child in children:
                        self.todolist.set_todo_completed(child)
                        # self.print_todo(child) # FIXME


    def _handle_recurrence(self):
        if self.todo.has_tag('rec'):
            new_todo = advance_recurring_todo(self.todo)
            self.todolist.add_todo(new_todo)
            # self.print_todo(self.todolist.count()) # FIXME

    def execute(self):
        if self.todo and not self.todo.is_completed():
            self._complete_children()
            self._handle_recurrence()
            self.todolist.set_todo_completed(self.number)
