# Solution to day 25 of AOC 2021, Sea Cucumber
# https://adventofcode.com/2021/day/25

f = open('input.txt')
t = f.read()
f.close()


# k = Coords of the cucumber (x, y).
# v = Type of cucumber, either '>' or 'v'.
trench = {}

found_x, found_y = 0, 0
for c in t:
    if c == '\n':
        found_y += 1
        found_x = 0
    else:
        if c != '.':
            trench[(found_x, found_y)] = c
        found_x += 1

print(trench)

# Gatepost error.
found_x = found_x - 1

print(found_x, found_y)


def print_trench():
    for py in range(found_y + 1):
        for px in range(found_x + 1):
            if (px, py) in trench:
                print(trench[px, py], end='')
            else:
                print('.', end='')
        print()
    print()


def x_wrap(wx: int) -> int:
    if wx == found_x:
        return 0
    return wx + 1


def y_wrap(wy: int) -> int:
    if wy == found_y:
        return 0
    return wy + 1


def step():
    global trench
    for species in ['>', 'v']:
        new_trench = {}

        for sx, sy in trench:
            creature = trench[(sx, sy)]
            if species == creature:
                if creature == '>' and (x_wrap(sx), sy) not in trench:
                    new_trench[(x_wrap(sx), sy)] = species
                elif creature == 'v' and (sx, y_wrap(sy)) not in trench:
                    new_trench[(sx, y_wrap(sy))] = species
                else:
                    new_trench[(sx, sy)] = species

        for sx, sy in trench:
            if trench[(sx, sy)] != species:
                new_trench[(sx, sy)] = trench[(sx, sy)]

        trench = new_trench.copy()


print_trench()

steps = 0
still_moving = True
while still_moving:
    prev_trench = trench.copy()
    step()
    steps += 1
    print_trench()
    still_moving = (prev_trench != trench)

print(steps)
