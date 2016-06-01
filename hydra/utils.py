"""
Contains various utility methods.

:file: utils.py
:date: 27/08/2015
:authors:
    - Gilad Naaman <gilad.doom@gmail.com>
"""

import struct
from .compatibility import *

ObjectCounter = 0


def get_id():
    """ Return an incremented ID. """
    global ObjectCounter
    ObjectCounter += 1
    return ObjectCounter


def fit_bytes_to_size(byte_string, length):
    """
    Ensure the given byte_string is in the correct length

    A long byte_string will be truncated, while a short one will be padded.

    :param byte_string: The string to fit.
    :param length:      The required string size.
    """
    if length is None:
        return byte_string

    if len(byte_string) < length:
        return byte_string + (b'\x00' * (length - len(byte_string)))

    return byte_string[:length]


def is_native_endian_little():
    """ Determine whether the host machine's native endian is little or not. """
    return struct.pack('@H', 0x00FF) == struct.pack('<H', 0x00FF)


def is_native_endian_big():
    """ Determine whether the host machine's native endian is big or not. """
    return struct.pack('@H', 0x00FF) == struct.pack('>H', 0x00FF)


def is_little_endian(endian):
    """ Determine whether the give endian is little or not on the host machine. """
    if endian == '<':
        return True

    return struct.pack(endian + 'H', 0x00FF) == struct.pack('<H', 0x00FF)


def to_chunks(byte_string, chunk_size):
    """
    Divide the given byte_string into chunks in the given size.

    :param byte_string: The string to divide.
    :param chunk_size:  The size of each of the chunks.
    :return:            A list of byte-strings.
    """
    chunks = []
    for idx in xrange(0, len(byte_string), chunk_size):
        chunks.append(byte_string[idx: idx + chunk_size])

    return chunks


def mask(length, offset=0):
    """
    Generate a bitmask with the given parameter.

    :param length:  The bit length of the mask.
    :param offset:  The offset of the mask from the LSB bit. [default: 0]
    :return:        An integer representing the bit mask.
    """
    return ((1 << length) - 1) << offset


def bit_length(num):
    """
    Measure the length of the number in bits.

    :param num: The number to measure.
    :return:    The minimal amount of bits needed to represent the number.
    """
    # `- 2` is due the output format of `bin`: `0bXXXXXXX`
    return len(bin(num)) - 2


def string2bytes(string):
    """ Make regular ol' strings work as bytes in python3. """
    if bytes is not str and type(string) is str:
        string = list(map(lambda char: ord(char), list(string)))
        string = bytes(string)

    return string

BYTE_MASK = mask(8)
WORD_MASK = mask(16)
DWORD_MASK = mask(32)
QWORD_MASK = mask(64)
