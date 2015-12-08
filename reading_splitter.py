import sqlite3

import Levenshtein

conn = sqlite3.connect("kanjidic.db")

def process_reading(reading):
    hiragana = "".join(chr(ord(c) - (ord('ァ') - ord('ぁ')))
                      if "ァ" <= c <= "ヶ" else c
                      for c in reading)
    return hiragana.split(".")[0].strip("-")

def get_readings(kanji):
    c = conn.cursor()
    readings =  {process_reading(reading)
                 for reading, reading_type in c.execute(
                     "SELECT reading, type from readings where kanji=?", (kanji,))}
    return readings

def split_reading(kanji, kana):
    def generate_readings(kanji, cur, i):
            if i < len(kanji):
                for reading in get_readings(kanji[i]):
                    yield from generate_readings(kanji, cur+[(kanji[i],reading)], i+1)
            else:
                yield cur

    def similarity(a,b):
        return Levenshtein.distance(a,b)

    scores = []
    for reading in generate_readings(kanji, [], 0):
        a, b = zip(*reading)
        read = ''.join(b)
        score = similarity(read, kana)
        #print("%s (score=%d)" % (read,score))
        scores.append((reading,score))

    #print()
    r,s = zip(*scores)
    result = r[s.index(min(s))]

    return result