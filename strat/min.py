
from collections import Counter
from dataclasses import dataclass
from functools import reduce
from typing import List

from state import State
from word_list import dictionary, answers


@dataclass
class MinStrat:
    state_to_pick = {}

    possibles: List[str]


    def __init__(self):
        self.possibles = dictionary


    def pick(self, round, state):
        if round == 0:
            return "riant", 0
        if round == 1:
            return "socle", 0

        state_key = str(state)
        if state_key in MinStrat.state_to_pick:
            return MinStrat.state_to_pick[state_key]

        self.possibles = list(p for p in self.possibles if state.is_possible(p))

        scores = Counter()
        for possible in self.possibles:
            for pick in dictionary:
                pick_state = state.copy().play(possible, pick)
                scores[pick] += sum(1 for p in self.possibles if pick_state.is_possible(p))

        if len(scores) == 0:
            return None, None

        pick, size, _ = min(((p, s, state.is_possible(p)) for p, s in scores.items()), key=lambda psp: (psp[1], not psp[2]))

        MinStrat.state_to_pick[state_key] = (pick, size)
        return pick, size


    @staticmethod
    def score(words):
        score = 0
        state = State()
        for solution in answers:
            state.reset()
            for w in words:
                state.play(solution, w)
            score += sum(1 for possible in answers if state.is_possible(possible))
        return score