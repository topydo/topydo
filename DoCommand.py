import re

import Command
from PrettyPrinter import *
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
                pretty_print_list(children, [pp_number])

                confirmation = raw_input("Also mark subtasks as done? [n] "); # FIXME

                if re.match('^y(es)?$', confirmation, re.I):
                    for child in children:
                        self.todolist.set_todo_completed(child)
                        self.out(pretty_print(child, [pp_number]))

    def _handle_recurrence(self):
        if self.todo.has_tag('rec'):
            new_todo = advance_recurring_todo(self.todo)
            self.todolist.add_todo(new_todo)
            self.out(pretty_print(new_todo, [pp_number]))

    def execute(self):
        if self.todo and not self.todo.is_completed():
            self._complete_children()
            self._handle_recurrence()
            self.todolist.set_todo_completed(self.number)
