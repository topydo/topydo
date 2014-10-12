import Command

class ListContextCommand(Command.Command):
    def __init__(self, p_args, p_todolist,
                 p_out=lambda a: None,
                 p_err=lambda a: None,
                 p_prompt=lambda a: None):
        super(ListContextCommand, self).__init__(p_args, p_todolist, p_out, p_err, p_prompt)

    def execute(self):
        for context in sorted(self.todolist.contexts()):
            self.out(context)
