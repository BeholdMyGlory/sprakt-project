
import functools
import itertools

import Levenshtein

import common
from needleman_wunsch import needleman_wunsch as align
from reading_splitter import get_readings, process_reading, split_reading

# kanji missing ruby
NO_RUBY_PENALTY = 2
# mismatch between given kana and resulting ruby
KANA_MISMATCH_PENALTY = 2

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

def filter_alignments(alignments, fill="-", limit=10000):
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
    def process_furigana(kanji, kana):
        if (common.to_hiragana(kanji) != kana
                and len(kanji) != 0
                and all(common.is_kanji(k) for k in kanji)):
            return split_reading(kanji, kana, return_score=True)
        else:
            return [(kanji, None)], sum(NO_RUBY_PENALTY for k in kanji
                                        if common.is_kanji(k))

    nested_furigana, scores = zip(*(process_furigana(kanji, kana)
                                    for kanji, kana in l))
    furigana = [pair
                for nested in nested_furigana
                for pair in nested]
    total_score = sum(scores) + KANA_MISMATCH_PENALTY * \
        Levenshtein.distance("".join(kana for _, kana in l),
                             "".join(kana if kana is not None else kanji
                                     for kanji, kana in furigana))

    return (furigana, total_score) if return_score else furigana

def match_kana(kanji, kana, return_score=False):
    def stoponzero(alignments):
        for i, alignment in enumerate(alignments):
            furigana, score = finalize_furigana(alignment, return_score=True)
            yield furigana, score

            if score == 0:
                break

    best_match, score = min(stoponzero(filter_alignments(align(kanji, kana))),
                            key=lambda x: x[1])
    return (best_match, score) if return_score else best_match

def pretty_print(pairs, fill="　"):
    ruby = ""
    output = ""

    for kanji, kana in pairs:
        if kana is not None:
            ruby += kana
        output += kanji

        while len(ruby) < len(output):
            ruby += "　"
        while len(output) < len(ruby):
            output += "　"

        ruby += "|"
        output += "|"

    return ruby, output

if __name__ == "__main__":
    kanji = "強い相手を求めて空を飛び回る。なんでも溶かしてしまう高熱の炎を自分より弱いものに向けることはしない。"
    kana = "つよいあいてをもとめてそらをとびまわる。なんでもとかしてしまうこうねつのほのおをじぶんよりよわいものにむけることはしない。"

    print("\n".join(pretty_print(match_kana(kanji, kana))))
