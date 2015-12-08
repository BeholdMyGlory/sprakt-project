import re

from smith_waterman import *
from needleman_wunsch import *

def get_ruby(alignA, alignB):
    return ''.join(alignB[i] if alignB[i]!=alignA[i] else "　" for i in range(len(alignB)))

def main():
    seq1 = "ACACACTA"
    seq2 = "AGCACACA"
    #seq1 = "fjfjfJDfjdjdfjdfgsGDgssfsdrhse"
    #seq2 = "fjfjfjdfjdjdfjdfgsgdgssfsdrhse"
    seq1 = "このエナメル質と、象牙質、セメント質、歯髄で歯は構成される。通常目に見える部分がこのエナメル質であり、象牙質に支えられている。"
    #seq1 = "このエナメルと、、セメント、ではされる。にえるがこのエナメルであり、にえられている。"
    seq2 = "このエナメルしつと、ぞうげしつ、セメントしつ、しずいでははこうせいされる。つうじょうめにみえるぶぶんがこのエナメルしつであり、ぞうげしつにささえられている。"

    print("Sequence A:  %s" % seq1)
    print("Sequence B:  %s" % seq2)

    #alignA, alignB = smith_waterman(seq1, seq2, fill="　")
    alignC, alignD = needleman_wunsch(seq1, seq2, fill="　")

    #print()
    #print("Alignment A: %s" % alignA)
    #print("Alignment B: %s" % alignB)
    print()
    print("Alignment C: %s" % alignC)
    print("Alignment D: %s" % alignD)
    print()

    #print("Sequence 2: %s" % seq3)
    filtered = re.sub("[\u4e00-\u9fff]", "　", alignA)
    kanji = re.sub("[^\u4e00-\u9fff ]", "　", alignA)
    rubyAB = get_ruby(alignA, alignB)
    rubyCD = get_ruby(alignC, alignD)

    #print("Filtered:   %s" % filtered)
    print("Kanji:       %s" % kanji)
    print("Hiragana:    %s" % alignB)
    print()

    print("Ruby AB:     %s" % rubyAB)
    print("Spaced A:    %s" % alignA)

    print()
    print("Ruby CD:     %s" % rubyCD)
    print("Spaced C:    %s" % alignC)

if __name__ == "__main__":
    main()
