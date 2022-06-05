#!/usr/bin/env python3

from dataclasses import dataclass, field
from itertools import combinations, product
from collections import Counter
from multiprocessing import Pool
from typing import List

def load_words(file):
    return [line for line in (line.strip() for line in file) if line.isalpha()]


answers = load_words(open("wordle_oracle.txt", "r"))
dictionary = load_words(open("wordle_dictionary.txt"))


@dataclass
class State:
    letters_inc: List[str]
    letters_exc: List[str]
    positions: List[str]
    not_positions: List[List[str]]
    round: int


    def __init__(self):
        self.reset()


    def reset(self):
        self.letters_inc = []
        self.letters_exc = []
        self.positions = [None for _ in range(5)]
        self.not_positions = [list() for _ in range(5)]
        self.round = 0


    def copy(self):
        s = State()
        s.letters_inc = list(self.letters_inc)
        s.letters_exc = list(self.letters_exc)
        s.positions = list(self.positions)
        s.not_positions = list(list(p) for p in self.not_positions)
        s.round = self.round
        return s


    def play(self, solution, guess):
        for i, letter in enumerate(guess):
            if letter == solution[i]:
                self.positions[i] = letter
                if letter in self.letters_inc:
                    self.letters_inc.remove(letter)
            elif letter in solution:
                if letter not in self.not_positions[i]:
                    self.not_positions[i].append(letter)
                    self.not_positions[i].sort()
                solution_sum = sum(l == letter for l in solution)
                positions_sum = sum(l == letter for l in self.positions)
                inc_sum = sum(l == letter for l in self.letters_inc)
                if positions_sum + inc_sum < solution_sum:
                    self.letters_inc.append(letter)
                    self.letters_inc.sort()
            else:
                if letter not in self.letters_exc:
                    self.letters_exc.append(letter)
                    self.letters_exc.sort()
        # print(f"solution={solution}, positions={positions}, letters_inc={letters_inc}, guess={guess}")
        return self


    def is_possible(self, possible):
        for i, letter in enumerate(self.positions):
            if letter is None:
                continue
            if possible[i] != letter:
                return False
        for letter in self.letters_inc:
            if letter not in possible:
                return False
        for letter in self.letters_exc:
            if letter in possible:
                return False
        for i, letters in enumerate(self.not_positions):
            if possible[i] in letters:
                return False
        return True


    def iter_solution_space(self):
        return (solution for solution in answers if self.is_possible(solution))


def find_solution_space_size_for_start(guesses):
        space_size = 0
        state = State()
        for solution in answers:
            state.reset()
            for guess in guesses:
                state.play(solution, guess)
            space_size += sum(1 for _ in state.iter_solution_space())
        return (guesses, space_size)

memo={}

def min_strat():
    store = {"possibles": dictionary}

    def pick(round, state):
        if round == 0:
            return "roate", 0
        # if round == 0:
        #     return "riant", 0
        # if round == 1:
        #     return "socle", 0

        state_str = str(state)
        if state_str in memo:
            return memo[state_str][0], memo[state_str][1]

        guess_sizes = Counter()
        possibles = store["possibles"] = list(p for p in store["possibles"] if state.is_possible(p))
        for possible in possibles:
            for guess in dictionary:
                tmp_state = state.copy().play(possible, guess)
                guess_sizes[guess] += sum(1 for p in possibles if tmp_state.is_possible(p))
        if len(guess_sizes) == 0:
            return None, None
        guess, size, _ = min(((g, s, state.is_possible(g)) for g, s in guess_sizes.items()), key=lambda t: (t[1], -int(t[2])))
        memo[state_str] = (guess, size)
        # print(f"MIN_STRAT - guess={guess}, possible_size={size}")
        return guess, size

    return pick


def play(solution):
    strategy = min_strat()
    state = State()
    chosen = []
    won = False
    scores = []
    for round in range(6):
        guess, score = strategy(round, state)
        chosen.append(guess)
        scores.append(score)
        if guess is None:
            break
        state.play(solution, guess)
        # print(f"PLAY - round={round+1}, guess={guess}, state={state}, size={sum(1 for _ in state.iter_solution_space())}")
        if guess == solution:
            won = True
            break
    return won, round + 1, solution, chosen, scores


def main_play():
    with Pool(processes=6) as pool:
        win_count = 0
        total = 0
        for win, rounds, solution, chosen, scores in pool.imap_unordered(play, answers):
            total += 1
            win_count += win
            win_str = "WIN " if win else "LOSS"
            losses = total - win_count
            print(f"{win_str}, {solution}, tries={rounds}, total={total}, losses={losses}, chosen={chosen}, scores={scores}", flush=True)


def main_start_words():
    starting = (w for w in combinations(dictionary, 2) if all(count <= 1 for _, count in Counter("".join(w)).items()))
    starting = (w for w in starting if all(c in "eariotnslcuyh" for c in "".join(w)))
    starting = (w for w in starting if any(c in "h" for c in "".join(w)))
    # starting = ((w,) for w in dictionary if all(count <= 1 for _, count in Counter(w).items()))
    # starting = [("irate", "lousy"), ("raise", "youth")]
    with Pool(processes=6) as pool:
        for guesses, space_size in pool.imap_unordered(find_solution_space_size_for_start, starting):
            print(*guesses, space_size, sep=",", flush=True)

if __name__ == "__main__":
    # main_start_words()
    main_play()