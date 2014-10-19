# Topydo - A todo.txt client written in Python.
# Copyright (C) 2014 Bram Schoenmakers <me@bramschoenmakers.nl>
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
This module contains some definitions to configure the application.
"""

DEFAULT_ACTION = 'ls'
COLORS = True
HIGHLIGHT_PROJECTS_CONTEXTS = True

FILENAME = 'todo.txt'
ARCHIVE_FILENAME = 'done.txt'

TAG_START = 't'
TAG_DUE = 'due'
TAG_STAR = 'star'

SORT_STRING = 'desc:importance,due,desc:priority'
IGNORE_WEEKENDS = True # for calculating the importance value
