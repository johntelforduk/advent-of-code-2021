# Solution to part 1 of day 9 of AOC 2021, Smoke Basin
# https://adventofcode.com/2021/day/9

f = open('input.txt')
t = f.read()
f.close()

floor = {}

x, y = 0, 0

for row in t.split('\n'):
    for height in row:
        floor[(x, y)] = int(height)
        x += 1
    x = 0
    y += 1

print(floor)

risk_sum = 0
for x, y in floor:
    all_less = True
    for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        if (x + dx, y + dy) in floor and floor[(x, y)] >= floor[(x + dx, y + dy)]:
            all_less = False

    if all_less:
        risk_sum += floor[(x, y)] + 1

print(risk_sum)
