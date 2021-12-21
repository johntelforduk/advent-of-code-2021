# Solution to day 18 of AOC 2021, Snailfish
# https://adventofcode.com/2021/day/18

import json

def str_to_list(s: str) -> list:
    """For the parm list, return the equivalent string."""

    if s.count('[') <= 1:
        # print(s)
        return json.loads(s)

    # Strip off outer pair of square brackets.
    inner = s[1:-1]

    elements = []
    depth = 0
    this_element = ''
    for c in inner:
        if c == ',' and depth == 0:
            elements.append(str_to_list(this_element))
            this_element = ''
        else:
            this_element += c
            if c == '[':
                depth += 1
            if c == ']':
                depth -= 1

    elements.append(str_to_list(this_element))
    return elements


def list_to_str(l: list) -> str:
    return (str(l)).replace(' ', '')


def first_num(s: str) -> (int, int):
    """For parm string, return the start and end positions of the first number in the string."""
    start_num, end_num = None, None
    for i in range(len(s)):
        if s[i].isdigit():
            if start_num is None:
                start_num = i
        else:                           # Not a digit.
            if start_num is not None and end_num is None:
                end_num = i - 1         # Gatepost!

    # Deal with all digits string case.
    if start_num is not None and end_num is None:
        end_num = len(s) - 1

    return start_num, end_num


def last_num(s: str) -> (int, int):
    """For parm string, return the start and end positions of the last number in the string."""
    start, end = first_num(s[::-1])         # Obtain position of first number in reversed string.
    if start is None:
        return None, None
    return len(s) - end -1, len(s) - start -1


def first_10_or_more(s: str) -> (int, int):
    start_num, end_num = None, None
    for i in range(len(s)):
        if s[i].isdigit():
            if start_num is None:
                start_num = i
        else:                           # Not a digit.
            if start_num is not None and end_num is None:
                end_num = i - 1         # Gatepost!
                if start_num == end_num:        # 1 digit number, so restart the search.
                    start_num, end_num = None, None


    # Deal with all digits string case.
    if start_num is not None and end_num is None:
        end_num = len(s) - 1
        if start_num == end_num:  # 1 digit number.
            return (None, None)

    return start_num, end_num


def begin_explode(l, depth: int) -> (list, int, int):

    if type(l) == int:
        return (l, 0, 0)

    if depth == 4:
        left = l[0]
        right = l[1]
        return ('X', left, right)

    left = l[0]
    right = l[1]

    stop_exploding = False

    inside_left, add_left, add_right = begin_explode(left, depth + 1)
    if add_left != 0 or add_right != 0:
        stop_exploding = True

    inside_right = right
    if not stop_exploding:
        inside_right, add_left, add_right = begin_explode(right, depth + 1)

    return ([inside_left, inside_right], add_left, add_right)


def add_to_first_num(s: str, add_on: int) -> str:
    start, end = first_num(s)
    if start is None:
        return s

    before = s[0:start]
    num = str(int(s[start:end + 1]) + add_on)
    after = s[end + 1:]

    return before + num + after


def add_to_last_num(s: str, add_on: int) -> str:
    start, end = last_num(s)
    if start is None:
        return s

    before = s[0:start]
    num = str(int(s[start:end + 1]) + add_on)
    after = s[end + 1:]

    return before + num + after


def explode(s: str) -> str:

    result, add_left, add_right = begin_explode(str_to_list(s), 0)
    # print(result, add_left, add_right)
    result_str = list_to_str(result)

    if 'X' not in result_str:
        return s

    left, right = result_str.split("'X'")
    new_left = add_to_last_num(left, add_left)
    new_right = add_to_first_num(right, add_right)

    return new_left + '0' + new_right


