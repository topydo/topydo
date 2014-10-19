import ArchiveCommand
import CommandTest
import TestFacilities
import TodoList

class ArchiveCommandTest(CommandTest.CommandTest):
    def test_archive(self):
        todolist = TestFacilities.load_file_to_todolist("data/ArchiveCommandTest.txt")
        archive = TodoList.TodoList([])

        command = ArchiveCommand.ArchiveCommand(todolist, archive)
        command.execute()

        self.assertTrue(todolist.is_dirty())
        self.assertTrue(archive.is_dirty())
        self.assertEquals(str(todolist), "x Not complete\n(C) Active")
        self.assertEquals(str(archive), "x 2014-10-19 Complete\nx 2014-10-20 Another one complete")

