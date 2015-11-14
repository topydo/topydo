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

import os
import shlex

from six import iteritems, PY2
from six.moves import configparser

if PY2:
    import ushlex as shlex
    import codecs

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
            'dep',
            'ls',
            'sort',
            'tags',
            'topydo',
        ]

        self.defaults = {
            'topydo': {
                'default_command': 'ls',
                'colors': '1',
                'filename': 'todo.txt',
                'archive_filename': 'done.txt',
                'identifiers': 'linenumber',
                'backup_count': '5',
            },

            'add': {
                'auto_creation_date': '1',
            },

            'ls': {
                'hide_tags': 'id,p,ical',
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
                'sort_string': 'desc:importance,due,desc:priority',
                'ignore_weekends': '1',
            },

            'dep': {
                'append_parent_projects': '0',
                'append_parent_contexts': '0',
            },

            'colorscheme': {
                'project_color': 'red',
                'context_color': 'magenta',
                'metadata_color': 'green',
                'link_color': 'cyan',
                'priority_colors': 'A:cyan,B:yellow,C:blue',
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
        }

        self.config = {}

        self.cp = configparser.RawConfigParser()

        for section in self.defaults:
            self.cp.add_section(section)

            for option, value in iteritems(self.defaults[section]):
                self.cp.set(section, option, value)

        files = [
            "/etc/topydo.conf",
            self._home_config_path(),
            ".topydo",
            "topydo.conf",
            "topydo.ini",
        ]

        # when a path is given, *only* use the values in that file, or the
        # defaults listed above.
        if p_path is not None:
            files = [p_path]

        if PY2:
            for path in files:
                try:
                    with codecs.open(path, 'r', encoding='utf-8') as f:
                        self.cp.readfp(f)
                except IOError:
                    pass
        else:
            self.cp.read(files)

        self._supplement_sections()

        if p_overrides:
            for (section, option), value in p_overrides.items():
                self.cp.set(section, option, value)

    def _supplement_sections(self):
        for section in self.sections:
            if not self.cp.has_section(section):
                self.cp.add_section(section)

    def _home_config_path(self):
        return os.path.join(os.path.expanduser('~'), '.topydo')

    def default_command(self):
        return self.cp.get('topydo', 'default_command')

    def colors(self):
        try:
            return self.cp.getboolean('topydo', 'colors')
        except ValueError:
            return self.defaults['topydo']['colors'] == '1'

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

    def priority_colors(self):
        """
        Returns a dict with priorities as keys and color numbers as value.
        """
        pri_colors_str = self.cp.get('colorscheme', 'priority_colors')

        def _str_to_dict(p_string):
            pri_colors_dict = dict()
            for pri_color in p_string.split(','):
                pri, color = pri_color.split(':')
                pri_colors_dict[pri] = color

            return pri_colors_dict

        try:
            if pri_colors_str == '':
                pri_colors_dict = {'A': '', 'B': '', 'C': ''}
            else:
                pri_colors_dict = _str_to_dict(pri_colors_str)
        except ValueError:
            pri_colors_dict = _str_to_dict(self.defaults['colorscheme']['priority_colors'])

        return pri_colors_dict

    def project_color(self):
        try:
            return self.cp.get('colorscheme', 'project_color')
        except ValueError:
            return int(self.defaults['colorscheme']['project_color'])

    def context_color(self):
        try:
            return self.cp.get('colorscheme', 'context_color')
        except ValueError:
            return int(self.defaults['colorscheme']['context_color'])

    def metadata_color(self):
        try:
            return self.cp.get('colorscheme', 'metadata_color')
        except ValueError:
            return int(self.defaults['colorscheme']['metadata_color'])

    def link_color(self):
        try:
            return self.cp.get('colorscheme', 'link_color')
        except ValueError:
            return int(self.defaults['colorscheme']['link_color'])

    def auto_creation_date(self):
        try:
            return self.cp.getboolean('add', 'auto_creation_date')
        except ValueError:
            return self.defaults['add']['auto_creation_date'] == '1'

    def aliases(self):
        """
        Returns dict with aliases names as keys and pairs of actual
        subcommand and alias args as values.
        """
        aliases = self.cp.items('aliases')
        alias_dict = dict()

        for alias, meaning in aliases:
            meaning = shlex.split(meaning)
            real_subcommand = meaning[0]
            alias_args = meaning[1:]
            alias_dict[alias] = (real_subcommand, alias_args)

        return alias_dict

    def list_format(self):
        """ Returns the list format used by `ls` """
        return self.cp.get('ls', 'list_format')


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
            raise ConfigError(str(perr))

    return config.instance

config.instance = None
