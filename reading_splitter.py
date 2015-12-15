import sqlite3

import Levenshtein

import common

conn = sqlite3.connect("kanjidic.db")

def process_reading(reading):
    hiragana = common.to_hiragana(reading)
    hiragana = hiragana.split(".")[0].strip("-")
    generated_readings = {hiragana}

    def generate_extra_readings(hiragana):
        # handle sokuon
        if hiragana[-1] in "きくちつ":
            yield hiragana[:-1] + "っ"
        # handle rendaku
        if hiragana[0] in "かきくけこさしすせそたちつてとはひふへほ":
            yield chr(ord(hiragana[0]) + 1) + hiragana[1:]
        # handle handakuten for ha row
        if hiragana[0] in "はひふへほ":
            yield chr(ord(hiragana[0]) + 2) + hiragana[1:]
        # handle homophones for dzi, dzu
        if hiragana[0] in "ちつ":
            yield {"ち": "じ", "つ": "ず"}[hiragana[0]] + hiragana[1:]

    old = set()

    while generated_readings != old:
        old = generated_readings
        generated_readings = generated_readings | {new_reading
                                                   for old_reading in generated_readings
                                                   for new_reading in generate_extra_readings(old_reading)}

    return generated_readings

def get_readings(kanji):
    c = conn.cursor()
    readings =  {processed_reading
                 for reading, reading_type in c.execute(
                     "SELECT reading, type from readings where kanji=?", (kanji,))
                 for processed_reading in process_reading(reading)}
    return readings

def split_reading(kanji, kana, skip=False):
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
    minScore = min(s)
    result = r[s.index(minScore)]

    if minScore > 0 and skip:
        return [(kanji, kana)]

    return result
