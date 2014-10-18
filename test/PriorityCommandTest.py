import CommandTest
import PriorityCommand
import TodoList

class PriorityCommandTest(CommandTest.CommandTest):
    def setUp(self):
        todos = [
            "(A) Foo",
            "Bar",
        ]

        self.todolist = TodoList.TodoList(todos)

    def test_set_prio1(self):
        command = PriorityCommand.PriorityCommand(["1", "B"], self.todolist, self.out, self.error)
        command.execute()

        self.assertTrue(self.todolist.is_dirty())
        self.assertEquals(self.output, "Priority changed from A to B\n(B) Foo\n")
        self.assertEquals(self.errors, "")

    def test_set_prio2(self):
        command = PriorityCommand.PriorityCommand(["2", "Z"], self.todolist, self.out, self.error)
        command.execute()

        self.assertTrue(self.todolist.is_dirty())
        self.assertEquals(self.output, "Priority set to Z.\n(Z) Bar\n")
        self.assertEquals(self.errors, "")

    def test_invalid1(self):
        command = PriorityCommand.PriorityCommand(["99", "A"], self.todolist, self.out, self.error)
        command.execute()

        self.assertFalse(self.todolist.is_dirty())
        self.assertFalse(self.output)
        self.assertEquals(self.errors, "Invalid todo number given.\n")

    def test_invalid2(self):
        command = PriorityCommand.PriorityCommand(["1", "ZZ"], self.todolist, self.out, self.error)
        command.execute()

        self.assertFalse(self.todolist.is_dirty())
        self.assertFalse(self.output)
        self.assertEquals(self.errors, "Invalid priority given.\n")

    def test_invalid3(self):
        command = PriorityCommand.PriorityCommand(["A"], self.todolist, self.out, self.error)
        command.execute()

        self.assertFalse(self.todolist.is_dirty())
        self.assertFalse(self.output)
        self.assertEquals(self.errors, command.usage() + "\n")

    def test_invalid4(self):
        command = PriorityCommand.PriorityCommand(["1"], self.todolist, self.out, self.error)
        command.execute()

        self.assertFalse(self.todolist.is_dirty())
        self.assertFalse(self.output)
        self.assertEquals(self.errors, command.usage() + "\n")

    def test_empty(self):
        command = PriorityCommand.PriorityCommand([], self.todolist, self.out, self.error)
        command.execute()

        self.assertFalse(self.todolist.is_dirty())
        self.assertFalse(self.output)
        self.assertEquals(self.errors, command.usage() + "\n")
