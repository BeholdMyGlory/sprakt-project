
import re
import sys
import traceback

import pydoc

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
    total_score = 0
    bad_lines = []

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
                print(kanji)
                print(kana)

                try:
                    result, score = kanamatcher.match_kana(kanji, kana, return_score=True)
                except Exception as e:
                    errors += 1
                    traceback.print_exc()
                    print()
                    continue


                total_score += score

                output = "\n".join(kanamatcher.pretty_print(result))
                print(output)
                print("Score:", score)

                if score > 0:
                    bad_lines.append((score, lines, kanji, kana, output))

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

    bad_lines.sort(reverse=True)
    print("================")
    print("Errors during parsing: {}/{}".format(errors, lines))
    print("Total score: {}".format(total_score))
    print("Average score: {}".format(total_score / lines))

    print("================")
    input("Press enter to view bad lines: ")

    pager_output = ""
    for score, line, kanji, kana, output in bad_lines:
        pager_output += "{}.\n{}\n{}\n{}\nScore: {}\n\n".format(
            line, kanji, kana, output, score)
    pydoc.pager(pager_output)

if __name__ == '__main__':
    main(*sys.argv[1:])
