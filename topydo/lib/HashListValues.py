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

_TABLE_SIZES = [
    # we choose a large table size to reduce the chance of collisions.
    (3, 17573, lambda h: _to_base('abcdefghijklmnopqrstuvwxyz', h)),
    (3, 46649, lambda h: _to_base('0123456789abcdefghijklmnopqrstuvwxyz', h)),
    (4, 456959, lambda h: _to_base('abcdefghijklmnopqrstuvwxyz', h)),
    (4, 1679609, lambda h: _to_base('0123456789abcdefghijklmnopqrstuvwxyz', h)),
]


def _to_base(p_alphabet, p_value):
    """
    Converts integer to text ID with characters from the given alphabet.

    Based on answer on
    https://stackoverflow.com/questions/1181919/python-base-36-encoding
    """
    result = ''
    while p_value:
        p_value, i = divmod(p_value, len(p_alphabet))
        result = p_alphabet[i] + result

    return result or p_alphabet[0]


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
    _, size, converter = _TABLE_SIZES[-1]
    for __, _size, _converter in _TABLE_SIZES:
        if len(p_list) < _size * 0.01:
            size , converter = _size, _converter
            break

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
        result.append((item, converter(hash_value)))

    return result

def max_id_length(p_num):
    """
    Returns the length of the IDs used, given the number of items that are
    assigned an ID.
    """
    for length, size, _ in _TABLE_SIZES:
        if p_num < size * 0.01:
            return length

    return 4
