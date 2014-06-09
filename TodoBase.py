"""
This module contains the class that represents a single todo item.
"""

import re

import TodoParser

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

    src = None
    fields = {}

    def __init__(self, p_src):
        self.src = p_src.strip()
        self.fields = TodoParser.parse_line(self.src)

    def tag_value(self, p_key):
        """
        Returns a tag value associated with p_key. Returns None if p_key
        does not exist.
        """
        values = self.tag_values(p_key)
        return values[0] if len(values) else None

    def tag_values(self, p_key):
        """
        Returns a list of all tag values associated with p_key. Returns
        empty list if p_key does not exist.
        """

        tags = self.fields['tags']
        matches = [tag[1] for tag in tags if tag[0] == p_key]
        return matches if len(matches) else []

    def has_tag(self, p_key, p_value=""):
        """
        Returns true when there is at least one tag with the given key. If a
        value is passed, it will only return true when there exists a tag with
        the given key-value combination.
        """

        result = [t for t in self.tag_values(p_key) \
                    if p_value == "" or t == p_value]
        return len(result) > 0

    def set_tag(self, p_key, p_value=""):
        """
        Sets a occurrence of the tag identified by p_key. Sets an arbitrary
        instance of the tag when the todo contains multiple tags with this key.
        When p_key does not exist, the tag is added.

        When p_value is not set, the tag will be removed.
        """

        if p_value == "":
            self.remove_tag(p_key)
            return

        value = self.tag_value(p_key)
        if value:
            # remove old value from the tags
            self.fields['tags'] = [t for t in self.fields['tags'] \
                if t[0] != p_key and t[1] != value]

            self.src = re.sub(
                r'\b' + p_key + ':' + value + r'\b',
                p_key + ':' + p_value,
                self.src
            )
        else:
            self.src += ' ' + p_key + ':' + p_value

        self.fields['tags'].append((p_key, p_value))

    def remove_tag(self, p_key, p_value=""):
        """
        Removes a tag from the todo.
        When the value is empty (default), all occurrences of the tag will be
        removed.
        Else, only those tags with the value will be removed.
        """

        # Build a new list that excludes the specified tag, match by value when
        # p_value is given.
        self.fields['tags'] = [t for t in self.fields['tags'] \
            if not (t[0] == p_key and (p_value == "" or t[1] == p_value))]

        # when value == "", match any value having key p_key
        value = p_value if p_value != "" else r'\S+'
        self.src = re.sub(r'\s?\b' + p_key + ':' + value + r'\b', '', self.src)

    def set_priority(self, p_priority):
        """
        Sets the priority of the todo. Must be a single capital letter [A-Z],
        or None to unset the priority.
        Priority remains unchanged when an invalid priority is given.
        """

        if p_priority == None or re.match('^[A-Z]$', p_priority):
            self.fields['priority'] = p_priority

            priority_str = '' if p_priority == None else '(' + p_priority + ') '
            self.src = re.sub(r'^(\([A-Z]\) )?', priority_str, self.src)

    def priority(self):
        """
        Returns the priority of this todo, or None if no priority is set.
        """
        return self.fields['priority']

    def text(self):
        """ Returns the todo text with tags stripped off. """
        return self.text

    def projects(self):
        """ Returns a list of projects associated with this todo item. """
        return self.fields['projects']

    def contexts(self):
        """ Returns a list of contexts associated with this todo item. """
        return self.fields['contexts']

    def is_completed(self):
        """ Returns True iff this todo has been completed. """
        return self.fields['completed']

    def __print__(self):
        """ A printer for the todo item. """
        print self.src + "\n"
