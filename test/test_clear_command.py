import unittest
from .command_testcase import CommandTest
from topydo.commands.ClearCommand import ClearCommand
import os

"""This module contains all the test functions for the clear command """
class ClearCommandTest(CommandTest):
    def test_clear_command(self):
        """This function tests the clear command """
        command = ClearCommand([], None, self.out, self.error)
        command.execute()

        self.assertEqual(self.output, '')
        self.assertFalse(self.errors)

        os.system('topydo clr > clr_cmd_output.txt')
        clr_cmd_output = str(open('clr_cmd_output.txt').readlines())

        self.assertIn('\\x1b[H\\x1b[2J', clr_cmd_output)

        os.remove('clr_cmd_output.txt')

    def test_clear_name(self):
        """ This test function clears the command name """

        name = ClearCommand.name()

        self.assertEqual(name, 'clear')

    def test_help(self):
        """ This function tests the help command """

        command = ClearCommand(['help'], None, self.out, self.error)
        command.execute()

        self.assertEqual(self.output, '')
        self.assertEqual(self.errors, command.usage() + '\n\n' + command.help() + '\n')


if __name__ == '__main__':
    unittest.main()
