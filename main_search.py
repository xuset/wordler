#!/usr/bin/env python3

from collections import Counter
from itertools import combinations
from multiprocessing import Pool

from strat.min import MinStrat
from word_list import dictionary


def min_strat_score(words):
    return words, MinStrat.score(words)


if __name__ == "__main__":
    words_list = combinations(dictionary, 2)
    words_list = (w for w in words_list if all(count <= 1 for _, count in Counter("".join(w)).items()))
    words_list = (w for w in words_list if all(c in "eariotnslcuyh" for c in "".join(w)))

    with Pool(processes=6) as pool:
        for words, score in pool.imap_unordered(min_strat_score, words_list):
            print(*words, score, sep=",", flush=True)