#!/usr/bin/env python3

from itertools import chain
import json
import sys

from state import State


def iter_state_to_pick(solution, picks):
    state = State()
    for i in range(1, len(picks) - 1):
        state.play(solution, picks[i])
        yield state.copy(), picks[i+1]


if __name__ == "__main__":
    gen = (line.strip().split(",") for line in sys.stdin if not line.isspace())
    gen = chain.from_iterable(iter_state_to_pick(split[0], split[1:]) for split in gen)
    states = {str(state): pick for state, pick in gen}
    json.dump(states, sys.stdout)