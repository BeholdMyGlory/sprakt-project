import re

from common import *

def similarity(a, b):
    if a == b:
        return +1
    else:
        return -1

def needleman_wunsch(a, b, s=similarity, d=-1, fill="-"):
    #W = lambda i: -1
    #d = -1

    m = len(a)
    n = len(b)

    F = [[0 for j in range(n+1)] for i in range(m+1)]

    for i in range(1,m+1):
        F[i][0] = -i
    for j in range(1,n+1):
        F[0][j] = -j

    dirs = {}
    for i in range(1,m+1):
        for j in range(1,n+1):
            match = F[i-1][j-1] + s(a[i-1], b[j-1])
            deletion = F[i-1][j] + d
            insertion = F[i][j-1] + d
            F[i][j] = max(match, insertion, deletion)

            dirs[(i,j)] = []
            if F[i][j] == match:
                dirs[(i,j)].append((i-1,j-1))
            if F[i][j] == deletion:
                dirs[(i,j)].append((i-1,j))
            if F[i][j] == insertion:
                dirs[(i,j)].append((i,j-1))

    #print_matrix(F)
    #for x,y in dirs:
    #    print(str((x,y)) + ": " + str(dirs[(x,y)]))

    return find_alignment(dirs, a, b, fill)

def main():
    seq1 = "GCATGCU"
    seq2 = "GATTACA"

    print("Sequence A:  %s" % seq1)
    print("Sequence B:  %s" % seq2)

    (alignA,alignB) = needleman_wunsch(seq1, seq2)

    print()
    print("Alignment A: %s" % alignA)
    print("Alignment B: %s" % alignB)
    print()

if __name__ == "__main__":
    main()
