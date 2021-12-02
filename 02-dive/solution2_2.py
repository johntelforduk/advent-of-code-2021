# Solution to part 2 of day 2 of AOC 2021, Dive!
# https://adventofcode.com/2021/day/2

f = open('input.txt')
t = f.read()
f.close()

h, d, a = 0, 0, 0
for [command, units_raw] in [r.split(' ') for r in t.split('\n')]:
    units = int(units_raw)

    if command == 'down':
        a += units
    elif command == 'up':
        a -= units
    elif command == 'forward':
        h += units
        d += a * units

print(h * d)
