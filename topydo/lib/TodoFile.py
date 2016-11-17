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

"""
This module deals with todo.txt files.
"""

import codecs
import os.path


class TodoFile(object):
    """
    This class represents a todo.txt file, which can be read from or written
    to.
    """

    def __init__(self, p_path, p_on_update=None):
        self.path = os.path.abspath(p_path)
        self.write_lock = False

        if p_on_update:
            from watchdog.observers import Observer
            from watchdog.events import FileSystemEventHandler, FileModifiedEvent, FileCreatedEvent

            class EventHandler(FileSystemEventHandler):
                def _handle(_, p_event):
                    right_type = isinstance(p_event, FileCreatedEvent) or isinstance(p_event, FileModifiedEvent)

                    if not self.write_lock and right_type and p_event.src_path == self.path:
                        p_on_update()

                def on_created(self, p_event):
                    """
                    Because vim deletes and creates a file on buffer save, also
                    catch a creation event.
                    """
                    self._handle(p_event)

                def on_modified(self, p_event):
                    self._handle(p_event)

            observer = Observer()
            observer.schedule(EventHandler(), os.path.dirname(self.path))
            observer.start()

    def read(self):
        """ Reads the todo.txt file and returns a list of todo items. """
        todos = []
        try:
            todofile = codecs.open(self.path, 'r', encoding="utf-8")
            todos = todofile.readlines()
            todofile.close()
        except IOError:
            pass

        return todos

    def write(self, p_todos):
        """
        Writes all the todo items to the todo.txt file.

        p_todos can be a list of todo items, or a string that is just written
        to the file.
        """

        # make sure not to reread the todo file because this instance is
        # actually writing it
        self.write_lock = True

        todofile = codecs.open(self.path, 'w', encoding="utf-8")

        if p_todos is list:
            for todo in p_todos:
                todofile.write(str(todo))
        else:
            todofile.write(p_todos)

        todofile.write("\n")

        todofile.close()
        self.write_lock = False
