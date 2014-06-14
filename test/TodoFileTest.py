import unittest

from TestFacilities import load_file

class TodoFileTest(unittest.TestCase):
    def test_empty_file(self):
        todofile = load_file('data/TodoFileTest1.txt')

        self.assertEquals(len(todofile), 0)
