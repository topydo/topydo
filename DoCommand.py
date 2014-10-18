import re

import Command
from PrettyPrinter import *
from Recurrence import advance_recurring_todo
from TodoList import InvalidTodoException
from Utils import convert_todo_number, InvalidTodoNumberException

class DoCommand(Command.Command):
    def __init__(self, p_args, p_todolist,
                 p_out=lambda a: None,
                 p_err=lambda a: None,
                 p_prompt=lambda a: None):
        super(DoCommand, self).__init__(p_args, p_todolist, p_out, p_err, p_prompt)

        self.number = None

        try:
            self.number = convert_todo_number(self.argument(0))
            self.todo = self.todolist.todo(self.number)
        except (InvalidTodoNumberException, InvalidTodoException):
            self.todo = None

    def _complete_children(self):
            children = sorted([t for t in self.todolist.children(self.todo) if not t.is_completed()])
            if children:
                self.out("\n".join(pretty_print_list(children, [self.todolist.pp_number()])))

                confirmation = self.prompt("Also mark subtasks as done? [n] ")

                if re.match('^y(es)?$', confirmation, re.I):
                    for child in children:
                        self.todolist.set_todo_completed(child)
                        self.out(pretty_print(child))

    def _handle_recurrence(self):
        if self.todo.has_tag('rec'):
            new_todo = advance_recurring_todo(self.todo)
            self.todolist.add_todo(new_todo)
            self.out(pretty_print(new_todo, [self.todolist.pp_number()]))

    def execute(self):
        if not self.number:
            self.error(self.usage())
        elif self.todo and not self.todo.is_completed():
            self._complete_children()
            self._handle_recurrence()
            self.todolist.set_todo_completed(self.todo)
            self.out(pretty_print(self.todo))
        elif not self.todo:
            self.error("Invalid todo number given.")
        else:
            self.error("Todo has already been completed.")
