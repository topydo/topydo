from datetime import date

import CommandTest
import DoCommand
import TodoList

def _yes_prompt(self):
    return "y"

def _no_prompt(self):
    return "n"

class DoCommandTest(CommandTest.CommandTest):
    def setUp(self):
        self.todolist = TodoList.TodoList([])
        self.today = date.today().isoformat()

        self.todolist.add("Foo id:1")
        self.todolist.add("Bar p:1")
        self.todolist.add("Baz p:1")
        self.todolist.add("Recurring! rec:1d")
        self.todolist.add("x 2014-10-18 Already complete")

    def test_do1(self):
        command = DoCommand.DoCommand(["3"], self.todolist, self.out, self.error, _no_prompt)
        command.execute()

        self.assertEquals(self.output, "x %s Baz p:1\n" % self.today)
        self.assertEquals(self.errors, "")

    def test_do_children1(self):
        command = DoCommand.DoCommand(["1"], self.todolist, self.out, self.error, _yes_prompt)
        command.execute()

        result = "  2 Bar p:1\n  3 Baz p:1\nx %s Bar p:1\nx %s Baz p:1\nx %s Foo id:1\n" % (self.today, self.today, self.today)

        self.assertEquals(self.output, result)
        self.assertEquals(self.errors, "")

    def test_do_children2(self):
        command = DoCommand.DoCommand(["1"], self.todolist, self.out, self.error, _no_prompt)
        command.execute()

        result = "  2 Bar p:1\n  3 Baz p:1\nx %s Foo id:1\n" % self.today

        self.assertEquals(self.output, result)
        self.assertEquals(self.errors, "")

    def test_recurrence(self):
        command = DoCommand.DoCommand(["4"], self.todolist, self.out, self.error)
        command.execute()

        result = "  6 2014-10-18 Recurring! rec:1d due:2014-10-19\nx 2014-10-18 Recurring! rec:1d\n"

        self.assertEquals(self.output, result)
        self.assertEquals(self.errors, "")
        self.assertEquals(self.todolist.count(), 6)
        self.assertTrue(self.todolist.todo(4).is_completed())
        self.assertFalse(self.todolist.todo(6).is_completed())

    def test_invalid1(self):
        command = DoCommand.DoCommand(["99"], self.todolist, self.out, self.error)
        command.execute()

        self.assertFalse(self.output)
        self.assertEquals(self.errors, "Invalid todo number given.\n")

    def test_invalid2(self):
        command = DoCommand.DoCommand(["A"], self.todolist, self.out, self.error)
        command.execute()

        self.assertFalse(self.output)
        self.assertEquals(self.errors, command.usage() + "\n")

    def test_already_complete(self):
        command = DoCommand.DoCommand(["5"], self.todolist, self.out, self.error)
        command.execute()

        self.assertFalse(self.output)
        self.assertEquals(self.errors, "Todo has already been completed.\n")

    def test_empty(self):
        command = DoCommand.DoCommand([""], self.todolist, self.out, self.error)
        command.execute()

        self.assertFalse(self.output)
        self.assertEquals(self.errors, command.usage() + "\n")
