# Solution to day 10 of AOC 2021, Syntax Scoring
# https://adventofcode.com/2021/day/10

from statistics import median

pairs = {'(': ')',
         '[': ']',
         '{': '}',
         '<': '>'}


def parse_chunk(line: str) -> str:
    global error_score

    if len(line) >= 2:
        if line[0] in pairs:
            partner = pairs[line[0]]
            the_rest = parse_chunk(line[1:])

            # TODO: Check this logic.
            if len(the_rest) == 0:          # For incomplete lines.
                return ''

            if the_rest[0] == partner:
                return parse_chunk(the_rest[1:])

            errors = {')': 3,
                      ']': 57,
                      '}': 1197,
                      '>': 25137}

            if the_rest[0] in errors:
                # print(the_rest[0])
                error_score = errors[the_rest[0]]

    return line


assert parse_chunk('') == ''

assert parse_chunk('()') == ''
assert parse_chunk('[]') == ''
assert parse_chunk('([])') == ''
assert parse_chunk('{()()()}') == ''
assert parse_chunk('<([{}])>') == ''
assert parse_chunk('[<>({}){}[([])<>]]') == ''
assert parse_chunk('(((((((((())))))))))') == ''

print(parse_chunk('[({(<(())[]>[[{[]{<()<>>'))

error_score = 0
assert parse_chunk('{([(<{}[<>[]}>{[]{[(<()>') != ''
assert error_score == 1197

error_score = 0
assert parse_chunk('[<(<(<(<{}))><([]([]()') != ''
assert error_score == 3

error_score = 0
assert parse_chunk('<{([([[(<>()){}]>(<<{{') != ''
assert error_score == 25137

incomplete_score = {')': 1,
                    ']': 2,
                    '}': 3,
                    '>': 4}

f = open('input.txt')
t = f.read()
f.close()

total, incomplete_scores = 0, []
for row in t.split('\n'):
    error_score, to_close = 0, []

    if parse_chunk(row) != '':
        total += error_score

    if error_score == 0:
        for c in row:
            if c in pairs:
                to_close.insert(0, pairs[c])

            elif c in ')]}>':
                i = 0
                remove_needed = True
                while i <= len(to_close) - 1 and remove_needed:
                    if to_close[i] == c:
                        to_close.pop(i)
                        remove_needed = False
                    i += 1

    print(row, error_score, to_close)

    this_incomplete = 0
    while len(to_close) > 0:
        this_incomplete *= 5
        this_incomplete += incomplete_score[to_close.pop(0)]
    if this_incomplete > 0:
        incomplete_scores.append(this_incomplete)

print(total)
print(median(incomplete_scores))
