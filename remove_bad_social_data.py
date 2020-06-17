import sys

vocabs = set()
for word in open('res/vocab').read().splitlines():
    vocabs.add(word)

inp = sys.argv[1]
out = inp + ".out"


def is_bad_line(line):
    count = 0
    words = line.split()
    if len(words) < 3:
        return True
    for word in words:
        if word in vocabs:
            count += 1
    return count / len(words) < 0.5


with open(out, 'w') as fp:
    for line in open(inp):
        if is_bad_line(line):
            continue
        fp.write(line)
