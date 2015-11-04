# Topydo - A todo.txt client written in Python.
# Copyright (C) 2014 - 2015 Bram Schoenmakers <me@bramschoenmakers.nl>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

""" Tests for the colorscheme functionality. """

import unittest

from test.topydo_testcase import TopydoTest
from topydo.lib.Colors import NEUTRAL_COLOR, Colors
from topydo.lib.Config import config


class ColorsTest(TopydoTest):
    def test_project_color1(self):
        config(p_overrides={('colorscheme', 'project_color'): '2'})
        color = Colors().get_project_color()

        self.assertEqual(color, '\033[1;38;5;2m')

    def test_project_color2(self):
        config(p_overrides={('colorscheme', 'project_color'): 'Foo'})
        color = Colors().get_project_color()

        self.assertEqual(color, NEUTRAL_COLOR)

    def test_project_color3(self):
        config(p_overrides={('colorscheme', 'project_color'): 'yellow'})
        color = Colors().get_project_color()

        self.assertEqual(color, '\033[1;33m')

    def test_project_color4(self):
        config(p_overrides={('colorscheme', 'project_color'): '686'})
        color = Colors().get_project_color()

        self.assertEqual(color, NEUTRAL_COLOR)

    def test_context_color1(self):
        config(p_overrides={('colorscheme', 'context_color'): '35'})
        color = Colors().get_context_color()

        self.assertEqual(color, '\033[1;38;5;35m')

    def test_context_color2(self):
        config(p_overrides={('colorscheme', 'context_color'): 'Bar'})
        color = Colors().get_context_color()

        self.assertEqual(color, NEUTRAL_COLOR)

    def test_context_color3(self):
        config(p_overrides={('colorscheme', 'context_color'): 'magenta'})
        color = Colors().get_context_color()

        self.assertEqual(color, '\033[1;35m')

    def test_context_color4(self):
        config(p_overrides={('colorscheme', 'context_color'): '392'})
        color = Colors().get_context_color()

        self.assertEqual(color, NEUTRAL_COLOR)

    def test_metadata_color1(self):
        config(p_overrides={('colorscheme', 'metadata_color'): '128'})
        color = Colors().get_metadata_color()

        self.assertEqual(color, '\033[1;38;5;128m')

    def test_metadata_color2(self):
        config(p_overrides={('colorscheme', 'metadata_color'): 'Baz'})
        color = Colors().get_metadata_color()

        self.assertEqual(color, NEUTRAL_COLOR)

    def test_metadata_color3(self):
        config(p_overrides={('colorscheme', 'metadata_color'): 'light-red'})
        color = Colors().get_metadata_color()

        self.assertEqual(color, '\033[1;1;31m')

    def test_metadata_color4(self):
        config(p_overrides={('colorscheme', 'metadata_color'): '777'})
        color = Colors().get_metadata_color()

        self.assertEqual(color, NEUTRAL_COLOR)

    def test_link_color1(self):
        config(p_overrides={('colorscheme', 'link_color'): '77'})
        color = Colors().get_link_color()

        self.assertEqual(color, '\033[4;38;5;77m')

    def test_link_color2(self):
        config(p_overrides={('colorscheme', 'link_color'): 'FooBar'})
        color = Colors().get_link_color()

        self.assertEqual(color, NEUTRAL_COLOR)

    def test_link_color3(self):
        config(p_overrides={('colorscheme', 'link_color'): 'red'})
        color = Colors().get_link_color()

        self.assertEqual(color, '\033[4;31m')

    def test_link_color4(self):
        config(p_overrides={('colorscheme', 'link_color'): '777'})
        color = Colors().get_link_color()

        self.assertEqual(color, NEUTRAL_COLOR)

    def test_priority_color1(self):
        config("test/data/ColorsTest1.conf")
        color = Colors().get_priority_colors()

        self.assertEqual(color['A'], '\033[0;38;5;1m')
        self.assertEqual(color['B'], '\033[0;38;5;2m')
        self.assertEqual(color['C'], '\033[0;38;5;3m')

    def test_priority_color2(self):
        config("test/data/ColorsTest2.conf")
        color = Colors().get_priority_colors()

        self.assertEqual(color['A'], '\033[0;35m')
        self.assertEqual(color['B'], '\033[0;1;36m')
        self.assertEqual(color['C'], '\033[0;37m')

    def test_priority_color3(self):
        config("test/data/ColorsTest3.conf")
        color = Colors().get_priority_colors()

        self.assertEqual(color['A'], '\033[0;35m')
        self.assertEqual(color['B'], '\033[0;1;36m')
        self.assertEqual(color['Z'], NEUTRAL_COLOR)
        self.assertEqual(color['D'], '\033[0;31m')
        self.assertEqual(color['C'], '\033[0;38;5;7m')

    def test_priority_color4(self):
        config("test/data/ColorsTest4.conf")
        color = Colors().get_priority_colors()

        self.assertEqual(color['A'], NEUTRAL_COLOR)
        self.assertEqual(color['B'], NEUTRAL_COLOR)
        self.assertEqual(color['C'], NEUTRAL_COLOR)

    def test_empty_color_values(self):
        config("test/data/ColorsTest5.conf")
        pri_color = Colors().get_priority_colors()
        project_color = Colors().get_project_color()
        context_color = Colors().get_context_color()
        link_color = Colors().get_link_color()
        metadata_color = Colors().get_metadata_color()

        self.assertEqual(pri_color['A'], NEUTRAL_COLOR)
        self.assertEqual(pri_color['B'], NEUTRAL_COLOR)
        self.assertEqual(pri_color['C'], NEUTRAL_COLOR)
        self.assertEqual(project_color, '')
        self.assertEqual(context_color, '')
        self.assertEqual(link_color, '')
        self.assertEqual(metadata_color, '')

    def test_empty_colorscheme(self):
        config("test/data/config1")
        pri_color = Colors().get_priority_colors()
        project_color = Colors().get_project_color()
        context_color = Colors().get_context_color()
        link_color = Colors().get_link_color()
        metadata_color = Colors().get_metadata_color()

        self.assertEqual(pri_color['A'], '\033[0;36m')
        self.assertEqual(pri_color['B'], '\033[0;33m')
        self.assertEqual(pri_color['C'], '\033[0;34m')
        self.assertEqual(project_color, '\033[1;31m')
        self.assertEqual(context_color, '\033[1;35m')
        self.assertEqual(link_color, '\033[4;36m')
        self.assertEqual(metadata_color, '\033[1;32m')

if __name__ == '__main__':
    unittest.main()
