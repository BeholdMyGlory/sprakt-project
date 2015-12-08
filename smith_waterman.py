import re

from common import *

def similarity(a, b):
	if a == b:
		return +2
	else:
		return -1

def smith_waterman(a, b, s=similarity, W = lambda i: -1, fill="-"):
	m = len(a)
	n = len(b)

	H = [[0 for j in range(n+1)] for i in range(m+1)]

	dirs = {}
	for i in range(1,m+1):
		for j in range(1,n+1):
			match = H[i-1][j-1] + similarity(a[i-1], b[j-1])
			deletion = max(H[i-k][j] + W(k) for k in range(1,i+1))
			insertion = max(H[i][j-l] + W(l) for l in range(1,j+1))
			H[i][j] = max(0, match, deletion, insertion)

	#print_matrix(H)

	dirs = {}
	i = m
	j = n
	while H[i][j] != 0:
		direction = [(-1,-1), (-1,0), (0,-1)]
		value = [H[i+k][j+l] for (k,l) in direction]
		(k,l) = direction[value.index(max(value))]
		dirs[(i,j)] = [(i+k,j+l)]
		i += k
		j += l

	return find_alignment(dirs, a, b, fill)

def main():
	seq1 = "ACACACTA"
	seq2 = "AGCACACA"

	print("Sequence A:  %s" % seq1)
	print("Sequence B:  %s" % seq2)

	(alignA,alignB) = smith_waterman(seq1, seq2)

	print()
	print("Alignment A: %s" % alignA)
	print("Alignment B: %s" % alignB)
	print()

if __name__ == "__main__":
	main()