# Topydo - A todo.txt client written in Python.
# Copyright (C) 2014 - 2016 Bram Schoenmakers <bram@topydo.org>
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
This module deals with todo.txt files while putting a watch on them for file
changes.
"""

import os.path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler, FileModifiedEvent, FileCreatedEvent

from topydo.lib.TodoFile import TodoFile


class TodoFileWatched(TodoFile):
    """
    This class represents a todo.txt file, which can be read from or written
    to.
    """

    def __init__(self, p_path, p_on_update):
        super().__init__(p_path)
        self.self_write = False

        class EventHandler(FileSystemEventHandler):
            """
            Event handler to catch modifications (or creations) of the
            current todo.txt file.
            """
            def __init__(self, p_file):
                super().__init__()
                self.file = p_file

            def _handle(self, p_event):
                right_type = isinstance(p_event, FileModifiedEvent) or isinstance(p_event, FileCreatedEvent)
                should_trigger = right_type and p_event.src_path == self.file.path

                if self.file.self_write and should_trigger:
                    # the file was written by topydo, unmark that so we can
                    # record external writes again.
                    self.file.self_write = False
                elif should_trigger:
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
        observer.schedule(EventHandler(self), os.path.dirname(self.path))
        observer.start()

    def write(self, p_todos):
        # make sure not to reread the todo file because this instance is
        # actually writing it
        self.self_write = True
        super().write(p_todos)
