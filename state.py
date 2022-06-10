from bisect import insort_left
from dataclasses import dataclass
from typing import List


@dataclass
class State:
    letters_inc: List[str]
    letters_exc: List[str]
    positions: List[str]
    not_positions: List[List[str]]


    def __init__(self):
        self.reset()


    def reset(self):
        self.letters_inc = []
        self.letters_exc = []
        self.positions = [None for _ in range(5)]
        self.not_positions = [list() for _ in range(5)]


    def copy(self):
        s = State()
        s.letters_inc = list(self.letters_inc)
        s.letters_exc = list(self.letters_exc)
        s.positions = list(self.positions)
        s.not_positions = list(list(p) for p in self.not_positions)
        return s


    def play(self, solution, guess):
        for i, letter in enumerate(guess):
            if letter == solution[i]:
                self.positions[i] = letter
                if letter in self.letters_inc:
                    self.letters_inc.remove(letter)
            elif letter in solution:
                if letter not in self.not_positions[i]:
                    insort_left(self.not_positions[i], letter)
                solution_sum = sum(l == letter for l in solution)
                positions_sum = sum(l == letter for l in self.positions)
                inc_sum = sum(l == letter for l in self.letters_inc)
                if positions_sum + inc_sum < solution_sum:
                    insort_left(self.letters_inc, letter)
            else:
                if letter not in self.letters_exc:
                    insort_left(self.letters_exc, letter)
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