import unittest

class CommandTest(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(CommandTest, self).__init__(*args, **kwargs)
        self.output = ""
        self.errors = ""

    def out(self, p_output):
        self.output += p_output + "\n";

    def error(self, p_error):
        self.errors += p_error + "\n";
