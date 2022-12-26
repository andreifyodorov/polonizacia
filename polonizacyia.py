#!/usr/bin/env python3

import re

from sys import stdin
from itertools import chain, groupby

IS_FIRST = "is_first"
IS_LAST = "is_last"
IOT_DROPPING = "iot_dropping"
DZ_IOT = "dz_iot"
RZ_IOT = "rz_iot"

TRIVIAL_CASES = dict(zip("абвгзклмнопстуфыэ", "abwgzklmnopstufye"))

def polonize_char(c, flags):
    """ Polonize a character

    >>> polonize_char("а", [])
    'a'

    >>> polonize_char("д", [])
    ('d', 'dz_iot')

    >>> polonize_char("я", [IS_FIRST])
    'ja'

    >>> polonize_char("ю", [DZ_IOT])
    'ziu'
    """

    t = TRIVIAL_CASES.get(c)
    if t:
        return t

    # after "certain letters" (fricatives? retroflex?) `i` is always skipped incl bnlt in iotized vowels
    # "fricative-iot reduction"?
    # "obstruents"? "affricatives"?

    # ц с (цапля caplia)
    if c == "ц":
        return "c", IOT_DROPPING

    # ч cz (чёрный czorni)
    if c == "ч":
        return "cz", IOT_DROPPING

    # ш - never followed by a iotized (counter examples?) - sz
    #   шь  =>  sz not szj e.g. (пойдешь pojdiosz NOT pojdioszj) - CAN'T ALWAYS DROP
    if c == "ш":
        return "sz", IOT_DROPPING

    # щ szcz (щёки szczoki)
    if c == "щ":
        return "szcz", IOT_DROPPING

    # х - (мухе muche NOT muchie - always palatalized?) - ch
    if c == "х":
        return "ch", IOT_DROPPING

    if c == "ж":
        return "ż", IOT_DROPPING

    if c == "ъ":
        return "j", IOT_DROPPING

    j = "i"
    if IS_FIRST in flags:
        j = "j"

    elif DZ_IOT in flags:
        j = "zi"

    elif RZ_IOT in flags:
        j = "z"

    elif IOT_DROPPING in flags:
        j = ""

    if c == "ь":
        if DZ_IOT in flags or RZ_IOT in flags:
            if IS_LAST in flags or RZ_IOT in flags:
                return "z", IS_FIRST

            return "zi", IS_FIRST

        if IOT_DROPPING in flags:
            return ""

        if IS_LAST in flags:
            return "j"
        else:
            return "i", IS_FIRST

    # IOTIZED
    if c == "е":
        return j + "e"

    if c == "ё":
        return j + "o"

    if c == "и":
        if j == "j" or j == "i":  # jy and iy are simply i (йы = и)
            return "i"

        if DZ_IOT in flags:  # it already has i
            return j

        return j + "y"

    if c == "й":
        return j

    if c == "ю":
        return j + "u"

    if c == "я":
        return j + "a"


    # soft d => dz (дядя dziadzia)
    if c == "д":
        return "d", DZ_IOT

    # soft r => rz (рим rzym) и => jy?!
    if c == "р":
        return "r", RZ_IOT

    return c

def polonize_word(word):
    # от = od
    word = re.sub(r"^от$", "od", word)

    # с, из = z
    word = re.sub(r"^(с|из)$", "z", word)

    # adjective ending reduction
    # -ая  =>  -a
    # -ой  =>  -oi
    # -ий  =>  -i

    word = re.sub(r"ая$", "а", word)
    word = re.sub(r"ый$", "ы", word)

    word = re.sub(r"ия$", "ья", word)
    word = re.sub(r"ий$", "и", word)
    word = re.sub(r"ие$", "ье", word)

    flags = [IS_FIRST]
    for i, c in enumerate(word):
        if i + 1 == len(word):
            flags.append(IS_LAST)

        # print(c, flags)
        ret = polonize_char(c, flags)
        # print(ret)
        flags = []

        if (isinstance(ret, tuple)):
            l_c, *flags = ret
            yield l_c
        else:
            yield ret

def str_sum(strs):
    return "".join(strs)

CYRILLIC = "CYR"
LATIN = "LAT"
PUNCTUATION = "PUNCT"

def char_types(iterable):
    for c in chain(*iterable):
        l = c.lower()
        if l in 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя':
            yield c, CYRILLIC

        elif l in 'abcdefghijklmnopqrstuvwxyz':
            yield c, LATIN

        else:
            yield c, PUNCTUATION

def tokenize(iterable):
    # split incoming iterable into chars with types (cyrillic, latin, punctuation)
    chars = char_types(iterable)

    # group chars into words by their type
    grouped = (
        (
            str_sum(c for c, type in group),
            gr_type
        )
        for gr_type, group
        in groupby(chars, lambda char_type: char_type[1])
    )

    # finally make lowercase tokens preserving the capitalization map
    return (
        (
            word.lower(),
            word_type,
            str_sum("O" if c.isupper() else "o" for c in word)
        )
        for word, word_type in grouped
    )

def polonize(tokens):
    for word, word_type, cap_map in tokens:
        if word_type == CYRILLIC:
            yield (polonize_word(word), cap_map)
        else:
            yield word, cap_map

def render(tokens):
    for word, cap_map in tokens:
        for char, cap in zip(word, cap_map):
            yield char.capitalize() if cap.isupper() else char

def process(iterable):
    tokens = tokenize(iterable)
    pol_tokens = polonize(tokens)
    polonized = render(pol_tokens)
    return polonized

def main():
    print(str_sum(process(stdin)))


if __name__ == '__main__':
    main()
