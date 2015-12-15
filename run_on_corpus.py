
import re
import sys
import traceback

import common
import kanamatcher

def main(*argv):
    print_all = False
    if argv[0] == "all":
        print_all = True
        argv = argv[1:]

    strip_whitespace = re.compile(r"\s")

    kanji_file, kana_file = argv

    lines = 0
    errors = 0
    num_kanji = 0
    no_ruby = 0

    try:
        with open(kanji_file, encoding="utf-8-sig") as kjf, \
            open(kana_file, encoding="utf-8-sig") as knf:

            skip_lines = 0
            for kanji, kana in zip(kjf, knf):
                if kanji.strip() == '':
                    continue

                lines += 1

                print("{}.".format(lines))

                kanji, kana = strip_whitespace.sub("", kanji), strip_whitespace.sub("", kana)

                kanji_al, kana_al = next(kanamatcher.align(kanji, kana, fill="　", d=-1))

                print(kanji_al)
                print(kana_al)


                try:
                    result = kanamatcher.match_kana(kanji, kana)
                except Exception as e:
                    errors += 1
                    traceback.print_exc()
                    print()
                    continue

                ruby = ""
                output = ""

                for kj, kn in result:
                    if any(common.is_kanji(k) for k in kj):
                        num_kanji += 1
                        if kn is None:
                            no_ruby += 1

                    if kn is not None:
                        ruby += kn
                    output += kj

                    while len(ruby) < len(output):
                        ruby += "　"
                    while len(output) < len(ruby):
                        output += "　"

                    ruby += "|"
                    output += "|"

                print(ruby)
                print(output)

                if print_all or skip_lines > 0:
                    if skip_lines > 0:
                        skip_lines -= 1
                    print()
                else:
                    l = input("Press enter or input the number of lines to skip: ")
                    try:
                        skip_lines = max(0, int(l))
                    except ValueError:
                        pass

    except KeyboardInterrupt:
        pass

    print("================")
    print("Errors during parsing: {}/{}".format(errors, lines))
    print("Kanji missing ruby: {}/{}".format(no_ruby, num_kanji))


if __name__ == '__main__':
    main(*sys.argv[1:])
