# -*- coding: utf-8 -*-

import re
import sys


def mreplace(s, chararray, newchararray):
    """
    Zamienia wszystkie wystąpienia znaków w napisie s z tablicy chararray na odpowiednie wystąpienia w tablicy newchararray. 
    """
    for a, b in zip(chararray, newchararray):
        s = s.replace(a, b)
    return s

def utf2ascii(s):
    chararray = [
        u'ą', u'ć', u'ę', u'ł', u'ń', u'ó', u'ś', u'ź', u'ż', u'Ą', u'Ć', u'Ę', u'Ł', u'Ń', u'Ó', u'Ś',
        u'Ź', u'Ż', u'č', u'ö', u'–', u'„', u'”', u'í'
    ]
    newchararray = [
        u'a', u'c', u'e', u'l', u'n', u'o', u's', u'z', u'z', u'A', u'C', u'E', u'L', u'N', u'O', u'S',
        u'Z', u'Z', u'c', u'o', u'-', u'"', u'"', u'i'
    ]
    return mreplace(s, chararray, newchararray)

def to_roman(a):
    """
    :param a: Arabic number.
    :return: Roman number.
    """
    a = int(a)
    romans = ['I', 'II', 'III', 'IV', 'V', 'VII', 'VIII', 'IX', 'X']
    return romans[a-1] if 0 < a <= len(romans) else a


def escape_invalid_xml_chars(text, replacement='?'):
    """
    XML 1.0 does not allow all characters in unicode.
    This function replaces invalid characters with provided character.
    :param text: XML text possibly containing invalid characters.
    :param replacement: Character that will be used to replace invalid XML characters.
    """
    illegal_chrs = [
        (0x00, 0x08), (0x0B, 0x0C), (0x0E, 0x1F), (0x7F, 0x84), (0x86, 0x9F), (0xFDD0, 0xFDDF), (0xFFFE, 0xFFFF)
    ]

    if sys.maxunicode >= 0x10000:  # not narrow build
        illegal_chrs.extend([
            (0x1FFFE, 0x1FFFF), (0x2FFFE, 0x2FFFF), (0x3FFFE, 0x3FFFF), (0x4FFFE, 0x4FFFF), (0x5FFFE, 0x5FFFF),
            (0x6FFFE, 0x6FFFF), (0x7FFFE, 0x7FFFF), (0x8FFFE, 0x8FFFF), (0x9FFFE, 0x9FFFF), (0xAFFFE, 0xAFFFF),
            (0xBFFFE, 0xBFFFF), (0xCFFFE, 0xCFFFF), (0xDFFFE, 0xDFFFF), (0xEFFFE, 0xEFFFF), (0xFFFFE, 0xFFFFF),
            (0x10FFFE, 0x10FFFF)
        ])

    illegal_ranges = ["%s-%s" % (chr(low), chr(high)) for (low, high) in illegal_chrs]
    illegal_xml_chars_re = re.compile(u'[%s]' % u''.join(illegal_ranges))
    return illegal_xml_chars_re.sub(replacement, text)
