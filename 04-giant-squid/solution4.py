# Solution to day 4 of AOC 2021, Giant Squid
# https://adventofcode.com/2021/day/4

class Board:

    def __init__(self, numbers: []):
        self.completed = False
        self.grid = {}

        i = 0
        for row in numbers:
            num_list = row.split(' ')
            while len(num_list) > 0:
                possible_num = num_list.pop(0)
                if possible_num != '':                          # Sometimes there are double spaces between numbers.
                    self.grid[i % 5, i // 5] = possible_num
                    i += 1

    def is_winner(self) -> bool:
        """Returns True if the board has either a complete row or a complete column."""
        for i in range(5):
            row_fail, col_fail = False, False           # Assume both row & column about to be checked are winners.
            for j in range(5):
                if self.grid[i, j] != '*':
                    col_fail = True
                if self.grid[j, i] != '*':
                    row_fail = True
            if not row_fail or not col_fail:
                self.completed = True
                return True
        return False

    def cell_to_coords(self, i: int) -> ():
        return i % 5, i // 5

    def get_cell(self, i: int) -> str:
        return self.grid[self.cell_to_coords(i)]

    def mark(self, drawn_number: str):
        """Mark off the parm drawn number on the board by setting it to a star."""
        for i in range(25):
            if self.get_cell(i) == drawn_number:
                self.grid[i % 5, i // 5] = '*'

    def sum_unmarked(self) -> int:
        """Return the sum of the non-star numbers on the grid."""
        total = 0
        for i in range(25):
            if self.get_cell(i) != '*':
                total += int(self.get_cell(i))
        return total

f = open('input.txt')
t = f.read()
f.close()
r = t.split('\n')

# print(r)

selections = r.pop(0).split(',')
print(selections)

# print()
# print(r)
# print()

boards = []
while len(r) > 0:
    r.pop(0)            # Discard blank line.

    five_rows = []
    while len(five_rows) < 5:
        five_rows.append(r.pop(0))

    # print(five_rows)
    # new_board = Board(five_rows)
    # print(new_board.grid[(0, 0)], new_board.grid[(4, 4)])
    boards.append(Board(five_rows))

winner_count = 0

while winner_count < len(boards):             # Loop until boards completed.
    drawn = selections.pop(0)
    for b in boards:
        if not b.completed:
            b.mark(drawn)
            if b.is_winner():
                winner_count += 1
                if winner_count == 1 or winner_count == len(boards):
                    print(b.sum_unmarked() * int(drawn))

