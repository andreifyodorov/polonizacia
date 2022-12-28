#!/usr/bin/env python3

import re

from sys import stdin
from itertools import chain, groupby

BASIC_CONSONANTS = dict(zip("бвгзкмнпстф", "bwgzkmnpstf"))
POLISH_EXCEPTIONS = dict(zip("длр", "dlr"))
ALWAYS_SOFT_CONSONANTS = {
    'ж': 'ż', 'х': 'ch', 'ц': 'c', 'ч': 'cz', 'ш': 'sz', 'щ': 'szcz'}
SERBIAN_ALWAYS_SOFT_CONSONANTS = {
    'ж': 'ž', 'х': 'h', 'ц': 'c', 'ч': 'č', 'ш': 'š', 'щ': 'šč'}
BASIC_VOWELS = dict(zip("аоуэы", "aouey"))
IOTIZED_VOWELS = dict(zip("яёюе", "aoue"))


def polonize_word(word, polish_exceptions=True,
                  serbian_always_soft_consonants=False):
    """
    >>> str_sum(polonize_word("андрей"))
    'andrzej'

    >>> str_sum(polonize_word("конь"))
    'konj'

    >>> str_sum(polonize_word("гоньба"))
    'goniba'

    >>> str_sum(polonize_word("грудь"))
    'grudź'

    >>> str_sum(polonize_word("дурь"))
    'durz'

    >>> str_sum(polonize_word("зорька"))
    'zorzka'

    >>> str_sum(polonize_word("старик"))
    'starzyk'

    >>> str_sum(polonize_word("володька"))  # Wołodźko
    'wołodźka'

    >>> str_sum(polonize_word("володька", polish_exceptions=False))
    'wolodika'

    >>> str_sum(polonize_word("лес"))
    'les'

    >>> str_sum(polonize_word("бью"))
    'biju'

    >>> str_sum(polonize_word("бюргер"))
    'biurgier'

    >>> str_sum(polonize_word("чёрт"))
    'czort'

    >>> str_sum(polonize_word("чьё"))
    'czjo'

    >>> str_sum(polonize_word("чужой", serbian_always_soft_consonants=True))
    'čužoj'

    >>> str_sum(polonize_word("папайя"))
    'papaja'

    >>> str_sum(polonize_word("шью"))
    'szju'

    >>> str_sum(polonize_word("подъезд"))
    'podjezd'

    >>> str_sum(polonize_word("полонизация"))
    'połonizacyja'

    """
    if polish_exceptions:
        if word == "от":
            yield from "od"
            return

        if word in ("с", "из"):
            yield "z"
            return

        # adjective ending reduction
        word = re.sub(r"ая$", "а", word)
        word = re.sub(r"ый$", "ы", word)
        word = re.sub(r"ий$", "и", word)

    trans = {
        **BASIC_CONSONANTS,
        **POLISH_EXCEPTIONS,
        **(SERBIAN_ALWAYS_SOFT_CONSONANTS if serbian_always_soft_consonants
           else ALWAYS_SOFT_CONSONANTS),
        **BASIC_VOWELS,
        **IOTIZED_VOWELS}

    w = WordIterator(word, polish_exceptions=polish_exceptions)
    while w.iterate():
        if w.is_basic_vowel:
            yield trans[w.c]

        elif w.is_iotized_vowel:
            yield "j" + trans[w.c]

        elif w.is_i:
            yield "i"

        elif w.is_basic_consonant:
            if w.next_is_iotized_vowel:  # this excludes и
                yield trans[w.c] + "i"
                w.iterate()
                yield trans[w.c]

            else:
                yield trans[w.c]

                if w.next_is_soft_sign:
                    w.iterate()
                    if w.is_last:
                        yield "j"
                    else:
                        yield "i"

        elif w.is_d:
            if w.next_is_iotized_vowel:  # this excludes и
                yield "dzi"
                w.iterate()
                yield trans[w.c]

            elif w.next_is_i:
                yield "dz"

            else:
                yield "d"

                if w.next_is_soft_sign:
                    w.iterate()
                    if w.is_last or w.next_is_consonant:
                        yield "ź"
                    else:
                        yield "zi"

        elif w.is_l:
            if w.next_is_iotized_vowel or w.next_is_i or w.next_is_soft_sign:
                yield "l"
                if w.next_is_iotized_vowel:
                    w.iterate()
                    yield trans[w.c]

                if w.next_is_soft_sign:
                    w.iterate()

            else:
                yield "ł"

        elif w.is_r:
            if w.next_is_iotized_vowel or w.next_is_i:
                yield "rz"
                w.iterate()
                if w.is_i:
                    yield "y"
                else:
                    yield trans[w.c]
                continue

            yield "r"

            if w.next_is_soft_sign:
                w.iterate()
                yield "z"

        elif w.is_always_soft_consonant:
            yield trans[w.c]

            if w.next_is_soft_sign or w.next_is_iotized_vowel or w.next_is_i:
                if w.next_is_soft_sign:
                    w.iterate()
                    if not w.is_last:
                        yield "j"

                if w.next_is_iotized_vowel:
                    w.iterate()
                    yield trans[w.c]

                elif w.next_is_i:
                    w.iterate()
                    yield 'y'

        elif w.is_i_short or w.is_hard_sign:
            yield "j"

            if w.next_is_iotized_vowel:
                w.iterate()
                yield trans[w.c]

            elif w.next_is_i:
                w.iterate()
                yield 'y'

        else:
            yield w.c


