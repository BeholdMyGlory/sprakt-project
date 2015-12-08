

import os
import sqlite3

import lxml.etree


doc = lxml.etree.parse("kanjidic2.xml")

try:
    os.remove("kanjidic.db")
except FileNotFoundError:
    pass

conn = sqlite3.connect("kanjidic.db")
c = conn.cursor()

c.execute("""CREATE TABLE readings
             (kanji text, reading text, type integer)""")

c.execute("CREATE INDEX kanji on readings (kanji)")

for character in doc.xpath("./character"):
    literal = character.find("literal").text
    readings = character.xpath("reading_meaning/rmgroup/"
                               "reading[@r_type = 'ja_on' or @r_type = 'ja_kun']")
    for reading in readings:
        c.execute("INSERT INTO readings VALUES (?, ?, ?)",
                  (literal, reading.text, 0 if reading.attrib['r_type'] == "ja_kun" else 1))

conn.commit()
conn.close()
