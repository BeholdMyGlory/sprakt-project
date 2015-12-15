
import functools

import common
from needleman_wunsch import needleman_wunsch as align
from reading_splitter import get_readings, process_reading, split_reading

def find_matches(a, b):
    def split(v, el):
        a, b = el
        if len(v) == 0:
            return [(a, b)]
        elif (a == b and v[-1][0] == v[-1][1] or
            a != b and v[-1][0] != v[-1][1]):
            v[-1] = v[-1][0] + a, v[-1][1] + b
        else:
            v.append((a, b))
        return v

    return functools.reduce(split, zip(a, b), [])

def clear_fill(l, fill='-'):
    return [(a.replace(fill, ''), b.replace(fill, '')) for a, b in l]

def finalize_furigana(l):
    return [(a, b)
            for kanji, kana in l
            for a, b in (split_reading(kanji, kana, skip=True)
                         # TODO: better check for when to call split_reading
                         if common.to_hiragana(kanji) != kana
                         else [(kanji, None)])]

def match_kana(kanji, kana):
    return finalize_furigana(
        clear_fill(
            find_matches(
                *next(align(kanji, kana)))))

if __name__ == "__main__":
    kanji = "出来ない場合も多いと思います"
    kana = "できないばあいもおおいとおもいます"
    kanji, kana = next(align(kanji, kana))
    print(kanji)
    print(kana)
    match = find_matches(kanji, kana)
    print(match)
    match = clear_fill(match)
    print(match)
    print(finalize_furigana(match))

    print(match_kana("出来ない場合も多いと思います", "できないばあいもおおいとおもいます"))
