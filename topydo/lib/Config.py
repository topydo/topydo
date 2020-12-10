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

import configparser
import os
import re
import shlex
from collections import OrderedDict
from functools import lru_cache
from itertools import accumulate
from string import ascii_lowercase

from topydo.lib.Color import Color


def home_config_path(p_filename):
    return os.path.join(os.path.expanduser('~'), p_filename)

class ConfigError(Exception):
    def __init__(self, p_text):
        self.text = p_text

    def __str__(self):
        return self.text


class _Config:
    def __init__(self, p_path=None, p_overrides=None):
        """
        Constructor.

        If p_path is given, that is the only configuration file that will be
        read.

        If p_overrides is given, some options are ultimately overridden. This
        is for some command line options which override any configuration file
        (such as todo.txt location passed with -t). The key is a tuple of
        (section, option), the value is the option's value.
        """
        self.sections = [
            'add',
            'aliases',
            'colorscheme',
            'column_keymap',
            'columns',
            'dep',
            'ls',
            'sort',
            'tags',
            'topydo',
        ]

        self.defaults = {
            'topydo': {
                'default_command': 'ls',
                'colors': 'auto',
                'force_colors': '0',
                'filename': 'todo.txt',
                'archive_filename': 'done.txt',
                'identifiers': 'linenumber',
                'identifier_alphabet': '0123456789abcdefghijklmnopqrstuvwxyz',
                'backup_count': '5',
                'auto_delete_whitespace': '1',
            },

            'add': {
                'auto_creation_date': '1',
            },

            'ls': {
                'hide_tags': 'id,p,ical',
                'hidden_item_tags': 'h,hide',
                'indent': '0',
                'list_limit': '-1',
                'list_format': '|%I| %x %{(}p{)} %c %s %k %{due:}d %{t:}t',
            },

            'tags': {
                'tag_start': 't',
                'tag_due': 'due',
                'tag_star': 'star',
            },

            'sort': {
                'keep_sorted': '0',
                'sort_string': 'desc:completed,desc:importance,due,desc:priority',
                'group_string': '',
                'ignore_weekends': '1',
            },

            'dep': {
                'append_parent_projects': '0',
                'append_parent_contexts': '0',
            },

            'edit': {
            },

            'colorscheme': {
                'project_color': 'red',
                'context_color': 'magenta',
                'metadata_color': 'green',
                'link_color': 'cyan',
                'priority_colors': 'A:cyan,B:yellow,C:blue',
                'focus_background_color': 'gray',
                'marked_background_color': 'blue'
            },

            'aliases': {
                'lsproj': 'lsprj',
                'listprj': 'lsprj',
                'listproj': 'lsprj',
                'listproject': 'lsprj',
                'listprojects': 'lsprj',
                'listcon': 'lscon',
                'listcontext': 'lscon',
                'listcontexts': 'lscon',
            },

            'columns': {
                'column_width': '40',
            },

            'column_keymap': {
                'gg': 'home',
                'G': 'end',
                'j': 'down',
                'k': 'up',
                'd': 'cmd del {}',
                'e': 'cmd edit {}',
                'u': 'cmd revert',
                'x': 'cmd do {}',
                'm': 'mark',
                '<C-a>': 'mark_all',
                '.': 'repeat',
                'pp': 'postpone',
                'ps': 'postpone_s',
                'pr': 'pri',
                '0': 'first_column',
                '$': 'last_column',
                'h': 'prev_column',
                'l': 'next_column',
                'A': 'append_column',
                'I': 'insert_column',
                'E': 'edit_column',
                'D': 'delete_column',
                'Y': 'copy_column',
                'L': 'swap_left',
                'R': 'swap_right',
                '<Left>': 'prev_column',
                '<Right>': 'next_column',
                '<Down>': 'down',
                '<Esc>': 'reset',
            },
        }

        self.config = {}

        self.cp = configparser.RawConfigParser(strict=False)
        # allow uppercase config keys
        self.cp.optionxform = lambda option: option

        for section in self.defaults:
            self.cp.add_section(section)

            for option, value in self.defaults[section].items():
                self.cp.set(section, option, value)

        files = [
            "/etc/topydo.conf",
            home_config_path('.config/topydo/config'),
            home_config_path('.topydo'),
            ".topydo",
            "topydo.conf",
            "topydo.ini",
        ]

        # when a path is given, *only* use the values in that file, or the
        # defaults listed above.
        if p_path is not None:
            files = [p_path]

        self.cp.read(files)
        self._supplement_sections()

        if p_overrides:
            for (section, option), value in p_overrides.items():
                self.cp.set(section, option, value)

    def _supplement_sections(self):
        for section in self.sections:
            if not self.cp.has_section(section):
                self.cp.add_section(section)

    def default_command(self):
        return self.cp.get('topydo', 'default_command')

    def colors(self, p_hint_possible=True):
        """
        Returns 0, 16 or 256 representing the number of colors that should be
        used in the output.

        A hint can be passed whether the device that will output the text
        supports colors.
        """
        lookup = {
            'false': 0,
            'no': 0,
            '0': 0,
            '1': 16,
            'true': 16,
            'yes': 16,
            '16': 16,
            '256': 256,
        }

        try:
            forced = self.cp.get('topydo', 'force_colors') == '1'
        except ValueError:
            forced = self.defaults['topydo']['force_colors'] == '1'

        try:
            colors = lookup[self.cp.get('topydo', 'colors').lower()]  # pylint: disable=no-member
        except ValueError:
            colors = lookup[self.defaults['topydo']['colors'].lower()]  # pylint: disable=no-member
        except KeyError:
            # for invalid values or 'auto'
            colors = 16 if p_hint_possible else 0

        # disable colors when no colors are enforced on the commandline and
        # color support is determined automatically
        return 0 if not forced and not p_hint_possible else colors

    def todotxt(self):
        return os.path.expanduser(self.cp.get('topydo', 'filename'))

    def archive(self):
        return os.path.expanduser(self.cp.get('topydo', 'archive_filename'))

    def identifiers(self):
        return self.cp.get('topydo', 'identifiers')

    def backup_count(self):
        try:
            value = self.cp.getint('topydo', 'backup_count')
            if value < 0:
                value = 0
            return value
        except ValueError:
            return int(self.defaults['topydo']['backup_count'])

    def auto_delete_whitespace(self):
        try:
            return self.cp.getboolean('topydo', 'auto_delete_whitespace')
        except ValueError:
            return self.defaults['topydo']['auto_delete_whitespace'] == '1'

    def list_limit(self):
        try:
            return self.cp.getint('ls', 'list_limit')
        except ValueError:
            return int(self.defaults['ls']['list_limit'])

    def list_indent(self):
        try:
            return self.cp.getint('ls', 'indent')
        except ValueError:
            return int(self.defaults['ls']['indent'])

    def keep_sorted(self):
        try:
            return self.cp.getboolean('sort', 'keep_sorted')
        except ValueError:
            return self.defaults['sort']['keep_sorted'] == '1'

    def sort_string(self):
        return self.cp.get('sort', 'sort_string')

    def group_string(self):
        return self.cp.get('sort', 'group_string')

    def ignore_weekends(self):
        try:
            return self.cp.getboolean('sort', 'ignore_weekends')
        except ValueError:
            return self.defaults['sort']['ignore_weekends'] == '1'

    def append_parent_projects(self):
        try:
            return self.cp.getboolean('dep', 'append_parent_projects')
        except ValueError:
            return self.defaults['dep']['append_parent_projects'] == '1'

    def append_parent_contexts(self):
        try:
            return self.cp.getboolean('dep', 'append_parent_contexts')
        except ValueError:
            return self.defaults['dep']['append_parent_contexts'] == '1'

    def _get_tag(self, p_tag):
        try:
            return self.config[p_tag]
        except KeyError:
            value = self.cp.get('tags', p_tag)
            self.config[p_tag] = value
            return value

    def tag_due(self):
        return self._get_tag('tag_due')

    def tag_start(self):
        return self._get_tag('tag_start')

    def tag_star(self):
        return self._get_tag('tag_star')

    def hidden_tags(self):
        """ Returns a list of tags to be hidden from the 'ls' output. """
        hidden_tags = self.cp.get('ls', 'hide_tags')
        # pylint: disable=no-member
        return [] if hidden_tags == '' else [tag.strip() for tag in
                                             hidden_tags.split(',')]

    def hidden_item_tags(self):
        """ Returns a list of tags which hide an item from the 'ls' output. """
        hidden_item_tags = self.cp.get('ls', 'hidden_item_tags')
        # pylint: disable=no-member
        return [] if hidden_item_tags == '' else [tag.strip() for tag in
                                                  hidden_item_tags.split(',')]

    @lru_cache(maxsize=26)
    def priority_color(self, p_priority):
        """
        Returns a dict with priorities as keys and color numbers as value.
        """
        def _str_to_dict(p_string):
            pri_colors_dict = dict()
            for pri_color in p_string.split(','):
                pri, color = pri_color.split(':')
                pri_colors_dict[pri] = Color(color)

            return pri_colors_dict

        try:
            pri_colors_str = self.cp.get('colorscheme', 'priority_colors')

            if pri_colors_str == '':
                pri_colors_dict = _str_to_dict('A:-1,B:-1,C:-1')
            else:
                pri_colors_dict = _str_to_dict(pri_colors_str)
        except ValueError:
            pri_colors_dict = _str_to_dict(self.defaults['colorscheme']['priority_colors'])

        return pri_colors_dict[p_priority] if p_priority in pri_colors_dict else Color('NEUTRAL')

    def project_color(self):
        try:
            return Color(self.cp.getint('colorscheme', 'project_color'))
        except ValueError:
            return Color(self.cp.get('colorscheme', 'project_color'))

    def context_color(self):
        try:
            return Color(self.cp.getint('colorscheme', 'context_color'))
        except ValueError:
            return Color(self.cp.get('colorscheme', 'context_color'))

    def metadata_color(self):
        try:
            return Color(self.cp.getint('colorscheme', 'metadata_color'))
        except ValueError:
            return Color(self.cp.get('colorscheme', 'metadata_color'))

    def link_color(self):
        try:
            return Color(self.cp.getint('colorscheme', 'link_color'))
        except ValueError:
            return Color(self.cp.get('colorscheme', 'link_color'))

    def focus_background_color(self):
        try:
            return Color(self.cp.getint('colorscheme', 'focus_background_color'))
        except ValueError:
            return Color(self.cp.get('colorscheme', 'focus_background_color'))

    def marked_background_color(self):
        try:
            return Color(self.cp.getint('colorscheme', 'marked_background_color'))
        except ValueError:
            return Color(self.cp.get('colorscheme', 'marked_background_color'))

    def auto_creation_date(self):
        try:
            return self.cp.getboolean('add', 'auto_creation_date')
        except ValueError:
            return self.defaults['add']['auto_creation_date'] == '1'

    @lru_cache(maxsize=1)
    def aliases(self):
        """
        Returns dict with aliases names as keys and pairs of actual
        subcommand and alias args as values.
        """
        aliases = self.cp.items('aliases')
        alias_dict = dict()

        for alias, meaning in aliases:
            try:
                meaning = shlex.split(meaning)
                real_subcommand = meaning[0]
                alias_args = meaning[1:]
                alias_dict[alias] = (real_subcommand, alias_args)
            except ValueError as verr:
                alias_dict[alias] = str(verr)

        return alias_dict

    def list_format(self):
        """ Returns the list format used by `ls` """
        return self.cp.get('ls', 'list_format')

    def column_width(self):
        try:
            width = self.cp.getint('columns', 'column_width')

            if width < 1:
                # read default
                raise ValueError

            return width
        except ValueError:
            return int(self.defaults['columns']['column_width'])

    @lru_cache(maxsize=1)
    def column_keymap(self):
        """ Returns keymap and keystates used in column mode """
        keystates = set()

        shortcuts = self.cp.items('column_keymap')
        keymap_dict = dict(shortcuts)

        for combo, action in shortcuts:
            # add all possible prefixes to keystates
            combo_as_list = re.split('(<[A-Z].+?>|.)', combo)[1::2]
            if len(combo_as_list) > 1:
                keystates |= set(accumulate(combo_as_list[:-1]))

            if action in ['pri', 'postpone', 'postpone_s']:
                keystates.add(combo)

            if action == 'pri':
                for c in ascii_lowercase:
                    keymap_dict[combo + c] = 'cmd pri {} ' + c

        return (keymap_dict, keystates)

    def editor(self):
        """
        Returns the editor to invoke. It returns a list with the command in
        the first position and its arguments in the remainder.
        """
        result = 'vi'
        if 'TOPYDO_EDITOR' in os.environ and os.environ['TOPYDO_EDITOR']:
            result = os.environ['TOPYDO_EDITOR']
        else:
            try:
                result = str(self.cp.get('edit', 'editor'))
            except configparser.NoOptionError:
                if 'EDITOR' in os.environ and os.environ['EDITOR']:
                    result = os.environ['EDITOR']

        return shlex.split(result)

    def identifier_alphabet(self):
        alphabet = self.cp.get('topydo', 'identifier_alphabet')

        # deduplicate characters alphabet. Use a dictionary, but an ordered one
        # to keep determinism.
        return list(OrderedDict([(c, None) for c in alphabet]).keys())

def config(p_path=None, p_overrides=None):
    """
    Retrieve the config instance.

    If a path is given, the instance is overwritten by the one that supplies an
    additional filename (for testability). Moreover, no other configuration
    files will be read when a path is given.

    Overrides will discard a setting in any configuration file and use the
    passed value instead. Structure: (section, option) => value
    The previous configuration instance will be discarded.
    """
    if not config.instance or p_path is not None or p_overrides is not None:
        try:
            config.instance = _Config(p_path, p_overrides)
        except configparser.ParsingError as perr:
            raise ConfigError(str(perr)) from perr

    return config.instance

config.instance = None
