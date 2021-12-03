# Solution to part 1 of day 3 of AOC 2021, Binary Diagnostic
# https://adventofcode.com/2021/day/3

f = open('input.txt')
t = f.read()
f.close()

rows = 0
counts = []
for r in t.split('\n'):
    rows += 1
    for i in range(len(r)):
        if rows == 1:
            counts.append(int(r[i]))
        else:
            counts[i] += int(r[i])

gamma = 0
epsilon = 0
while len(counts) != 0:
    gamma, epsilon = 2 * gamma, 2 * epsilon
    if 2 * counts.pop(0) > rows:
        gamma += 1
    else:
        epsilon += 1

print(gamma * epsilon)