def split(s: str) -> str:
    start, end = first_10_or_more(s)
    if start is None:
        return s

    before = s[0:start]
    num = int(s[start:end + 1])
    after = s[end + 1:]

    return before + '[' + str(num // 2) + ',' + str(round((num + 0.1) / 2)) + ']' + after


def reduce(s: str) -> str:
    new_str = explode(s)
    if new_str != s:
        return reduce(new_str)
    else:                   # Explode had no effect, so lets try a split.
        new_str = split(s)
        if new_str != s:
            return reduce(new_str)
    return s


def add(s1: str, s2: str) -> str:
    return reduce('[' + s1 + ',' + s2 + ']')


def magnitude(l) -> int:
    if type(l) == int:
        return l

    left = l[0]
    right = l[1]
    return 3 * magnitude(left) + 2 * magnitude(right)


assert str_to_list('[1,2]') == [1, 2]
assert str_to_list('[[1,2],3]') == [[1, 2], 3]
assert str_to_list('[9,[8,7]]') == [9, [8, 7]]
assert str_to_list('[[1,9],[8,5]]') == [[1, 9],[8, 5]]
assert str_to_list('[[[[1,2],[3,4]],[[5,6],[7,8]]],9]') == [[[[1,2],[3,4]],[[5,6],[7,8]]],9]
assert str_to_list('[[[9,[3,8]],[[0,9],6]],[[[3,7],[4,9]],3]]') == [[[9,[3,8]],[[0,9],6]],[[[3,7],[4,9]],3]]
assert str_to_list('[[[[1,3],[5,3]],[[1,3],[8,7]]],[[[4,9],[6,9]],[[8,2],[7,3]]]]') == [[[[1,3],[5,3]],[[1,3],[8,7]]],[[[4,9],[6,9]],[[8,2],[7,3]]]]

assert list_to_str([1, 2]) == '[1,2]'
assert list_to_str([[[[1, 2], [3, 4]], [[5, 6], [7, 8]]], 9]) == '[[[[1,2],[3,4]],[[5,6],[7,8]]],9]'

assert first_num(',4],4],[7,[[8,4],9]]],[1,1]]') == (1, 1)
assert first_num('abcde123zse345fg') == (5, 7)
assert first_num('1234') == (0, 3)
assert first_num('abcdefg') == (None, None)
assert first_num('') == (None, None)

assert last_num('1234') == (0, 3)
assert last_num('abcde123ss10a') == (10, 11)
assert last_num('dddffes') == (None, None)
assert last_num('') == (None, None)

assert add_to_first_num('abcde123zse345fg', 10) == 'abcde133zse345fg'
assert add_to_first_num('abcdezsefg', 10) == 'abcdezsefg'
assert add_to_first_num('abcd0eert', 12) == 'abcd12eert'

assert add_to_last_num('abcde123zse345fg', 10) == 'abcde123zse355fg'
assert add_to_last_num('abcdezsefg', 10) == 'abcdezsefg'
assert add_to_last_num('abcd0eert', 12) == 'abcd12eert'

assert explode('[[[[[9,8],1],2],3],4]') == '[[[[0,9],2],3],4]'
assert explode('[[[[[4,3],4],4],[7,[[8,4],9]]],[1,1]]') == '[[[[0,7],4],[7,[[8,4],9]]],[1,1]]'
assert explode('[[[[0,7],4],[7,[[8,4],9]]],[1,1]]') == '[[[[0,7],4],[15,[0,13]]],[1,1]]'

assert first_10_or_more('12345efg') == (0, 4)
assert first_10_or_more('a3bc100efg') == (4, 6)
assert first_10_or_more('123') == (0, 2)
assert first_10_or_more('1') == (None, None)
assert first_10_or_more('dfgsdsgsdf') == (None, None)
assert first_10_or_more('4dfdf3dfdfk9dffff0') == (None, None)

assert split('10') == '[5,5]'
assert split('11') == '[5,6]'
assert split('12') == '[6,6]'
assert split('[[[[0,7],4],[15,[0,13]]],[1,1]]') == '[[[[0,7],4],[[7,8],[0,13]]],[1,1]]'
assert split('[[[[0,7],4],[[7,8],[0,13]]],[1,1]]') == '[[[[0,7],4],[[7,8],[0,[6,7]]]],[1,1]]'
assert split('[[[[0,7],4],[[7,8],[0,13]]],[1,21]]') == '[[[[0,7],4],[[7,8],[0,[6,7]]]],[1,21]]'

assert reduce('[[[[[4,3],4],4],[7,[[8,4],9]]],[1,1]]') == '[[[[0,7],4],[[7,8],[6,0]]],[8,1]]'

assert add('[1,2]', '[[3,4],5]') == '[[1,2],[[3,4],5]]'
assert add('[[[[4,3],4],4],[7,[[8,4],9]]]', '[1,1]') == reduce('[[[[[4,3],4],4],[7,[[8,4],9]]],[1,1]]')

assert add('[[[0,[4,5]],[0,0]],[[[4,5],[2,6]],[9,5]]]', '[7,[[[3,7],[4,3]],[[6,3],[8,8]]]]') == '[[[[4,0],[5,4]],[[7,7],[6,0]]],[[8,[7,7]],[[7,9],[5,0]]]]'
assert add('[[[[4,0],[5,4]],[[7,7],[6,0]]],[[8,[7,7]],[[7,9],[5,0]]]]', '[[2,[[0,8],[3,4]]],[[[6,7],1],[7,[1,6]]]]') == '[[[[6,7],[6,7]],[[7,7],[0,7]]],[[[8,7],[7,7]],[[8,8],[8,0]]]]'

assert magnitude(42) == 42
assert magnitude([9,1]) == 29
assert magnitude([[9,1],[1,9]]) == 129
assert magnitude([[1,2],[[3,4],5]]) == 143
assert magnitude([[[[8,7],[7,7]],[[8,6],[7,7]]],[[[0,7],[6,6]],[8,7]]]) == 3488

f = open('input.txt')
t = f.read()
f.close()

so_far = None
for line in t.split('\n'):
    print(so_far, line)
    if so_far is None:
        so_far = line
    else:
        so_far = add(so_far, line)

print(magnitude(str_to_list(so_far)))

