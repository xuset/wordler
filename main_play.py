#!/usr/bin/env python3

from collections import Counter
from multiprocessing import Pool

from state import State
from strat.min import MinStrat
from word_list import answers


def play(strategy, solution):
    state = State()
    chosen = []
    scores = []
    won = False

    for round in range(6):
        guess, score = strategy.pick(round, state)
        chosen.append(guess)
        scores.append(score)
        if guess is None:
            break
        state.play(solution, guess)
        if guess == solution:
            won = True
            break
    return won, round + 1, solution, chosen, scores


def min_strat_play(solution):
    return play(MinStrat(), solution)


if __name__ == "__main__":
    with Pool(processes=6) as pool:
        win_count = 0
        total = 0
        for win, rounds, solution, chosen, scores in pool.imap_unordered(min_strat_play, answers):
            total += 1
            win_count += win
            win_str = "WIN " if win else "LOSS"
            losses = total - win_count
            print(f"{win_str}, {solution}, tries={rounds}, total={total}, losses={losses}, chosen={chosen}, scores={scores}", flush=True)