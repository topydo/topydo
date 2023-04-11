import unittest
from .command_testcase import CommandTest
from topydo.commands.ClearCommand import ClearCommand
import os


class ClearCommandTest(CommandTest):
    def test_clear_command(self):
        command = ClearCommand([], None, self.out, self.error)
        command.execute()

        self.assertEqual(self.output, '')
        self.assertFalse(self.errors)

        os.system('topydo clr > clr_cmd_output.txt')
        clr_cmd_output = str(open('clr_cmd_output.txt').readlines())

        self.assertIn('\\x1b[H\\x1b[2J', clr_cmd_output)

        os.remove('clr_cmd_output.txt')

    def test_clear_name(self):
        name = ClearCommand.name()

        self.assertEqual(name, 'clear')

    def test_help(self):
        command = ClearCommand(['help'], None, self.out, self.error)
        command.execute()

        self.assertEqual(self.output, '')
        self.assertEqual(self.errors, command.usage() + '\n\n' + command.help() + '\n')


if __name__ == '__main__':
    unittest.main()
