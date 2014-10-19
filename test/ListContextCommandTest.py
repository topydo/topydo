import CommandTest
import TestFacilities
import ListContextCommand

class ListContextCommandTest(CommandTest.CommandTest):
    def test_contexts1(self):
        todolist = TestFacilities.load_file_to_todolist("data/TodoListTest.txt")
        command = ListContextCommand.ListContextCommand([""], todolist, self.out, self.error)
        command.execute()

        self.assertEquals(self.output,"Context1\nContext2\n")
        self.assertFalse(self.errors)

    def test_contexts2(self):
        todolist = TestFacilities.load_file_to_todolist("data/TodoListTest.txt")
        command = ListContextCommand.ListContextCommand(["aaa"], todolist, self.out, self.error)
        command.execute()

        self.assertEquals(self.output,"Context1\nContext2\n")
        self.assertFalse(self.errors)
