# Solution to part 1 of day 21 of AOC 2021, Dirac Dice
# https://adventofcode.com/2021/day/21


class Die:

    def __init__(self):
        self.rolls = 0          # Number of times the dies has been rolled.
        self.value = None       # Value the die returned last time it was rolled.

    def roll(self):
        if self.value is None:  # This die always rolls 1 first.
            self.value = 1
        else:
            self.value += 1
            if self.value >= 101:
                self.value = 1      # ... and so on up to 100, after which it starts over at 1 again.

        self.rolls += 1


class Player:

    def __init__(self, start: int):
        self.space = start                  # Current space the player is on.
        self.score = 0
        self.winner = False


class Game:
    def __init__(self, p1_start: int, p2_start: int):
        self.players = [Player(p1_start), Player(p2_start)]
        self.die = Die()

    def one_roll(self, player_num: int):
        curr_space = self.players[player_num].space
        self.die.roll()
        new_space = (curr_space - 1 + self.die.value) % 10 + 1
        self.players[player_num].space = new_space

    def turn(self, player_num: int):
        for rolls in range(3):
            self.one_roll(player_num)
        self.players[player_num].score += self.players[player_num].space
        if self.players[player_num].score >= 1000:
            self.players[player_num].winner = True


test_die = Die()

assert test_die.rolls == 0
test_die.roll()
assert test_die.value == 1
assert test_die.rolls == 1
for i in range(100):
    test_die.roll()
assert test_die.value == 1
assert test_die.rolls == 101

test_game = Game(4, 8)
assert test_game.die.rolls == 0
assert test_game.die.value is None
assert test_game.players[0].space == 4
assert test_game.players[1].space == 8

test_game.one_roll(player_num=0)
assert test_game.players[0].space == 5

test_game.one_roll(player_num=0)
test_game.one_roll(player_num=0)
assert test_game.players[0].space == 10

test_game.turn(1)
assert test_game.players[1].space == 3
assert test_game.players[1].score == 3

test_game.one_roll(player_num=0)
test_game.one_roll(player_num=0)
test_game.one_roll(player_num=0)
assert test_game.players[0].space == 4

# ----

my_game = Game(10, 6)
curr_player = 0
game_over = False
while not game_over:
    my_game.turn(curr_player)
    game_over = my_game.players[curr_player].winner
    curr_player = (curr_player + 1) % 2

    print(my_game.die.rolls)

print(my_game.players[curr_player].score)
print(my_game.die.rolls * my_game.players[curr_player].score)
