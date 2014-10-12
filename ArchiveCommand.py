import Command
import Config

class ArchiveCommand(Command.Command):
    def __init__(self, p_todolist, p_archive_list):
        super(ArchiveCommand, self).__init__([], p_todolist)
        self.archive = p_archive_list

    def execute(self):
        for todo in [t for t in self.todolist.todos() if t.is_completed()]:
            self.archive.add_todo(todo)
            self.todolist.delete(self.todolist.number(todo))
