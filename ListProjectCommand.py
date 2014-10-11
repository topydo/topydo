import Command

class ListProjectCommand(Command.Command):
    def __init__(self, p_args, p_todolist):
        super(ListProjectCommand, self).__init__(p_args, p_todolist)

    def execute(self):
        for p in sorted(self.todolist.projects()):
            print p
