# Solution to part 2 of day 1 of AOC 2021, Sonar Sweep
# https://adventofcode.com/2021/day/1

f = open('input.txt')
t = f.read()
f.close()

increases = 0
last4 = []
for i in [int(r) for r in t.split('\n')]:
    last4.append(i)
    if len(last4) > 4:
        last4.pop(0)

    if len(last4) == 4 and last4[3] > last4[0]:
        increases += 1

print(increases)
