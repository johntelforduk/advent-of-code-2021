# Solution to day 19 of AOC 2021, Beacon Scanner
# https://adventofcode.com/2021/day/19

from itertools import permutations, combinations


def pick_term(xp: int, yp: int, zp: int, option: str) -> int:
    """For parm tuple of (x, y, z) and option string like 'x" or '-z'. Return the number for the option term."""
    options_map = {'x': xp, 'y': yp, 'z': zp, '-x': -xp, '-y': -yp, '-z': -zp}
    return options_map[option]


def make_variant(s: list, xo: str, yo: str, zo: str) -> list:
    return [(pick_term(xi, yi, zi, xo), pick_term(xi, yi, zi, yo), pick_term(xi, yi, zi, zo)) for xi, yi, zi in s]


def variations(s: list) -> list:
    """For parm set of tuples (x, y, z). Return list of the 24 orientation variations possible."""

    neg = {"x": "-x", "-x": "x",
           "y": "-y", "-y": "y",
           "z": "-z", "-z": "z"}

    rots = set()
    rots.add(("x", "y", "z"))

    for steps in range(4):

        update = set()

        for a, b, c in rots:
            update.add((a, b, c))
            update.add((a, neg[c], b))
            update.add((neg[c], b, a))
            update.add((neg[b], a, c))
        rots = update

    variants = [make_variant(s, 'x', 'y', 'z')]
    for xo, yo, zo in rots:
        if xo != 'x' or yo != 'y' or zo != 'z':
            variants.append(make_variant(s, xo, yo, zo))
    return variants


def find_matches(t1: list, t1x: int, t1y: int, t1z: int, t2: list) -> (set, int, int, int):
    """For the 2 parm lists of coordinate tuples (x, y, z).
    t1x, t1y, t1z is the offset of t1 from beacon zero's origin.
    Try every combination of coordinates as anchors.
    Return the set of matching coordinates for whichever pair of anchors has 12 or more matches.
    't' is for list of coordinate to be TESTED for matches."""

    for (xa1, ya1, za1) in t1:          # Every coordinate in the list is a potential anchor. 'a' is for anchor.
        for (xa2, ya2, za2) in t2:

            # Work out the offset that needs to be added to t2 coordinates to make them anchor to t1 coords.
            xo = xa1 - xa2
            yo = ya1 - ya2
            zo = za1 - za2

            test_match = set()

            match_count = 0

            for (xt, yt, zt) in t2:
                x_shifted = xt + xo
                y_shifted = yt + yo
                z_shifted = zt + zo

                test_match.add((t1x + x_shifted, t1y + y_shifted, t1z + z_shifted))
                if (x_shifted, y_shifted, z_shifted) in t1:
                    match_count += 1

            if match_count >= 12:
                return test_match, xo, yo, zo

    return set(), 0, 0, 0                       # Less than 12 matches found, so not a match.


def manhattan(t1b: tuple, t2b: tuple) -> int:
    """For parm pair of coordinate tuples, each (x, y, z). Return the Manhattan distance between them."""
    t1x, t1y, t1z = t1b
    t2x, t2y, t2z = t2b

    return abs(t1x - t2x) + abs(t1y - t2y) + abs(t1z - t2z)


assert manhattan((1105, -1205, 1229), (-92, -2380, -20)) == 3621

f = open('input.txt')
t = f.read()
f.close()

scanners = []

for scanner_raw in t.split('\n\n'):
    num = 0
    scanner = []
    for row in scanner_raw.split('\n'):
        if num != 0:                                # Omit this row, which is like '--- scanner 0 ---'.
            raw_x, raw_y, raw_z = row.split(',')
            scanner.append((int(raw_x), int(raw_y), int(raw_z)))

        num += 1
    scanners.append(scanner)

all_variants = [variations(scanner) for scanner in scanners]
print(len(all_variants))

matches = {0: (0, 0, 0, 0)}                    # Scanner 0 with default orientation is the anchor of the solution.

# This is a hacky way to put the first scanner in the solution set of beacons.
beacons, _, _, _ = find_matches(all_variants[0][0], 0, 0, 0, all_variants[0][0])

perms = list(permutations(range(len(scanners)), 2))     # Iterator containing tuples like (0, 0), (0, 1)... (5, 5).

while len(matches) != len(all_variants):               # Keep looping until all scanners have been matched.
    for s1, s2 in perms:
        print(s1, s2, len(all_variants), len(matches))
        if s1 in matches and s2 not in matches:
            s1_variant_num, x1, y1, z1 = matches[s1]
            s1_variant = all_variants[s1][s1_variant_num]
            s2_variants = all_variants[s2]              # List of s2 variants.

            found = False
            s2_variant_num = 0
            while not found and s2_variant_num < len(s2_variants):
                try_matches, tx, ty, tz = find_matches(s1_variant, x1, y1, z1, s2_variants[s2_variant_num])

                if len(try_matches) >= 12:
                    matches[s2] = (s2_variant_num, x1 + tx, y1 + ty, z1 + tz)
                    found = True
                    beacons = beacons.union(try_matches)
                s2_variant_num += 1

print('Part 1:', len(beacons))

scanner_coords = []
for scanner in matches:
    _, scx, scy, scz = matches[scanner]
    scanner_coords.append((scx, scy, scz))

largest = 0
for b1, b2 in combinations(scanner_coords, 2):
    largest = max(largest, manhattan(b1, b2))

print('Part 2:', largest)
