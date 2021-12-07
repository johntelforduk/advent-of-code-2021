# Solution to part 2 of day 7 of AOC 2021, The Treachery of Whales
# https://adventofcode.com/2021/day/7

f = open('input.txt')
t = f.read()
f.close()

crabs = [int(crab) for crab in t.split(',')]

print(crabs)

fuel_needed = {}
for i in range(max(crabs) + 1):
    if i == 0:
        fuel_needed[i] = i
    else:
        fuel_needed[i] = i + fuel_needed[i - 1]

best = None

for start in range(max(crabs)):
    fuel = 0
    for crab in crabs:
        fuel += fuel_needed[abs(crab - start)]

    if best is None:
        best = fuel
    else:
        best = min(best, fuel)

print(best)
