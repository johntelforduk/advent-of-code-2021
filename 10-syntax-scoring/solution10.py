# Solution to day 10 of AOC 2021, Syntax Scoring
# https://adventofcode.com/2021/day/10

def parse_chunk(line: str) -> str:
    global error_score

    pairs = {'(': ')',
             '[': ']',
             '{': '}',
             '<': '>'}

    if len(line) >= 2:
        if line[0] in pairs:
            partner = pairs[line[0]]
            the_rest = parse_chunk(line[1:])

            # TODO: Check this logic.
            if len(the_rest) == 0:          # For incomplete lines.
                return ''

            if the_rest[0] == partner:
                return parse_chunk(the_rest[1:])

            errors =  {')': 3,
                       ']': 57,
                       '}': 1197,
                       '>': 25137}

            if the_rest[0] in errors:
                # print(the_rest[0])
                error_score = errors[the_rest[0]]


#    print('incomplete:', line)

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

# error_score = 0
# output =  parse_chunk('[({(<(())[]>[[{[]{<()<>>')
# print(output)




f = open('test.txt')
t = f.read()
f.close()

total = 0
for l in t.split('\n'):
    error_score = 0
    if parse_chunk(l) != '':
        total += error_score

print(total)
