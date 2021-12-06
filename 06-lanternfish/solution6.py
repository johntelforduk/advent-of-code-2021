# Solution to day 6 of AOC 2021, Lanternfish
# https://adventofcode.com/2021/day/6

f = open('input.txt')
t = f.read()
f.close()

today = {}

for timer in [int(fish) for fish in t.split(',')]:
    if timer in today:
        today[timer] += 1
    else:
        today[timer] = 1

print(0, today)

for day in range(1, 256 + 1):
    tomorrow = {}

    for timer in today:
        if timer > 0:                               # Progress pregnancies by 1 day.
            if timer -1 in tomorrow:
                tomorrow[timer - 1] += today[timer]
            else:
                tomorrow[timer - 1] = today[timer]

        elif timer == 0:                            # New fish born.
            if 8 in tomorrow:
                tomorrow[8] += today[timer]
            else:
                tomorrow[8] = today[timer]

            if 6 in tomorrow:                       # Parents start a new pregnancy.
                tomorrow[6] += today[timer]
            else:
                tomorrow[6] = today[timer]

    today = tomorrow.copy()

    count = 0
    for timer in today:
        count += today[timer]

    print(day, today, count)
