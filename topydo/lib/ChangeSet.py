# Topydo - A todo.txt client written in Python.
# Copyright (C) 2014 - 2017 Bram Schoenmakers <bram@topydo.org>
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

""" This module serves for managing todo and archive changesets. """

import json
import time
import zlib
from copy import deepcopy
from hashlib import sha1
from os import path

from topydo.lib.Config import config
from topydo.lib.TodoList import TodoList


def hash_todolist(p_todolist):
    """ Calculates hash for TodoList.TodoList object. """
    todolist_hash = sha1(p_todolist.print_todos().encode('utf-8')).hexdigest()

    return todolist_hash

def get_backup_path():
    """ Returns full path and filename of backup file """
    dirname, filename = path.split(path.splitext(config().todotxt())[0])
    filename = '.' + filename + '.bak'

    return path.join(dirname, filename)

class ChangeSet(object):
    """ Class for operations related with backup management. """

    def __init__(self, p_todolist=None, p_archive=None, p_label=None):
        self.todolist = deepcopy(p_todolist)
        self.archive = deepcopy(p_archive)
        self.timestamp = str(time.time())
        self.label = ' '.join(p_label if p_label else [])

        try:
            self.json_file = open(get_backup_path(), 'r+b')
        except IOError:
            self.json_file = open(get_backup_path(), 'w+b')

        self._read()

    def __iter__(self):
        items = {key: self.backup_dict[key]
                 for key in self.backup_dict if key != 'index'}.items()
        return iter(sorted(items, reverse=True))

    def _read(self):
        """
        Reads backup file from json_file property and sets backup_dict property
        with data decompressed and deserialized from that file. If no usable
        data is found backup_dict is set to the empty dict.
        """
        self.json_file.seek(0)
        try:
            data = zlib.decompress(self.json_file.read())
            self.backup_dict = json.loads(data.decode('utf-8'))
        except (EOFError, zlib.error):
            self.backup_dict = {}

    def _write(self):
        """
        Writes data from backup_dict property in serialized and compressed form
        to backup file pointed in json_file property.
        """
        self.json_file.seek(0)
        self.json_file.truncate()
        dump = json.dumps(self.backup_dict)
        dump_c = zlib.compress(dump.encode('utf-8'))
        self.json_file.write(dump_c)

    def add_archive(self, p_archive):
        """ Sets deep copy of p_archive as archive attribute. """
        self.archive = deepcopy(p_archive)

    def add_todolist(self, p_todolist):
        """ Sets deep copy of p_todolist as todolist attribute. """
        self.todolist = deepcopy(p_todolist)

    def save(self, p_todolist):
        """
        Saves a tuple with archive, todolist and command with its arguments
        into the backup file with unix timestamp as the key. Tuple is then
        indexed in backup file with combination of hash calculated from
        p_todolist and unix timestamp. Backup file is closed afterwards.
        """
        self._trim()

        current_hash = hash_todolist(p_todolist)
        list_todo = (self.todolist.print_todos()+'\n').splitlines(True)
        try:
            list_archive = (self.archive.print_todos()+'\n').splitlines(True)
        except AttributeError:
            list_archive = []

        self.backup_dict[self.timestamp] = (list_todo, list_archive,  self.label)

        index = self._get_index()
        index.insert(0, (self.timestamp, current_hash))
        self._save_index(index)

        self._write()
        self.close()

    def delete(self, p_timestamp=None, p_write=True):
        """ Removes backup from the backup file. """
        timestamp = p_timestamp or self.timestamp
        index = self._get_index()

        try:
            del self.backup_dict[timestamp]
            index.remove(index[[change[0] for change in index].index(timestamp)])
            self._save_index(index)

            if p_write:
                self._write()
        except KeyError:
            pass

    def _get_index(self):
        try:
            index = self.backup_dict['index']
        except KeyError:
            self.backup_dict['index'] = []
            index = self.backup_dict['index']

        return index

    def _save_index(self, p_index):
        """
        Saves index of backups supplied in p_index into the backup_file
        property with 'index' as the key.
        """
        self.backup_dict['index'] = p_index

    def _trim(self):
        """
        Removes oldest backups that exceed the limit configured in backup_count
        option.

        Does not write back to file system, make sure to call self._write()
        afterwards.
        """
        index = self._get_index()
        backup_limit = config().backup_count() - 1

        for changeset in index[backup_limit:]:
            self.delete(changeset[0], p_write=False)

    def read_backup(self, p_todolist=None, p_timestamp=None):
        """
        Retrieves a backup for p_timestamp or p_todolist (if p_timestamp is not
        specified) from backup file and sets timestamp, todolist, archive and
        label attributes to appropriate data from it.
        """
        if not p_timestamp:
            change_hash = hash_todolist(p_todolist)
            index = self._get_index()
            self.timestamp = index[[change[1] for change in index].index(change_hash)][0]
        else:
            self.timestamp = p_timestamp

        d = self.backup_dict[self.timestamp]

        self.todolist = TodoList(d[0])
        self.archive = TodoList(d[1])
        self.label = d[2]

    def apply(self, p_todolist, p_archive):
        """ Applies backup on supplied p_todolist. """
        if self.todolist and p_todolist:
            p_todolist.replace(self.todolist.todos())

        if self.archive and p_archive:
            p_archive.replace(self.archive.todos())

    def close(self):
        """ Closes backup file. """
        self.json_file.close()
