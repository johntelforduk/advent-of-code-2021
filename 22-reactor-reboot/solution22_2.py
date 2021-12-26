# Solution to part 2 of day 22 of AOC 2021, Reactor Reboot
# https://adventofcode.com/2021/day/22

def volume(c_vol: tuple) -> int:
    vfx, vtx, vfy, vty, vfz, vtz, _ = c_vol
    return abs(vtx - vfx + 1) * abs(vty - vfy + 1) * abs(vtz - vfz + 1)


def overlap(f1: int, t1: int, f2: int, t2: int) -> (int, int):
    mf = max(f1, f2)
    mt = min(t1, t2)

    if mf <= mt:
        return mf, mt
    return None


def intersection(c1: tuple, c2: tuple) -> (int, int, int, int, int, int):
    fx1, tx1, fy1, ty1, fz1, tz1, _ = c1
    fx2, tx2, fy2, ty2, fz2, tz2, _ = c2

    x_over = overlap(fx1, tx1, fx2, tx2)
    y_over = overlap(fy1, ty1, fy2, ty2)
    z_over = overlap(fz1, tz1, fz2, tz2)

    if x_over is None or y_over is None or z_over is None:
        return None

    xof, xot = x_over
    yof, yot = y_over
    zof, zot = z_over

    return xof, xot, yof, yot, zof, zot


assert overlap(1, 7, 5, 9) == (5, 7)
assert overlap(5, 9, 1, 7) == (5, 7)            # Overlap is commutative.
assert overlap(1, 7, 7, 12) == (7, 7)
assert overlap(1, 3, 5, 6) is None              # These range don't overlap.
assert overlap(10, 12, 11, 15) == (11, 12)
assert overlap(10, 12, 11, 16) == (11, 12)

test_c1 = (10, 12, 10, 12, 10, 12, 'on')
test_c2 = (11, 15, 11, 16, 11, 17, 'on')
test_c3 = (12, 13, 13, 14, 14, 16, 'off')
test_c4 = (12, 13, 13, 14, -5, 5, 'off')

assert volume(test_c1) == (3 * 3 * 3)
assert volume(test_c2) == (5 * 6 * 7)

assert intersection(test_c1, test_c2) == (11, 12, 11, 12, 11, 12)
assert intersection(test_c2, test_c1) == (11, 12, 11, 12, 11, 12)   # Intersection is commutative.
assert intersection(test_c2, test_c3) == (12, 13, 13, 14, 14, 16)   # test_3 entirely inside test_c2.
assert intersection(test_c3, test_c2) == (12, 13, 13, 14, 14, 16)   # test_3 entirely inside test_c2.
assert intersection(test_c1, test_c4) is None
assert intersection(test_c4, test_c1) is None


f = open('input.txt')
t = f.read()
f.close()

cubes = []
for line in t.split('\n'):
    on_off, raw_ranges = line.split(' ')
    raw_x, raw_y, raw_z = raw_ranges.split(',')

    [fx, tx] = [int(term) for term in raw_x[2:].split('..')]
    [fy, ty] = [int(term) for term in raw_y[2:].split('..')]
    [fz, tz] = [int(term) for term in raw_z[2:].split('..')]
    new_cube = (fx, tx, fy, ty, fz, tz, on_off)

    # Go through list of existing cubes.
    updated_cubes = cubes.copy()
    if on_off == 'on':
        updated_cubes.append(new_cube)
    for existing_cube in cubes:
        # updated_cubes.append(existing_cube)
        _, _, _, _, _, _, on_off_e = existing_cube      # Is the existing cube an 'on' or 'off'?
        inter = intersection(new_cube, existing_cube)
        if inter is not None:                           # If no intersection, then no adjustment cube needed.
            fxi, txi, fyi, tyi, fzi, tzi = inter

            adjustment = {('on', 'on'): 'off',          # Intersecting 'on's needs 'off' as adjustment.
                          ('off', 'on'): 'on',
                          ('on', 'off'): 'off',
                          ('off', 'off'): 'on'          # Subtracting an off from an off is a net 'on'.
                          }[on_off_e, on_off]
            updated_cubes.append((fxi, txi, fyi, tyi, fzi, tzi, adjustment))

    cubes = updated_cubes.copy()
    print(len(cubes))

total = 0
for c in cubes:
    _, _, _, _, _, _, on_off = c
    if on_off == 'on':
        total += volume(c)
    else:
        total -= volume(c)
print(total)
