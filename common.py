def print_matrix(H):
	m = len(H)-1
	n = len(H[0])-1

	l = max(len(str(max(max(H)))), len(str(min(min(H)))))
	for j in range(n+1):
		row = ""
		for i in range(m+1):
			row += " " + str(H[i][j]).rjust(l) + " "
		print(row)

def find_one(dirs, a, b, fill="-"):
	alignA = ""
	alignB = ""

	i = len(a)
	j = len(b)
	while i>0 or j>0:
		if (i-1,j-1) in dirs[(i,j)]:
			alignA = a[i-1] + alignA
			alignB = b[j-1] + alignB
			i -= 1
			j -= 1
		elif (i-1,j) in dirs[(i,j)]:
			alignA = a[i-1] + alignA
			alignB = fill + alignB
			i -= 1
		elif (i,j-1) in dirs[(i,j)]:
			alignA = fill + alignA
			alignB = b[j-1] + alignB
			j -= 1

	return (alignA, alignB)

def find_alignment(dirs, a, b, fill="-"):
	if False:
		A = find_all(dirs, a, b, fill, len(a), len(b))
		print(A)
		return A[0]
	else:
		return find_one(dirs, a, b, fill)

def find_all(dirs, a, b, fill, i, j):
	if i>0 or j>0:
		align = []
		if (i-1,j-1) in dirs[(i,j)]:
			A = find_all(dirs,a,b,fill,i-1,j-1)
			for x,y in A:
				align.append((x + a[i-1], y + b[j-1]))
		if (i-1,j) in dirs[(i,j)]:
			A = find_all(dirs,a,b,fill,i-1,j)
			for x,y in A:
				align.append((x + a[i-1], y + fill))
		if (i,j-1) in dirs[(i,j)]:
			A = find_all(dirs,a,b,fill,i,j-1)
			for x,y in A:
				align.append((x + fill, y + b[j-1]))

		return align
	return [("", "")]
