
from collections import Counter
from dataclasses import dataclass
from typing import List
import json

from state import State
from word_list import dictionary, answers


@dataclass
class MinStrat:
    state_to_pick = {}

    possibles: List[str]
    chosen: List[str]


    def __init__(self):
        self.possibles = dictionary
        # self.chosen = ["riant", "socle"]
        self.chosen = ["roate"]
        MinStrat.load_states_to_picks()


    def pick(self, round, state):
        if round < len(self.chosen):
            return self.chosen[round], 0

        state_key = str(state)
        if state_key in MinStrat.state_to_pick:
            return MinStrat.state_to_pick[state_key]

        self.possibles = list(p for p in self.possibles if state.is_possible(p))

        scores = Counter()
        for possible in self.possibles:
            picks = dictionary
            if round == 1:
                picks = (pick for pick in picks if 1 <= sum(count > 1 for count in Counter(self.chosen[0] + pick).values()))
            for pick in picks:
                pick_state = state.copy().play(possible, pick)
                scores[pick] += sum(1 for p in self.possibles if pick_state.is_possible(p))

        if len(scores) == 0:
            return None, None

        pick, size, _ = min(((p, s, state.is_possible(p)) for p, s in scores.items()), key=lambda psp: (psp[1], not psp[2]))

        self.chosen.append(pick)
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


    @staticmethod
    def load_states_to_picks():
        if len(MinStrat.state_to_pick) != 0:
            return MinStrat.state_to_pick
        with open("states_to_picks.json", "r") as f:
            MinStrat.state_to_pick = {state_key: (pick, 0) for state_key, pick in json.load(f).items()}