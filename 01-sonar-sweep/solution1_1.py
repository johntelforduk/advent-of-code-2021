# Solution to part 1 of day 1 of AOC 2021, Sonar Sweep
# https://adventofcode.com/2021/day/1

f = open('input.txt')
t = f.read()
f.close()

increases = 0
prev = None
for i in [int(r) for r in t.split('\n')]:
    if prev is not None and i > prev:
        increases += 1
    prev = i

print(increases)
