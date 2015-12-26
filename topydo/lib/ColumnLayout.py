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

import configparser

from topydo.lib.Config import home_config_path, ConfigError

class ColumnLayout:
    def __init__(self, p_path=None):
        """
        Constructor.

        If p_path is given, that is the only configuration file that will be
        read.
        """
        self.defaults = {
                'title':  'Yet another column',
                'filterexpr': '',
                'sortexpr': 'desc:prio',
                'show_all': '0',
        }

        self.config = {}

        self.cp = configparser.RawConfigParser(self.defaults)

        files = [
            "/etc/topydo_columns.conf",
            home_config_path('.config/topydo/columns'),
            home_config_path('.topydo_columns'),
            ".topydo_columns",
            "topydo_columns.conf",
            "topydo_columns.ini",
        ]

        # when a path is given, *only* use the values in that file, or the
        # defaults listed above.
        if p_path is not None:
            files = [p_path]

        self.cp.read(files)

    def _get_column_names(self):
        return self.cp.sections()

    def _get_column_dict(self, p_column):
        column_dict = dict()

        column_dict['title'] = self.cp.get(p_column, 'title')
        column_dict['filterexpr'] = self.cp.get(p_column, 'filterexpr')
        column_dict['sortexpr'] = self.cp.get(p_column, 'sortexpr')
        column_dict['show_all'] = self.cp.getboolean(p_column, 'show_all')

        return column_dict

    def columns(self):
        """
        Returns list with complete column configuration dicts.
        """
        column_list = []

        for column in self._get_column_names():
            column_list.append(self._get_column_dict(column))

        return column_list
