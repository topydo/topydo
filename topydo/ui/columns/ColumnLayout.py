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
from os.path import expanduser

from topydo.lib.Config import home_config_path, config


def columns(p_alt_layout_path=None):
    """
    Returns list with complete column configuration dicts.
    """
    def _get_column_dict(p_cp, p_column):
        column_dict = dict()

        column_dict['title'] = p_cp.get(p_column, 'title')
        column_dict['filterexpr'] = p_cp.get(p_column, 'filterexpr')
        column_dict['sortexpr'] = p_cp.get(p_column, 'sortexpr')
        column_dict['groupexpr'] = p_cp.get(p_column, 'groupexpr')
        column_dict['show_all'] = p_cp.getboolean(p_column, 'show_all')

        return column_dict

    defaults = {
            'title':  'Yet another column',
            'filterexpr': '',
            'sortexpr': config().sort_string(),
            'groupexpr': config().group_string(),
            'show_all': '0',
    }

    cp = configparser.RawConfigParser(defaults)
    files = [
        "topydo_columns.ini",
        "topydo_columns.conf",
        ".topydo_columns",
        home_config_path('.topydo_columns'),
        home_config_path('.config/topydo/columns'),
        "/etc/topydo_columns.conf",
    ]

    if p_alt_layout_path is not None:
        files.insert(0, expanduser(p_alt_layout_path))
    for filename in files:
        if cp.read(filename):
            break

    column_list = []

    for column in cp.sections():
        column_list.append(_get_column_dict(cp, column))

    return column_list