class WordIterator(object):
    """
    >>> w = WordIterator("тест")
    >>> w.next_iot_drop = True
    >>> w.iterate()
    True
    >>> w.c
    'т'
    >>> w.iterate()
    True
    >>> w.c
    'е'
    """
    def __init__(self, word, polish_exceptions=True):
        self.polish_exceptions = polish_exceptions
        self.word = word
        self.i = None

    def iterate(self):
        self.i = 0 if self.i is None else self.i + 1
        return self.i < len(self.word)

    c = property(lambda s: s.word[s.i])
    is_last = property(lambda s: s.i == len(s.word) - 1)
    next = property(lambda s: None if s.is_last else s.word[s.i + 1])
    is_iotized_vowel = property(lambda s: s.c in IOTIZED_VOWELS)
    next_is_iotized_vowel = property(lambda s: s.next in IOTIZED_VOWELS)
    is_basic_vowel = property(lambda s: s.c in BASIC_VOWELS)
    is_i = property(lambda s: s.c == "и")
    next_is_i = property(lambda s: s.next == "и")
    is_i_short = property(lambda s: s.c == "й")
    is_soft_sign = property(lambda s: s.c == "ь")
    next_is_soft_sign = property(lambda s: s.next == "ь")
    is_hard_sign = property(lambda s: s.c == "ъ")
    is_basic_consonant = property(
        lambda s:
            not s.polish_exceptions and s.c in POLISH_EXCEPTIONS or
            s.c in BASIC_CONSONANTS
    )
    is_d = property(lambda s: s.polish_exceptions and s.c == "д")
    is_l = property(lambda s: s.polish_exceptions and s.c == "л")
    is_r = property(lambda s: s.polish_exceptions and s.c == "р")
    next_is_consonant = property(
        lambda s:
            s.next in BASIC_CONSONANTS or
            s.next in POLISH_EXCEPTIONS or
            s.next in ALWAYS_SOFT_CONSONANTS)
    is_always_soft_consonant = property(
        lambda s: s.c in ALWAYS_SOFT_CONSONANTS)


def str_sum(strs):
    return "".join(strs)


CYRILLIC = "CYR"
LATIN = "LAT"
PUNCTUATION = "PUNCT"


def char_types(iterable):
    for c in chain(*iterable):
        lower = c.lower()
        if lower in 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя':
            yield c, CYRILLIC

        elif lower in 'abcdefghijklmnopqrstuvwxyz':
            yield c, LATIN

        else:
            yield c, PUNCTUATION


def tokenize(iterable):
    # split incoming iterable into chars with types
    # (cyrillic, latin, punctuation)
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


def polonize(tokens, **features):
    for word, word_type, cap_map in tokens:
        if word_type == CYRILLIC:
            yield (polonize_word(word, **features), cap_map)
        else:
            yield word, cap_map


def render(tokens):
    for word, cap_map in tokens:
        for char, cap in zip(word, cap_map):
            yield char.capitalize() if cap.isupper() else char


def process(iterable, **features):
    tokens = tokenize(iterable)
    pol_tokens = polonize(tokens, **features)
    pol_tokens = list(pol_tokens)
    polonized = render(pol_tokens)
    return polonized


def main():
    print(str_sum(process(stdin)))


if __name__ == '__main__':
    main()
