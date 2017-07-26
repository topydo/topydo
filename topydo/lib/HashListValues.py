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

from topydo.lib.Config import config

_DEFAULT_ALPHABET = '0123456789abcdefghijklmnopqrstuvwxyz'

# a two-dimensional lookup table, the first dimension is the length of the
# configured alphabet, the second dimension is the width of the ID
# The values are prime numbers that are used for populating the hash table.
_TABLE_SIZES = {
    10: {3: 997, 4: 9973, 5: 99991, 6: 999983},
    11: {3: 1327, 4: 14639, 5: 161047, 6: 1771559},
    12: {3: 1723, 4: 20731, 5: 248827, 6: 2985979},
    13: {3: 2179, 4: 28559, 5: 371291, 6: 4826797},
    14: {3: 2741, 4: 38393, 5: 573811, 6: 7529519},
    15: {3: 3373, 4: 50599, 5: 759371, 6: 11390593},
    16: {3: 4093, 4: 65521, 5: 1048573},
    17: {3: 4909, 4: 83497, 5: 1419839},
    18: {3: 5827, 4: 104971, 5: 1889561},
    19: {3: 6857, 4: 130307, 5: 2476081},
    20: {3: 7993, 4: 159979, 5: 3199997},
    21: {3: 9257, 4: 194479, 5: 4084081},
    22: {3: 10639, 4: 245239, 5: 5153623},
    23: {3: 12163, 4: 279823, 5: 6436327},
    24: {3: 13807, 4: 331769, 5: 7962607},
    25: {3: 15619, 4: 390581, 5: 9765619},
    26: {3: 17573, 4: 456959, 5: 11881357},
    27: {3: 19681, 4: 531383, 5: 14348891},
    28: {3: 21943, 4: 614639, 5: 17210353},
    29: {3: 24379, 4: 707279, 5: 20511143},
    30: {3: 26993, 4: 809993, 5: 24299981},
    31: {3: 29789, 4: 923513, 5: 28629149},
    32: {3: 32749, 4: 1048573},
    33: {3: 35933, 4: 1185907},
    34: {3: 39301, 4: 1336333},
    35: {3: 42863, 4: 1500619},
    36: {3: 46649, 4: 1679609},
    37: {3: 50651, 4: 1874153},
    38: {3: 54869, 4: 2085133},
    39: {3: 59281, 4: 2313439},
    40: {3: 63997, 4: 2559989},
    41: {3: 68917, 4: 2825759},
    42: {3: 74077, 4: 3111679},
    43: {3: 79493, 4: 3418799},
    44: {3: 85159, 4: 3748079},
    45: {3: 91121, 4: 4100611},
    46: {3: 97327, 4: 4477453},
    47: {3: 103813, 4: 4879669},
    48: {3: 110587, 4: 5308379},
    49: {3: 117643, 4: 5764799},
    50: {3: 124991, 4: 6249989},
}


class _TableSizeException(Exception):
    pass

def _get_table_size(p_alphabet, p_num):
    """
    Returns a prime number that is suitable for the hash table size. The size
    is dependent on the alphabet used, and the number of items that need to be
    hashed. The table size is at least 100 times larger than the number of
    items to be hashed, to avoid collisions.

    When the alphabet is too little or too large, then _TableSizeException is
    raised. Currently an alphabet of 10 to 40 characters is supported.
    """
    try:
        for width, size in sorted(_TABLE_SIZES[len(p_alphabet)].items()):
            if p_num < size * 0.01:
                return width, size
    except KeyError:
        pass

    raise _TableSizeException('Could not find appropriate table size for given alphabet')

def hash_list_values(p_list, p_key=lambda i: i):  # pragma: no branch
    """
    Calculates a unique value for each item in the list, these can be used as
    identifiers.

    The value is based on hashing an item using the p_key function.

    Suitable for lists not larger than approx. 16K items.

    Returns a tuple with the status and a list of tuples where each item is
    combined with the ID.
    """
    def to_base(p_alphabet, p_value):
        """
        Converts integer to text ID with characters from the given alphabet.

        Based on answer at
        https://stackoverflow.com/questions/1181919/python-base-36-encoding
        """
        result = ''
        while p_value:
            p_value, i = divmod(p_value, len(p_alphabet))
            result = p_alphabet[i] + result

        return result or p_alphabet[0]

    result = []
    used = set()
    alphabet = config().identifier_alphabet()

    try:
        _, size = _get_table_size(alphabet, len(p_list))
    except _TableSizeException:
        alphabet = _DEFAULT_ALPHABET
        _, size = _get_table_size(alphabet, len(p_list))

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
        result.append((item, to_base(alphabet, hash_value)))

    return result

def max_id_length(p_num):
    """
    Returns the length of the IDs used, given the number of items that are
    assigned an ID. Used for padding in lists.
    """
    try:
        alphabet = config().identifier_alphabet()
        length, _ = _get_table_size(alphabet, p_num)
    except _TableSizeException:
        length, _ = _get_table_size(_DEFAULT_ALPHABET, p_num)

    return length
