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
from topydo.lib.Colors import (get_ansi_color, NEUTRAL_COLOR, CONTEXT_COLOR,
                               METADATA_COLOR, LINK_COLOR, PRIORITY_COLOR,
                               PROJECT_COLOR)
from topydo.lib.Config import config
from topydo.lib.Todo import Todo


class ColorsTest(TopydoTest):
    def test_project_color1(self):
        config(p_overrides={('colorscheme', 'project_color'): '2'})
        color = get_ansi_color(PROJECT_COLOR, p_todo=None, p_decoration='bold')

        self.assertEqual(color, '\033[1;32m')

    def test_project_color2(self):
        config(p_overrides={('colorscheme', 'project_color'): 'Foo'})
        color = get_ansi_color(PROJECT_COLOR, p_todo=None, p_decoration='bold')

        self.assertEqual(color, get_ansi_color(NEUTRAL_COLOR, None))

    def test_project_color3(self):
        config(p_overrides={('colorscheme', 'project_color'): 'yellow'})
        color = get_ansi_color(PROJECT_COLOR, p_todo=None, p_decoration='bold')

        self.assertEqual(color, '\033[1;33m')

    def test_project_color4(self):
        config(p_overrides={('colorscheme', 'project_color'): '686'})
        color = get_ansi_color(PROJECT_COLOR, p_todo=None, p_decoration='bold')

        self.assertEqual(color, get_ansi_color(NEUTRAL_COLOR, None))

    def test_context_color1(self):
        config(p_overrides={('colorscheme', 'context_color'): '35'})
        color = get_ansi_color(CONTEXT_COLOR, p_todo=None, p_decoration='bold')

        self.assertEqual(color, '\033[1;38;5;35m')

    def test_context_color2(self):
        config(p_overrides={('colorscheme', 'context_color'): 'Bar'})
        color = get_ansi_color(CONTEXT_COLOR, p_todo=None, p_decoration='bold')

        self.assertEqual(color, get_ansi_color(NEUTRAL_COLOR, None))

    def test_context_color3(self):
        config(p_overrides={('colorscheme', 'context_color'): 'magenta'})
        color = get_ansi_color(CONTEXT_COLOR, p_todo=None, p_decoration='bold')

        self.assertEqual(color, '\033[1;35m')

    def test_context_color4(self):
        config(p_overrides={('colorscheme', 'context_color'): '392'})
        color = get_ansi_color(CONTEXT_COLOR, p_todo=None, p_decoration='bold')

        self.assertEqual(color, get_ansi_color(NEUTRAL_COLOR, None))

    def test_metadata_color1(self):
        config(p_overrides={('colorscheme', 'metadata_color'): '128'})
        color = get_ansi_color(METADATA_COLOR, p_todo=None, p_decoration='bold')

        self.assertEqual(color, '\033[1;38;5;128m')

    def test_metadata_color2(self):
        config(p_overrides={('colorscheme', 'metadata_color'): 'Baz'})
        color = get_ansi_color(METADATA_COLOR, p_todo=None, p_decoration='bold')

        self.assertEqual(color, get_ansi_color(NEUTRAL_COLOR, None))

    def test_metadata_color3(self):
        config(p_overrides={('colorscheme', 'metadata_color'): 'light-red'})
        color = get_ansi_color(METADATA_COLOR, p_todo=None, p_decoration='bold')

        self.assertEqual(color, '\033[1;1;31m')

    def test_metadata_color4(self):
        config(p_overrides={('colorscheme', 'metadata_color'): '777'})
        color = get_ansi_color(METADATA_COLOR, p_todo=None, p_decoration='bold')

        self.assertEqual(color, get_ansi_color(NEUTRAL_COLOR, None))

    def test_link_color1(self):
        config(p_overrides={('colorscheme', 'link_color'): '77'})
        color = get_ansi_color(LINK_COLOR, p_todo=None,
                               p_decoration='underline')

        self.assertEqual(color, '\033[4;38;5;77m')

    def test_link_color2(self):
        config(p_overrides={('colorscheme', 'link_color'): 'FooBar'})
        color = get_ansi_color(LINK_COLOR, p_todo=None,
                               p_decoration='underline')

        self.assertEqual(color, get_ansi_color(NEUTRAL_COLOR, None))

    def test_link_color3(self):
        config(p_overrides={('colorscheme', 'link_color'): 'red'})
        color = get_ansi_color(LINK_COLOR, p_todo=None,
                               p_decoration='underline')

        self.assertEqual(color, '\033[4;31m')

    def test_link_color4(self):
        config(p_overrides={('colorscheme', 'link_color'): '777'})
        color = get_ansi_color(LINK_COLOR, p_todo=None,
                               p_decoration='underline')

        self.assertEqual(color, get_ansi_color(NEUTRAL_COLOR, None))

    def test_priority_color1(self):
        config("test/data/ColorsTest1.conf")
        todo_a = Todo('(A) Foo')
        todo_b = Todo('(B) Bar')
        todo_c = Todo('(C) FooBar')

        color_a = get_ansi_color(PRIORITY_COLOR, todo_a)
        color_b = get_ansi_color(PRIORITY_COLOR, todo_b)
        color_c = get_ansi_color(PRIORITY_COLOR, todo_c)

        self.assertEqual(color_a, '\033[0;31m')
        self.assertEqual(color_b, '\033[0;32m')
        self.assertEqual(color_c, '\033[0;33m')

    def test_priority_color2(self):
        config("test/data/ColorsTest2.conf")
        todo_a = Todo('(A) Foo')
        todo_b = Todo('(B) Bar')
        todo_c = Todo('(C) FooBar')

        color_a = get_ansi_color(PRIORITY_COLOR, todo_a)
        color_b = get_ansi_color(PRIORITY_COLOR, todo_b)
        color_c = get_ansi_color(PRIORITY_COLOR, todo_c)

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

        color_a = get_ansi_color(PRIORITY_COLOR, todo_a)
        color_b = get_ansi_color(PRIORITY_COLOR, todo_b)
        color_z = get_ansi_color(PRIORITY_COLOR, todo_z)
        color_d = get_ansi_color(PRIORITY_COLOR, todo_d)
        color_c = get_ansi_color(PRIORITY_COLOR, todo_c)

        self.assertEqual(color_a, '\033[0;35m')
        self.assertEqual(color_b, '\033[0;1;36m')
        self.assertEqual(color_z, get_ansi_color(NEUTRAL_COLOR, p_todo=None))
        self.assertEqual(color_d, '\033[0;31m')
        self.assertEqual(color_c, '\033[0;37m')

    def test_priority_color4(self):
        config("test/data/ColorsTest4.conf")
        todo_a = Todo('(A) Foo')
        todo_b = Todo('(B) Bar')
        todo_c = Todo('(C) FooBar')

        color_a = get_ansi_color(PRIORITY_COLOR, todo_a)
        color_b = get_ansi_color(PRIORITY_COLOR, todo_b)
        color_c = get_ansi_color(PRIORITY_COLOR, todo_c)

        self.assertEqual(color_a, get_ansi_color(NEUTRAL_COLOR, p_todo=None))
        self.assertEqual(color_b, get_ansi_color(NEUTRAL_COLOR, p_todo=None))
        self.assertEqual(color_c, get_ansi_color(NEUTRAL_COLOR, p_todo=None))

    def test_empty_color_values(self):
        config("test/data/ColorsTest5.conf")
        project_color = get_ansi_color(PROJECT_COLOR, p_todo=None,
                                       p_decoration='bold')
        context_color = get_ansi_color(CONTEXT_COLOR, p_todo=None,
                                       p_decoration='bold')
        link_color = get_ansi_color(LINK_COLOR, p_todo=None,
                                    p_decoration='underline')
        metadata_color = get_ansi_color(METADATA_COLOR, p_todo=None,
                                        p_decoration='bold')

        todo_a = Todo('(A) Foo')
        todo_b = Todo('(B) Bar')
        todo_c = Todo('(C) FooBar')

        color_a = get_ansi_color(PRIORITY_COLOR, todo_a)
        color_b = get_ansi_color(PRIORITY_COLOR, todo_b)
        color_c = get_ansi_color(PRIORITY_COLOR, todo_c)

        self.assertEqual(color_a, get_ansi_color(NEUTRAL_COLOR, p_todo=None))
        self.assertEqual(color_b, get_ansi_color(NEUTRAL_COLOR, p_todo=None))
        self.assertEqual(color_c, get_ansi_color(NEUTRAL_COLOR, p_todo=None))
        self.assertEqual(project_color, '')
        self.assertEqual(context_color, '')
        self.assertEqual(link_color, '')
        self.assertEqual(metadata_color, '')

    def test_empty_colorscheme(self):
        config("test/data/config1")
        project_color = get_ansi_color(PROJECT_COLOR, p_todo=None,
                                       p_decoration='bold')
        context_color = get_ansi_color(CONTEXT_COLOR, p_todo=None,
                                       p_decoration='bold')
        link_color = get_ansi_color(LINK_COLOR, p_todo=None,
                                    p_decoration='underline')
        metadata_color = get_ansi_color(METADATA_COLOR, p_todo=None,
                                        p_decoration='bold')

        todo_a = Todo('(A) Foo')
        todo_b = Todo('(B) Bar')
        todo_c = Todo('(C) FooBar')

        color_a = get_ansi_color(PRIORITY_COLOR, todo_a)
        color_b = get_ansi_color(PRIORITY_COLOR, todo_b)
        color_c = get_ansi_color(PRIORITY_COLOR, todo_c)

        self.assertEqual(color_a, '\033[0;36m')
        self.assertEqual(color_b, '\033[0;33m')
        self.assertEqual(color_c, '\033[0;34m')
        self.assertEqual(project_color, '\033[1;31m')
        self.assertEqual(context_color, '\033[1;35m')
        self.assertEqual(link_color, '\033[4;36m')
        self.assertEqual(metadata_color, '\033[1;32m')

if __name__ == '__main__':
    unittest.main()
