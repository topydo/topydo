import unittest

import topydo


class Test_Setup(unittest.TestCase):

    def test_we_live(self):
        '''Test we should *always* pass'''
        pass

    def test_version(self):
        '''Version is available'''
        self.assertIsNotNone(topydo.__version__)


if __name__ == '__main__':
    unittest.main()
