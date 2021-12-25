# Solution to day part 1 of 21 of AOC 2021, Dirac Dice
# https://adventofcode.com/2021/day/21

def move(space: int, d: int) -> int:
    """For parm current space and die roll, return the new space the pawn will land on."""
    return (space - 1 + d) % 10 + 1


assert move(4, 1) == 5
assert move(4, 3) == 7
assert move(10, 1) == 1
assert move(9, 2) == 1
assert move(9, 3) == 2

# k = (p1 space, p1 score, p2 space, p2 score).
# v = number of games with this status.
games = {(10, 0, 6, 0): 1}
print(games)
target = 21

who_next = 1            # Either player 1 or 2.
games_in_progress = True

while games_in_progress:

    # One turn.
    games_in_progress = False                       # Be optimistic that all games are completed.
    for roll in range(1, 3 + 1):                    # 3 rolls per turn.
        # One move.
        new_games = {}
        for p1_space, p1_score, p2_space, p2_score in games:
            num_games = games[(p1_space, p1_score, p2_space, p2_score)]

            if p1_score >= target or p2_score >= target:    # Finished game, so no need to keep moving pawns.
                if (p1_space, p1_score, p2_space, p2_score) in new_games:
                    old_games = new_games[(p1_space, p1_score, p2_space, p2_score)]
                    new_games[(p1_space, p1_score, p2_space, p2_score)] = num_games + old_games
                else:
                    new_games[(p1_space, p1_score, p2_space, p2_score)] = num_games

            else:
                games_in_progress = True
                for die in range(1, 3 + 1):            # Consider all possible die rolls: 1, 2, and 3.
                    if who_next == 1:
                        new_space = move(p1_space, die)

                        new_score = p1_score
                        if roll == 3:
                            new_score = new_score + new_space

                        if (new_space, new_score, p2_space, p2_score) in new_games:
                            new_games[(new_space, new_score, p2_space, p2_score)] += num_games
                        else:
                            new_games[(new_space, new_score, p2_space, p2_score)] = num_games

                    else:
                        new_space = move(p2_space, die)

                        new_score = p2_score
                        if roll == 3:
                            new_score = new_score + new_space

                        if (p1_space, p1_score, new_space, new_score) in new_games:
                            new_games[(p1_space, p1_score, new_space, new_score)] += num_games
                        else:
                            new_games[(p1_space, p1_score, new_space, new_score)] = num_games

        games = new_games.copy()

        print(len(games), who_next)

    who_next = {1: 2, 2: 1}[who_next]

p1_wins, p2_wins = 0, 0
for p1_space, p1_score, p2_space, p2_score in games:
    num_games = games[(p1_space, p1_score, p2_space, p2_score)]

    if p1_score >= target:
        p1_wins += num_games
    else:
        p2_wins += num_games

print(max(p1_wins, p2_wins))
