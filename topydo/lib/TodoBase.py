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
This module contains the class that represents a single todo item.
"""

import re
from datetime import date

from topydo.lib.TodoParser import parse_line
from topydo.lib.Utils import is_valid_priority


class TodoBase(object):
    """
    This class represents a single todo item in a todo.txt file. It maintains
    an internal data dictionary of various attributes, but also keeps the plain
    text format in shape such that it can be printed back to a file with as few
    distortions as possible (no re-shuffling of attributes).

    This is a base class, but supports enough to process any item in a todo.txt
    file. Derived classes add some interpretation to the tags that may appear
    in a todo item.
    """

    def __init__(self, p_src):
        self.src = ""
        self.fields = {}

        self.set_source_text(p_src)

    def tag_value(self, p_key, p_default=None):
        """
        Returns a tag value associated with p_key. Returns p_default if p_key
        does not exist (which defaults to None).
        """
        return self.tag_values(p_key)[0] if p_key in self.fields['tags'] else p_default

    def tag_values(self, p_key):
        """
        Returns a list of all tag values associated with p_key. Returns
        empty list if p_key does not exist.
        """
        return self.fields['tags'][p_key] if p_key in self.fields['tags'] else []

    def has_tag(self, p_key, p_value=""):
        """
        Returns true when there is at least one tag with the given key. If a
        value is passed, it will only return true when there exists a tag with
        the given key-value combination.
        """
        tags = self.fields['tags']
        return p_key in tags and (p_value == "" or p_value in tags[p_key])

    def add_tag(self, p_key, p_value):
        """ Adds a tag to the todo. """
        self.set_tag(p_key, p_value, True)

    def _remove_tag_helper(self, p_key, p_value):
        """
        Removes a tag from the internal todo dictionary. Only those instances
        with the given value are removed. If the value is empty, all tags with
        the given key are removed.
        """
        tags = self.fields['tags']

        try:
            tags[p_key] = [t for t in tags[p_key] if p_value != "" and t != p_value]
            if len(tags[p_key]) == 0:
                del tags[p_key]
        except KeyError:
            pass

    def set_tag(self, p_key, p_value="", p_force_add=False, p_old_value=""):
        """
        Sets a occurrence of the tag identified by p_key. Sets an arbitrary
        instance of the tag when the todo contains multiple tags with this key.
        When p_key does not exist, the tag is added.

        When p_value is not set, the tag will be removed.

        When p_force_add is true, a tag will always be added to the todo, in
        case there is already a tag with the given key.

        When p_old_value is set, all tags having this value will be set to the
        new value.
        """
        if p_value == "":
            self.remove_tag(p_key, p_old_value)
            return

        tags = self.fields['tags']
        value = p_old_value if p_old_value else self.tag_value(p_key)

        if not p_force_add and value:
            self._remove_tag_helper(p_key, value)

            self.src = re.sub(
                r'\b' + p_key + ':' + value + r'\b',
                p_key + ':' + p_value,
                self.src
            )
        else:
            self.src += ' ' + p_key + ':' + p_value

        try:
            tags[p_key].append(p_value)
        except KeyError:
            tags[p_key] = [p_value]

    def remove_tag(self, p_key, p_value=""):
        """
        Removes a tag from the todo.
        When the value is empty (default), all occurrences of the tag will be
        removed.
        Else, only those tags with the value will be removed.
        """
        self._remove_tag_helper(p_key, p_value)

        # when value == "", match any value having key p_key
        value = p_value if p_value != "" else r'\S+'
        self.src = re.sub(r'\s?\b' + p_key + ':' + value + r'\b', '', self.src)

    def tags(self):
        """
        Returns a list of tuples with key-value pairs representing tags in
        this todo item.
        """
        tags = self.fields['tags']
        return [(t, v) for t in tags for v in tags[t]]

    def set_priority(self, p_priority):
        """
        Sets the priority of the todo. Must be a single capital letter [A-Z],
        or None to unset the priority.
        Priority remains unchanged when an invalid priority is given, or when
        the task was completed.
        """
        if not self.is_completed() and (p_priority is None or
                                        is_valid_priority(p_priority)):
            self.fields['priority'] = p_priority

            priority_str = '' if p_priority is None else '(' + p_priority + ') '
            self.src = re.sub(r'^(\([A-Z]\) )?', priority_str, self.src)

    def priority(self):
        """
        Returns the priority of this todo, or None if no priority is set.
        """
        return self.fields['priority']

    def text(self, p_with_tags=False):
        """ Returns the todo text with tags stripped off. """
        return self.src if p_with_tags else self.fields['text']

    def source(self):
        """
        Returns the source text of the todo. This is the raw text with all
        the tags included.
        """
        return self.text(True)

    def set_source_text(self, p_text):
        """ Sets the todo source text. The text will be parsed again. """
        self.src = p_text.strip()
        self.fields = parse_line(self.src)

    def projects(self):
        """ Returns a set of projects associated with this todo item. """
        return set(self.fields['projects'])

    def contexts(self):
        """ Returns a set of contexts associated with this todo item. """
        return set(self.fields['contexts'])

    def is_completed(self):
        """ Returns True iff this todo has been completed. """
        return self.fields['completed']

    def completion_date(self):
        """
        Returns the completion date when the todo has been completed, or None
        otherwise.
        """
        return self.fields['completionDate']

    def set_completed(self, p_completion_date=date.today()):
        """
        Marks the todo as complete.
        Sets the completed flag and sets the completion date to today.
        """
        if not self.is_completed():
            self.set_priority(None)

            self.fields['completed'] = True
            self.fields['completionDate'] = p_completion_date

            self.src = re.sub(r'^(\([A-Z]\) )?',
                              'x ' + p_completion_date.isoformat() + ' ',
                              self.src)

    def set_creation_date(self, p_date=date.today()):
        """
        Sets the creation date of a todo. Should be passed a date object.
        """
        self.fields['creationDate'] = p_date

        # not particularly pretty, but inspired by
        # http://bugs.python.org/issue1519638 non-existent matches trigger
        # exceptions, hence the lambda
        self.src = re.sub(
            r'^(x \d{4}-\d{2}-\d{2} |\([A-Z]\) )?(\d{4}-\d{2}-\d{2} )?(.*)$',
            lambda m:
            u"{}{} {}".format(m.group(1) or '', p_date.isoformat(),
                                m.group(3)), self.src)

    def creation_date(self):
        """ Returns the creation date of a todo. """
        return self.fields['creationDate']
