# Solution to day 4 of AOC 2021, Giant Squid
# https://adventofcode.com/2021/day/4

class Board:

    def __init__(self, numbers: []):
        self.completed = False

        # def cartesian_to_grid(x, y): return y * 5 + x
        # so...
        #   grid[0] is top left corner.
        #   grid[4] is top right corner.
        #   grid[12] is centre.
        #   grid[24] is bottom right.
        self.grid = {}

        g = 0
        for row in numbers:
            num_list = row.split(' ')
            while len(num_list) > 0:
                possible_num = num_list.pop(0)
                if possible_num != '':                          # Sometimes there are double spaces between numbers.
                    self.grid[g] = possible_num
                    g += 1

    def is_winner(self) -> bool:
        """Returns True if the board has either a complete row or a complete column."""
        for i in range(5):
            row_fail, col_fail = False, False           # Assume both row & column about to be checked are winners.
            for j in range(5):
                if self.grid[i * 5 + j] != '*':
                    col_fail = True
                if self.grid[i + j * 5] != '*':
                    row_fail = True
            if not row_fail or not col_fail:
                self.completed = True
                return True
        return False

    def mark(self, drawn_number: str):
        """Mark off the parm drawn number on the board by setting it to a star."""
        for g in self.grid:
            if self.grid[g] == drawn_number:
                self.grid[g] = '*'

    def sum_unmarked(self) -> int:
        """Return the sum of the non-star numbers on the grid."""
        total = 0
        for g in self.grid:
            if self.grid[g] != '*':
                total += int(self.grid[g])
        return total


f = open('input.txt')
t = f.read()
f.close()
r = t.split('\n')

selections = r.pop(0).split(',')                # List of number selections, as list if strings.

boards = []
while len(r) > 0:
    r.pop(0)                                    # Discard the blank line between each board.

    five_rows = []
    while len(five_rows) < 5:
        five_rows.append(r.pop(0))

    boards.append(Board(five_rows))

winner_count = 0
while winner_count < len(boards):               # Loop until all boards completed.
    drawn = selections.pop(0)
    for b in boards:
        if not b.completed:
            b.mark(drawn)
            if b.is_winner():
                winner_count += 1
                if winner_count == 1 or winner_count == len(boards):
                    print(b.sum_unmarked() * int(drawn))
