import AppendCommand
import CommandTest
import TodoList

class AppendCommandTest(CommandTest.CommandTest):
    def setUp(self):
        self.todolist = TodoList.TodoList([])
        self.todolist.add("Foo")

    def test_append1(self):
        command = AppendCommand.AppendCommand([1, "Bar"], self.todolist, self.out, self.err)
        command.execute()

        self.assertEqual(self.output, "  1 Foo Bar\n")
        self.assertEqual(self.errors, "")

    def test_append2(self):
        command = AppendCommand.AppendCommand([2, "Bar"], self.todolist, self.out, self.err)
        command.execute()

        self.assertEqual(self.output, "")
        self.assertEqual(self.errors, "Invalid todo number given.\n")

    def test_append3(self):
        command = AppendCommand.AppendCommand([1, ""], self.todolist, self.out, self.err)
        command.execute()

        self.assertEqual(self.output, "")
        self.assertEqual(self.output, "")

    def test_append4(self):
        command = AppendCommand.AppendCommand([1], self.todolist, self.out, self.err)
        command.execute()

        self.assertEqual(self.output, "")
        self.assertEqual(self.errors, command.usage() + "\n")

    def test_append5(self):
        command = AppendCommand.AppendCommand([1, "Bar", "Baz"], self.todolist, self.out, self.err)
        command.execute()

        self.assertEqual(self.output, "  1 Foo Bar Baz\n")
        self.assertEqual(self.errors, "")

    def test_append6(self):
        command = AppendCommand.AppendCommand([], self.todolist, self.out, self.err)
        command.execute()

        self.assertEqual(self.output, "")
        self.assertEqual(self.errors, command.usage() + "\n")

    def test_append7(self):
        command = AppendCommand.AppendCommand(["Bar"], self.todolist, self.out, self.err)
        command.execute()

        self.assertEqual(self.output, "")
        self.assertEqual(self.errors, command.usage() + "\n")
