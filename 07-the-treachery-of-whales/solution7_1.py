# Solution to part 1 of day 7 of AOC 2021, The Treachery of Whales
# https://adventofcode.com/2021/day/7

f = open('input.txt')
t = f.read()
f.close()

crabs = [int(crab) for crab in t.split(',')]

print(crabs)

best = None

for start in range(max(crabs)):
    fuel = 0
    for crab in crabs:
        fuel += abs(crab - start)

    if best is None:
        best = fuel
    else:
        best = min(best, fuel)

print(best)
