import CommandTest
import TestFacilities
import ListProjectCommand

class ListProjectCommandTest(CommandTest.CommandTest):
    def test_projects1(self):
        todolist = TestFacilities.load_file_to_todolist("data/TodoListTest.txt")
        command = ListProjectCommand.ListProjectCommand([""], todolist, self.out, self.error)
        command.execute()

        self.assertEquals(self.output,"Project1\nProject2\n")
        self.assertFalse(self.errors)

    def test_projects2(self):
        todolist = TestFacilities.load_file_to_todolist("data/TodoListTest.txt")
        command = ListProjectCommand.ListProjectCommand(["aaa"], todolist, self.out, self.error)
        command.execute()

        self.assertEquals(self.output,"Project1\nProject2\n")
        self.assertFalse(self.errors)
