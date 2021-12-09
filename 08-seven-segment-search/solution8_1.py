# Solution to part 1 of day 8 of AOC 2021, Seven Segment Search
# https://adventofcode.com/2021/day/8

f = open('input.txt')
t = f.read()
f.close()

count_1478 = 0
for line in t.split('\n'):
    signal, output = line.split(' | ')
    # print(output)

    for digit in output.split(' '):
        print(digit, len(digit))
        if len(digit) in [2, 3, 4, 7]:
            count_1478 += 1

print(count_1478)
