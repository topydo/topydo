import Command

class ListContextCommand(Command.Command):
    def __init__(self, p_args, p_todolist):
        super(ListContextCommand, self).__init__(p_args, p_todolist)

    def execute(self):
        for context in sorted(self.todolist.contexts()):
            self.out(context)
