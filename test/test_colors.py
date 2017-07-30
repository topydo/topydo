# Topydo - A todo.txt client written in Python.
# Copyright (C) 2014 - 2015 Bram Schoenmakers <bram@topydo.org>
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

from topydo.lib.Color import Color
from topydo.lib.Config import config
from topydo.lib.Todo import Todo

from .topydo_testcase import TopydoTest

NEUTRAL_COLOR = '\033[0m'


class ColorsTest(TopydoTest):
    def test_project_color1(self):
        config(p_overrides={('colorscheme', 'project_color'): '2'})
        self.assertEqual(config().project_color().as_ansi(p_decoration='bold'), '\033[1;32m')

    def test_project_color2(self):
        config(p_overrides={('colorscheme', 'project_color'): 'Foo'})
        self.assertEqual(config().project_color().as_ansi(p_decoration='bold'), NEUTRAL_COLOR)

    def test_project_color3(self):
        config(p_overrides={('colorscheme', 'project_color'): 'yellow'})
        self.assertEqual(config().project_color().as_ansi(p_decoration='bold'), '\033[1;33m')

    def test_project_color4(self):
        config(p_overrides={('colorscheme', 'project_color'): '686'})
        self.assertEqual(config().project_color().as_ansi(p_decoration='bold'), NEUTRAL_COLOR)

    def test_context_color1(self):
        config(p_overrides={('colorscheme', 'context_color'): '35'})
        self.assertEqual(config().context_color().as_ansi(p_decoration='bold'), '\033[1;38;5;35m')

    def test_context_color2(self):
        config(p_overrides={('colorscheme', 'context_color'): 'Bar'})
        self.assertEqual(config().context_color().as_ansi(p_decoration='bold'), NEUTRAL_COLOR)

    def test_context_color3(self):
        config(p_overrides={('colorscheme', 'context_color'): 'magenta'})
        self.assertEqual(config().context_color().as_ansi(p_decoration='bold'), '\033[1;35m')

    def test_context_color4(self):
        config(p_overrides={('colorscheme', 'context_color'): '392'})
        self.assertEqual(config().context_color().as_ansi(p_decoration='bold'), NEUTRAL_COLOR)

    def test_metadata_color1(self):
        config(p_overrides={('colorscheme', 'metadata_color'): '128'})
        self.assertEqual(config().metadata_color().as_ansi(p_decoration='bold'), '\033[1;38;5;128m')

    def test_metadata_color2(self):
        config(p_overrides={('colorscheme', 'metadata_color'): 'Baz'})
        self.assertEqual(config().metadata_color().as_ansi(p_decoration='bold'), NEUTRAL_COLOR)

    def test_metadata_color3(self):
        config(p_overrides={('colorscheme', 'metadata_color'): 'light-red'})
        self.assertEqual(config().metadata_color().as_ansi(p_decoration='bold'), '\033[1;1;31m')

    def test_metadata_color4(self):
        config(p_overrides={('colorscheme', 'metadata_color'): '777'})
        self.assertEqual(config().metadata_color().as_ansi(p_decoration='bold'), NEUTRAL_COLOR)

    def test_link_color1(self):
        config(p_overrides={('colorscheme', 'link_color'): '77'})
        self.assertEqual(config().link_color().as_ansi(p_decoration='underline'), '\033[4;38;5;77m')

    def test_link_color2(self):
        config(p_overrides={('colorscheme', 'link_color'): 'FooBar'})
        self.assertEqual(config().link_color().as_ansi(p_decoration='underline'), NEUTRAL_COLOR)

    def test_link_color3(self):
        config(p_overrides={('colorscheme', 'link_color'): 'red'})
        self.assertEqual(config().link_color().as_ansi(p_decoration='underline'), '\033[4;31m')

    def test_link_color4(self):
        config(p_overrides={('colorscheme', 'link_color'): '777'})
        self.assertEqual(config().link_color().as_ansi(p_decoration='underline'), NEUTRAL_COLOR)

    def test_priority_color1(self):
        config("test/data/ColorsTest1.conf")
        todo_a = Todo('(A) Foo')
        todo_b = Todo('(B) Bar')
        todo_c = Todo('(C) FooBar')

        color_a = config().priority_color(todo_a.priority()).as_ansi()
        color_b = config().priority_color(todo_b.priority()).as_ansi()
        color_c = config().priority_color(todo_c.priority()).as_ansi()

        self.assertEqual(color_a, '\033[0;31m')
        self.assertEqual(color_b, '\033[0;32m')
        self.assertEqual(color_c, '\033[0;33m')

    def test_priority_color2(self):
        config("test/data/ColorsTest2.conf")
        todo_a = Todo('(A) Foo')
        todo_b = Todo('(B) Bar')
        todo_c = Todo('(C) FooBar')

        color_a = config().priority_color(todo_a.priority()).as_ansi()
        color_b = config().priority_color(todo_b.priority()).as_ansi()
        color_c = config().priority_color(todo_c.priority()).as_ansi()

        self.assertEqual(color_a, '\033[0;35m')
        self.assertEqual(color_b, '\033[0;1;36m')
        self.assertEqual(color_c, '\033[0;37m')

    def test_priority_color3(self):
        config("test/data/ColorsTest3.conf")
        todo_a = Todo('(A) Foo')
        todo_b = Todo('(B) Bar')
        todo_z = Todo('(Z) FooBar')
        todo_d = Todo('(D) Baz')
        todo_c = Todo('(C) FooBaz')

        color_a = config().priority_color(todo_a.priority()).as_ansi()
        color_b = config().priority_color(todo_b.priority()).as_ansi()
        color_z = config().priority_color(todo_z.priority()).as_ansi()
        color_d = config().priority_color(todo_d.priority()).as_ansi()
        color_c = config().priority_color(todo_c.priority()).as_ansi()

        self.assertEqual(color_a, '\033[0;35m')
        self.assertEqual(color_b, '\033[0;1;36m')
        self.assertEqual(color_z, NEUTRAL_COLOR)
        self.assertEqual(color_d, '\033[0;31m')
        self.assertEqual(color_c, '\033[0;37m')

    def test_priority_color4(self):
        config("test/data/ColorsTest4.conf")
        todo_a = Todo('(A) Foo')
        todo_b = Todo('(B) Bar')
        todo_c = Todo('(C) FooBar')

        color_a = config().priority_color(todo_a.priority()).as_ansi()
        color_b = config().priority_color(todo_b.priority()).as_ansi()
        color_c = config().priority_color(todo_c.priority()).as_ansi()

        self.assertEqual(color_a, '')
        self.assertEqual(color_b, '')
        self.assertEqual(color_c, '')

    def test_focus_color(self):
        config(p_overrides={('colorscheme', 'focus_background_color'): 'gray'})
        self.assertEqual(config().focus_background_color().as_ansi(), '\033[0;37m')

    def test_mark_color(self):
        config(p_overrides={('colorscheme', 'marked_background_color'): 'blue'})
        self.assertEqual(config().marked_background_color().as_ansi(), '\033[0;34m')

    def test_empty_color_values(self):
        config("test/data/ColorsTest5.conf")
        project_color = config().project_color().as_ansi(p_decoration='bold')
        context_color = config().context_color().as_ansi(p_decoration='bold')
        link_color = config().link_color().as_ansi(p_decoration='underline')
        metadata_color = config().metadata_color().as_ansi(p_decoration='bold')

        todo_a = Todo('(A) Foo')
        todo_b = Todo('(B) Bar')
        todo_c = Todo('(C) FooBar')

        color_a = config().priority_color(todo_a.priority()).as_ansi()
        color_b = config().priority_color(todo_b.priority()).as_ansi()
        color_c = config().priority_color(todo_c.priority()).as_ansi()

        self.assertEqual(color_a, NEUTRAL_COLOR)
        self.assertEqual(color_b, NEUTRAL_COLOR)
        self.assertEqual(color_c, NEUTRAL_COLOR)
        self.assertEqual(project_color, '')
        self.assertEqual(context_color, '')
        self.assertEqual(link_color, '')
        self.assertEqual(metadata_color, '')

    def test_empty_colorscheme(self):
        config("test/data/config1")
        project_color = config().project_color().as_ansi(p_decoration='bold')
        context_color = config().context_color().as_ansi(p_decoration='bold')
        link_color = config().link_color().as_ansi(p_decoration='underline')
        metadata_color = config().metadata_color().as_ansi(p_decoration='bold')

        todo_a = Todo('(A) Foo')
        todo_b = Todo('(B) Bar')
        todo_c = Todo('(C) FooBar')

        color_a = config().priority_color(todo_a.priority()).as_ansi()
        color_b = config().priority_color(todo_b.priority()).as_ansi()
        color_c = config().priority_color(todo_c.priority()).as_ansi()

        self.assertEqual(color_a, '\033[0;36m')
        self.assertEqual(color_b, '\033[0;33m')
        self.assertEqual(color_c, '\033[0;34m')
        self.assertEqual(project_color, '\033[1;31m')
        self.assertEqual(context_color, '\033[1;35m')
        self.assertEqual(link_color, '\033[4;36m')
        self.assertEqual(metadata_color, '\033[1;32m')

    def test_neutral_color(self):
        color = Color('NEUTRAL')

        self.assertEqual(color.as_ansi(), NEUTRAL_COLOR)

if __name__ == '__main__':
    unittest.main()
