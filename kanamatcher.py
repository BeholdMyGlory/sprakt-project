
import functools
import itertools

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

def filter_alignments(alignments, fill="-", limit=1000):
    matches = set()
    for a, b in itertools.islice(alignments, limit):
        match = clear_fill(find_matches(a, b), fill=fill)
        tup = tuple(match)
        if tup in matches:
            continue

        yield match

        matches.add(tup)

def clear_fill(l, fill='-'):
    return [(a.replace(fill, ''), b.replace(fill, '')) for a, b in l]

def finalize_furigana(l, return_score=False):
    total_score = 0

    def process_furigana(kanji, kana):
        nonlocal total_score
        if (common.to_hiragana(kanji) != kana
                and len(kanji) != 0
                and all(common.is_kanji(k) or k == '々' for k in kanji)):
            furigana, score = split_reading(kanji, kana, return_score=True)
            total_score += score
            return furigana
        else:
            return [(kanji, None)]

    furigana = [(a, b)
                for kanji, kana in l
                for a, b in process_furigana(kanji, kana)]
    return furigana, total_score if return_score else furigana

def match_kana(kanji, kana):
    return min((finalize_furigana(alignment, return_score=True)
                for alignment in filter_alignments(align(kanji, kana))),
               key=lambda x: x[1])[0]

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
