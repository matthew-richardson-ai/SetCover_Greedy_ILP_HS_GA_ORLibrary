"""
Greedy Approximation Heuristic for the Unweighted Set Covering Problem.
"""
from Code.greedy_solvers import run_greedy_approach

import numpy as np


def run_greedy_approach(subsets, universe_size):
    """
    Constructs a set cover solution using the classic greedy heuristic:
    at every step, select the subset that covers the largest number of
    still-uncovered universe elements, until the universe is fully covered.
    """
    num_subsets = len(subsets)
    chromosome = np.zeros(num_subsets, dtype=int)

    # Pre-convert every subset to a Python set once up front.
    # Set operations (difference, union) are O(1) amortized per element,
    # which is what keeps each selection round to O(m) instead of O(m*n).
    subset_pool = [set(s) for s in subsets]

    uncovered = set(range(universe_size))
    cover_size = 0

    # Guard against instances where some universe elements aren't
    # covered by any subset at all
    while uncovered:
        best_idx = -1
        best_gain = 0
        best_new_elements = None

        # Scan every not-yet-selected subset, measure how many
        # *uncovered* elements it would add if picked.
        for idx in range(num_subsets):
            if chromosome[idx] == 1:
                continue

            new_elements = subset_pool[idx] & uncovered
            gain = len(new_elements)

            if gain > best_gain:
                best_gain = gain
                best_idx = idx
                best_new_elements = new_elements

        # No remaining subset covers anything new -> infeasible instance.
        if best_idx == -1:
            print(
                f"[GREEDY WARNING] {len(uncovered)} universe elements "
                "cannot be covered by any remaining subset. Stopping early."
            )
            break

        # Commit the best subset found this round.
        chromosome[best_idx] = 1
        uncovered -= best_new_elements
        cover_size += 1

    return chromosome, cover_size
