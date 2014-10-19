import CommandTest
import ListCommand
import TestFacilities

class ListCommandTest(CommandTest.CommandTest):
    def setUp(self):
        self.todolist = TestFacilities.load_file_to_todolist("data/ListCommandTest.txt")

    def test_list1(self):
        command = ListCommand.ListCommand([""], self.todolist, self.out, self.error)
        command.execute()

        self.assertFalse(self.todolist.is_dirty())
        self.assertEquals(self.output, "  1 (C) Foo @Context2 Not@Context +Project1 Not+Project\n  4 (C) Drink beer @ home\n  5 (C) 13 + 29 = 42\n  2 (D) Bar @Context1 +Project2 p:1\n")
        self.assertEquals(self.errors, "")

    def test_list3(self):
        command = ListCommand.ListCommand(["Context1"], self.todolist, self.out, self.error)
        command.execute()

        self.assertFalse(self.todolist.is_dirty())
        self.assertEquals(self.output, "  2 (D) Bar @Context1 +Project2 p:1\n")
        self.assertEquals(self.errors, "")

    def test_list4(self):
        command = ListCommand.ListCommand(["-x", "Context1"], self.todolist, self.out, self.error)
        command.execute()

        self.assertFalse(self.todolist.is_dirty())
        self.assertEquals(self.output, "  3 (C) Baz @Context1 +Project1 key:value id:1\n  2 (D) Bar @Context1 +Project2 p:1\n")
        self.assertEquals(self.errors, "")

    def test_list5(self):
        command = ListCommand.ListCommand(["-x"], self.todolist, self.out, self.error)
        command.execute()

        self.assertFalse(self.todolist.is_dirty())
        self.assertEquals(self.output, "  1 (C) Foo @Context2 Not@Context +Project1 Not+Project\n  3 (C) Baz @Context1 +Project1 key:value id:1\n  4 (C) Drink beer @ home\n  5 (C) 13 + 29 = 42\n  2 (D) Bar @Context1 +Project2 p:1\n")
        self.assertEquals(self.errors, "")

    def test_list6(self):
        command = ListCommand.ListCommand(["Project3"], self.todolist, self.out, self.error)
        command.execute()

        self.assertFalse(self.todolist.is_dirty())
        self.assertEquals(self.output, "")
        self.assertEquals(self.errors, "")
