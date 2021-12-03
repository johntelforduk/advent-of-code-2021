# Solution to part 2 of day 3 of AOC 2021, Binary Diagnostic
# https://adventofcode.com/2021/day/3

def gte(x: int, y: int) -> bool:
    return x >= y


def lt(x: int, y: int) -> bool:
    return x < y


def rating(codes: list, func) -> int:
    bit_pos = 0

    while len(codes) > 1:
        ones = 0

        for c in codes:
            if c[bit_pos] == '1':
                ones += 1

        if func(ones * 2,  len(codes)):
            winner = '1'
        else:
            winner = '0'

        codes = [r for r in codes if r[bit_pos] == winner]

        bit_pos += 1
    return int(codes[0], 2)


f = open('input.txt')
t = f.read()
f.close()
code_list = t.split('\n')

oxygen = rating(code_list, gte)
co2 = rating(code_list, lt)

print(oxygen * co2)
