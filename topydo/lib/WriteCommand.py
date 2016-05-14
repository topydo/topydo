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

from topydo.lib.Command import Command
from topydo.lib.Config import config
from topydo.lib.RelativeDate import relative_date_to_date
from topydo.lib.TodoListBase import InvalidTodoException


class WriteCommand(Command):

    def postprocess_input_todo(self, p_todo):
        """
        Post-processes a parsed todo when adding it to the list.

        * It converts relative dates to absolute ones.
        * Automatically inserts a creation date if not present.
        * Handles more user-friendly dependencies with before:, partof: and
        after: tags
        """
        def convert_date(p_tag):
            value = p_todo.tag_value(p_tag)

            if value:
                dateobj = relative_date_to_date(value)
                if dateobj:
                    p_todo.set_tag(p_tag, dateobj.isoformat())

        def add_dependencies(p_tag):
            for value in p_todo.tag_values(p_tag):
                try:
                    dep = self.todolist.todo(value)

                    if p_tag == 'after':
                        self.todolist.add_dependency(p_todo, dep)
                    elif p_tag == 'before' or p_tag == 'partof':
                        self.todolist.add_dependency(dep, p_todo)
                    elif p_tag.startswith('parent'):
                        for parent in self.todolist.parents(dep):
                            self.todolist.add_dependency(parent, p_todo)
                    elif p_tag.startswith('child'):
                        for child in self.todolist.children(dep):
                            self.todolist.add_dependency(p_todo, child)
                except InvalidTodoException:
                    pass

                p_todo.remove_tag(p_tag, value)

        convert_date(config().tag_start())
        convert_date(config().tag_due())

        keywords = [
            'after',
            'before',
            'child-of',
            'childof',
            'children-of',
            'childrenof',
            'parent-of',
            'parentof',
            'parents-of',
            'parentsof',
            'partof',
        ]

        for keyword in keywords:
            add_dependencies(keyword)
