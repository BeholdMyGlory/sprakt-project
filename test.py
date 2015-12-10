import functools
import re

from smith_waterman import *
from needleman_wunsch import *
from reading_splitter import *

import kanamatcher

def get_ruby(alignA, alignB):
    return ''.join(alignB[i] if alignB[i]!=alignA[i] else "　" for i in range(len(alignB)))

def main():
    seq1 = "ACACACTA"
    seq2 = "AGCACACA"
    seq1 = "GCATGCU"
    seq2 = "GATTACA"
    #seq1 = "fjfjfJDfjdjdfjdfgsGDgssfsdrhse"
    #seq2 = "fjfjfjdfjdjdfjdfgsgdgssfsdrhse"
    seq1 = "このエナメル質と、象牙質、セメント質、歯髄で歯は構成される。通常目に見える部分がこのエナメル質であり、象牙質に支えられている。"
    #seq1 = "このエナメルと、、セメント、ではされる。にえるがこのエナメルであり、にえられている。"
    seq2 = "このエナメルしつと、ぞうげしつ、セメントしつ、しずいでははこうせいされる。つうじょうめにみえるぶぶんがこのエナメルしつであり、ぞうげしつにささえられている。"

    print("Sequence A:  %s" % seq1)
    print("Sequence B:  %s" % seq2)

    kanji, kana = next(kanamatcher.align(seq1, seq2, d=-1, fill="　"))
    print(kanji)
    print(kana)
    print()
    match = kanamatcher.find_matches(kanji, kana)
    match = kanamatcher.clear_fill(match, fill="　")
    for m in match:
        print(m)
    print()

    for a,b in match:
        filtered = re.sub("[^\u4e00-\u9fff]", "", a)
        if len(filtered) > 0:
            if a == filtered:
                result = split_reading(a, b, True)
                x,y = zip(*result)
                print("%s = %s" % (a,', '.join(y)))
            else:
                print("%s = %s" % (a, b))

    print()

    kanji = "学校"
    kana = "がっこう"

    print(kanji)
    print(kana)
    print()

    result = split_reading(kanji, kana, True)

    print(result)
    for a, b in result:
        print("%s = %s" % (a,b))

    #print("Sequence 2: %s" % seq3)
    #filtered = re.sub("[\u4e00-\u9fff]", "　", alignA)
    #kanji = re.sub("[^\u4e00-\u9fff ]", "　", alignA)
    #rubyAB = get_ruby(alignA, alignB)
    #rubyCD = get_ruby(alignC, alignD)
    print(get_readings("匹"))

    print(kanamatcher.match_kana("日本語は、主に日本国内や日本人同士で使われている言語である。",
                                 "にほんごは、おもににほんこくないやににほんじんどうしでつかわれているげんごである。"))

if __name__ == "__main__":
    main()
