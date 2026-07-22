"""
===============================================================================
CSC 2400 — Term Project: Unweighted Set Cover Problem (SCP)
Module: Integer Linear Programming (ILP) Exact Solver Engine
Authors: Ian Phillips, Abdullah Javed, Matthew Richardson
===============================================================================
Description:
    Formulates and solves the Unweighted Set Cover Problem as a binary
    Integer Linear Program (ILP) using branch-and-bound. Provides the exact
    mathematical baseline for evaluating metaheuristics.
===============================================================================
"""

import pulp  # Requires pulp: pip install pulp


def run_ilp_solver(subsets, universe_size, time_limit_sec=60):
    """Solves the Set Covering Problem exactly using ILP.

    Parameters:
        subsets (list of list of int): Map of subset indices to covered
        universe elements.
        universe_size (int): Total number of unique elements to cover.
        time_limit_sec (int): Max solver runtime in seconds before cutoff.

    Returns:
        tuple: (best_chromosome, best_fitness)
            - best_chromosome (list of int): Binary array of selected subsets.
            - best_fitness (int): Minimal number of subsets required.
    """
    num_subsets = len(subsets)

    # Initialize minimization problem
    prob = pulp.LpProblem("Unweighted_Set_Cover", pulp.LpMinimize)

    # Decision variables: x_j = 1 if subset j is chosen, 0 otherwise
    x = [pulp.LpVariable(f"x_{j}", cat=pulp.LpBinary) for j in range(num_subsets)]

    # Objective: Minimize total subsets chosen
    prob += pulp.lpSum(x), "Total_Subsets_Picked"

    # Map elements to covering subsets for constraint building
    element_to_subsets = [[] for _ in range(universe_size)]
    for subset_idx, covered_elements in enumerate(subsets):
        for elem in covered_elements:
            if 0 <= elem < universe_size:
                element_to_subsets[elem].append(subset_idx)

    # Coverage constraints: Each element must be covered at least once
    for elem_idx, covering_subsets in enumerate(element_to_subsets):
        if covering_subsets:
            prob += (
                pulp.lpSum([x[j] for j in covering_subsets]) >= 1,
                f"Cover_Element_{elem_idx}",
            )

    # Solve using CBC solver with output silenced
    solver = pulp.PULP_CBC_CMD(msg=False, timeLimit=time_limit_sec)
    prob.solve(solver)

    # Extract binary solution vector
    best_chromosome = [0] * num_subsets
    for j in range(num_subsets):
        if pulp.value(x[j]) is not None and pulp.value(x[j]) >= 0.99:
            best_chromosome[j] = 1

    best_fitness = int(round(pulp.value(prob.objective)))

    return best_chromosome, best_fitness
