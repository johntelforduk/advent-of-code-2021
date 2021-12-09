# Solution to part 2 of day 8 of AOC 2021, Seven Segment Search
# https://adventofcode.com/2021/day/8

from itertools import permutations

f = open('input.txt')
t = f.read()
f.close()

# String of all the segment labels in a seven-segment display.
segments = 'abcdefg'

# k = String of official segment labels (in alphabetical order).
# v = The digit that this string of segments displays.
solution = {'abcefg': 0,
            'cf': 1,
            'acdeg': 2,
            'acdfg': 3,
            'bcdf': 4,
            'abdfg': 5,
            'abdefg': 6,
            'acf': 7,
            'abcdefg': 8,
            'abcdfg': 9
            }

total_outputs = 0

for line in t.split('\n'):
    signal, output = line.split(' | ')

    # Try every combination of rewirings possible.
    for destination in permutations(segments, len(segments)):

        # k = old label for 1 segment.
        # v = new label for that segment.
        # For example,
        # {'a': 'g', 'b': 'e', 'c': 'a', 'd': 'd', 'e': 'f', 'f': 'b', 'g': 'c'}
        rewire = {}
        for s in range(len(segments)):
            rewire[segments[s]] = destination[s]

        # Count how many signal digits, if rewired in this way, are in the solution dictionary of segments.
        matches = 0
        for digit in signal.split(' '):
            # Apply the rewiring to this digit.

            rewired_digit = ''
            for segment in digit:
                rewired_digit += rewire[segment]

            # sorted() is needed as keys in solution dictionary are alphabetically sorted segment letters.
            if ''.join(sorted(rewired_digit)) in solution:
                matches += 1

        # If all 10 signal digits have their segments matched in solution dictionary, then the rewiring worked!
        if matches == len(solution):
            print(rewire, matches)

            # Rewire the segments in each output digit.
            this_number = 0
            for digit in output.split(' '):

                rewired_digit = ''
                for segment in digit:
                    rewired_digit += rewire[segment]

                this_number = 10 * this_number + solution[''.join(sorted(rewired_digit))]
            total_outputs += this_number

print(total_outputs)
