
def print_matrix(H):
    m = len(H)-1
    n = len(H[0])-1

    l = max(len(str(max(max(H)))), len(str(min(min(H)))))
    for j in range(n+1):
        row = ""
        for i in range(m+1):
            row += " " + str(H[i][j]).rjust(l) + " "
        print(row)

def is_kanji(k):
    return 0x3400 <= ord(k) <= 0x9faf

def find_alignment(dirs, a, b, fill="-"):
    return find_all(dirs, a, b, "", "", fill, len(a), len(b))

def find_all(dirs, a, b, al, bl, fill, i, j):
    if i > 0 or j > 0:
        if (i - 1, j - 1) in dirs[i, j]:
            yield from find_all(dirs, a, b, a[i-1] + al, b[j-1] + bl, fill, i - 1, j - 1)
        if (i - 1, j) in dirs[i, j]:
            yield from find_all(dirs, a, b, a[i-1] + al, fill + bl, fill, i - 1, j)
        if (i, j - 1) in dirs[i, j]:
            yield from find_all(dirs, a, b, fill + al, b[j-1] + bl, fill, i, j - 1)
    else:
        yield al, bl

