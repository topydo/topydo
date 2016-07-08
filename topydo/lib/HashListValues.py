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
Module that calculates identifiers for each item in a list, based on the hash
value of each item.
"""

from hashlib import sha1

_TABLE_SIZES = {
    # we choose a large table size to reduce the chance of collisions.
    3: 46649,   # largest prime under zzz_36
    4: 1679609  # largest prime under zzzz_36
}


def _to_base36(p_value):
    """
    Converts integer to base36 string.

    Based on answer on
    https://stackoverflow.com/questions/1181919/python-base-36-encoding
    """
    alphabet = '0123456789abcdefghijklmnopqrstuvwxyz'

    base36 = ''
    while p_value:
        p_value, i = divmod(p_value, 36)
        base36 = alphabet[i] + base36

    return base36 or alphabet[0]


def hash_list_values(p_list, p_key=lambda i: i):  # pragma: no branch
    """
    Calculates a unique value for each item in the list, these can be used as
    identifiers.

    The value is based on hashing an item using the p_hash function.

    Suitable for lists not larger than approx. 16K items.

    Returns a tuple with the status and a list of tuples where each item is
    combined with the ID.
    """
    result = []
    used = set()

    # choose a larger key size if there's >1% chance of collision
    size = _TABLE_SIZES[3] \
        if len(p_list) < _TABLE_SIZES[3] * 0.01 else _TABLE_SIZES[4]

    for item in p_list:
        # obtain the to-be-hashed value
        raw_value = p_key(item)

        # hash
        hasher = sha1()
        hasher.update(raw_value.encode('utf-8'))
        hash_value = int(hasher.hexdigest(), 16) % size

        # resolve possible collisions
        while hash_value in used:
            hash_value = (hash_value + 1) % size

        used.add(hash_value)
        result.append((item, _to_base36(hash_value)))

    return result
