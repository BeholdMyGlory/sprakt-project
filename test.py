import functools
import re

from smith_waterman import *
from needleman_wunsch import *
from reading_splitter import *

def get_ruby(alignA, alignB):
    return ''.join(alignB[i] if alignB[i]!=alignA[i] else "　" for i in range(len(alignB)))

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

    print(get_readings("悪"))
    print("Sequence A:  %s" % seq1)
    print("Sequence B:  %s" % seq2)

    kanji, kana = next(needleman_wunsch(seq1, seq2, d=-1, fill="　"))
    print(kanji)
    print(kana)
    print()
    match = functools.reduce(split, zip(kanji, kana), [])
    match = [(a.replace("　", ""), b.replace("　", "")) for a, b in match]
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

if __name__ == "__main__":
    main()
