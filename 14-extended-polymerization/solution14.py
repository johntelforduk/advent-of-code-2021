# Solution to day 14 of AOC 2021, Extended Polymerization
# https://adventofcode.com/2021/day/14

from collections import Counter


def str_to_pairs(poly: str) -> dict:
    """For the parm string, return a dictionary of counts of adjacent paris of characters.
    For example 'AAAB, returns {'AA': 2, AB: 1}."""
    pairs = {}
    for i in range(len(poly) - 1):
        pair = poly[i:i+2]
        if pair in pairs:
            pairs[pair] += 1
        else:
            pairs[pair] = 1
    return pairs


def base_to_pair_rules(base_rules: dict) -> dict:
    """For dictionary of base rules, like {'CH': 'B', 'HH': 'N'} return a dictionary of pair rules. These have same
    keys as base rules, but the value is list of pairs.
    For example, {'CH': 'B''} parm returns {'CH': ['CB', 'BH']}"""
    pair_rules = {}
    for pair in base_rules:
        new_element = base_rules[pair]
        pair_rules[pair] = [pair[0] + new_element, new_element + pair[1]]
    return pair_rules


def next_step(poly_pairs: dict, pair_rules: dict) -> dict:
    """For parm dictionary of polymer pair counts, and transformation rules. Return the output of this transformation
    step.
    For example:
    poly_pairs={'NN': 1, 'NC': 2, 'CB': 3}
    pair_rule={'NN': ['NC', 'CN'], 'NC': ['NB', 'BC'], 'CB': ['CH', 'HB']
    Returns: {'NC': 1, 'CN': 1, 'NB': 2, 'BC': 2, 'CH': 3, 'HB': 3}"""

    pairs = {}
    for pair in poly_pairs:
        for new_pair in pair_rules[pair]:
            if new_pair in pairs:
                pairs[new_pair] += poly_pairs[pair]
            else:
                pairs[new_pair] = poly_pairs[pair]
    return pairs


def pairs_to_counts(original_poly: str, poly_pairs: dict) -> dict:
    """For parm dictionary of polymer pairs, return dictionary of counts of each elements letter.
    Most letters are 'double counted'. Eg. 'B' is in the pairs 'BC' and 'CD'. Except the first and last letters of the
    original polymer. In this example, 'A' is in 'AB' only. So count all the letters, add 1 extra to count for first
    and last letters of original polymer, then divide all counts by 2."""

    counts = {}
    for pair in poly_pairs:
        for element in pair:
            if element in counts:
                counts[element] += poly_pairs[pair]
            else:
                counts[element] = poly_pairs[pair]

    # Add 1 extra to the count for the first and last elements in the original polymer, as these are the only ones
    # that are not double counted.
    for element in [original_poly[0], original_poly[-1]]:
        if element in counts:
            counts[element] += 1
        else:
            counts[element] += 1

    # Finally, divide everything by 2 - as every element is double counted.
    adjusted_counts = {}
    for element in counts:
        adjusted_counts[element] = counts[element] // 2

    return adjusted_counts


f = open('input.txt')
t = f.read()
f.close()

raw_polymer, raw_rules = t.split('\n\n')

base_rules = {}
for r in raw_rules.split('\n'):
    pair, result = r.split(' -> ')
    base_rules[pair] = result

assert str_to_pairs('NNCB') == {'NN': 1, 'NC': 1, 'CB': 1}
assert str_to_pairs('AAAB') == {'AA': 2, 'AB': 1}

print(str_to_pairs('ABCDEF'))
print(Counter('ABCDEF').most_common())

pairs_dict = str_to_pairs('ABCDEF')
print(pairs_to_counts(original_poly='AXF', poly_pairs=pairs_dict))

assert base_to_pair_rules({'CH': 'B'}) == {'CH': ['CB', 'BH']}
assert base_to_pair_rules({'CH': 'B', 'HH': 'N'}) == {'CH': ['CB', 'BH'], 'HH': ['HN', 'NH']}

polymer = str_to_pairs(raw_polymer)
print('raw_polymer, polymer:', raw_polymer, polymer)

print('base_rules:', base_rules)
pair_rules = base_to_pair_rules(base_rules)
print('pair_rules:', pair_rules)

# assert (next_step(poly_pairs={'NN': 1, 'NC': 2, 'CB': 3}, pair_rules=pair_rules)) == {
#                             'NC': 1, 'CN': 1, 'NB': 2, 'BC': 2, 'CH': 3, 'HB': 3}

print()
print(0, polymer)
print(pairs_to_counts(original_poly=raw_polymer, poly_pairs=polymer))

for step in range(1, 40 + 1):
    new_polymer = next_step(polymer, pair_rules)
    polymer = new_polymer.copy()

    print()
    print(step, polymer)
    print(pairs_to_counts(original_poly=raw_polymer, poly_pairs=polymer))

# Find the smallest and largest counts.
counts = pairs_to_counts(original_poly=raw_polymer, poly_pairs=polymer)
min_count, max_count = None, None
for element in counts:
    if min_count is None:
        min_count = counts[element]
        max_count = counts[element]
    else:
        min_count = min(counts[element], min_count)
        max_count = max(counts[element], max_count)

print(max_count - min_count)
