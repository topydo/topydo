import unittest

from Utils import escape_ansi

class CommandTest(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(CommandTest, self).__init__(*args, **kwargs)
        self.output = ""
        self.errors = ""

    def out(self, p_output):
        if p_output:
            self.output += escape_ansi(p_output + "\n")

    def error(self, p_error):
        if p_error:
            self.errors += escape_ansi(p_error + "\n")
