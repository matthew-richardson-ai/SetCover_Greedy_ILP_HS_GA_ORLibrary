"""
===============================================================================
CSC 2400 — Term Project: Unweighted Set Cover Problem (SCP) Benchmark Driver
Authors: Ian Phillips, Abdullah Javed, Matthew Richardson
===============================================================================
Description:
    Main execution driver for running single benchmark instances and
    automated scaling experiments across Greedy, GA, Harmony Search, and ILP.
===============================================================================
"""

import csv
import os
import time
from datetime import datetime
import numpy as np

# Pull in our algorithm solvers
from Code.generate_plots import generate_benchmark_plots
from Code.genetic_algorithm import run_genetic_algorithm
from Code.greedy_solvers import run_greedy_approach
from Code.harmony_search import run_harmony_search
from Code.ilp_solver import run_ilp_solver


def load_or_library_instance(file_path):
    """Loads and parses OR-Library text files.

    Beasley's benchmark files are formatted as a single stream of space-
    separated tokens rather than standard line-by-line rows.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Data instance missing from directory: {file_path}")

    with open(file_path, "r") as f:
        tokens = f.read().split()

    if not tokens:
        raise ValueError("The target data file is completely empty.")

    token_iter = iter(tokens)

    # Read header dimensions (rows = universe size, cols = candidate subsets)
    universe_size = int(next(token_iter))
    num_subsets = int(next(token_iter))

    # Parse costs (ignored for unweighted SCP, but needed to skip token offset)
    _costs = [float(next(token_iter)) for _ in range(num_subsets)]

    subsets = [[] for _ in range(num_subsets)]

    # Read element coverage row by row
    for row_idx in range(universe_size):
        num_covering_columns = int(next(token_iter))

        for _ in range(num_covering_columns):
            # OR-Library uses 1-based indexing; convert to 0-based for Python
            col_idx = int(next(token_iter)) - 1
            subsets[col_idx].append(row_idx)

    return subsets, universe_size


def main():
    print("=" * 70)
    print("      CSC 2400: UNWEIGHTED SET COVERING PROBLEM BENCHMARK DRIVER      ")
    print("=" * 70)

    target_instance = "References/scp41.txt"

    try:
        # Load test instance
        print(f"[DATA LOG] Reading instance: '{target_instance}'...")
        subsets, universe_size = load_or_library_instance(target_instance)
        print(f"[DATA LOG] Universe Size : {universe_size} elements")
        print(f"[DATA LOG] Total Subsets : {len(subsets)}\n")

        # ILP Exact Solver Run
        print("[ENGINE] Running ILP Exact Solver...")
        start_time_ilp = time.time()
        ilp_chromosome, ilp_fitness_score = run_ilp_solver(
            subsets=subsets, universe_size=universe_size
        )
        ilp_execution_runtime = time.time() - start_time_ilp

        # Genetic Algorithm Run
        print("\n[ENGINE] Running Genetic Algorithm...")
        pop_size = 100
        generations = 300
        mutation_rate = 0.01

        start_time = time.time()
        best_cover_chromosome, best_fitness_score = run_genetic_algorithm(
            subsets=subsets,
            universe_size=universe_size,
            pop_size=pop_size,
            generations=generations,
            mutation_rate=mutation_rate,
        )
        execution_runtime = time.time() - start_time

        # Harmony Search Run
        print("\n[ENGINE] Running Harmony Search...")
        start_time_hs = time.time()
        best_hs_chromosome, best_hs_fitness_score = run_harmony_search(
            subsets=subsets,
            universe_size=universe_size,
            hms=30,
            hmcr=0.85,
            par=0.1,
            max_iter=300,
        )
        hs_execution_runtime = time.time() - start_time_hs

        # Greedy Heuristic Run
        print("\n[ENGINE] Running Greedy Heuristic...")
        start_time_greedy = time.time()
        greedy_chromosome, greedy_fitness_score = run_greedy_approach(
            subsets=subsets, universe_size=universe_size
        )
        greedy_execution_runtime = time.time() - start_time_greedy

        # Results Summary
        print("\n" + "=" * 50)
        print("                 BENCHMARK METRICS SUMMARY        ")
        print("=" * 50)
        print(f" Target Benchmark File  : {target_instance}")
        print(f" ILP Runtime            : {ilp_execution_runtime:.4f} seconds")
        print(f" ILP Optimal Cover Size : {ilp_fitness_score} subsets utilized")
        print("-" * 50)
        print(f" GA Runtime             : {execution_runtime:.4f} seconds")
        print(f" GA Cover Size          : {best_fitness_score} subsets utilized")
        print("-" * 50)
        print(f" HS Runtime             : {hs_execution_runtime:.4f} seconds")
        print(f" HS Cover Size          : {best_hs_fitness_score} subsets utilized")
        print("-" * 50)
        print(f" Greedy Runtime         : {greedy_execution_runtime:.4f} seconds")
        print(f" Greedy Cover Size      : {greedy_fitness_score} subsets utilized")
        print("=" * 50)

        selected_indices = [
            idx for idx, selected in enumerate(ilp_chromosome) if selected == 1
        ]
        print(f" ILP Optimal Subset Indices: {selected_indices}")
        print("=" * 50)

    except FileNotFoundError:
        print(f"\n[ERROR] Could not find data file: '{target_instance}'")
        print("-> Ensure benchmark files are placed in 'References/'.")
    except Exception as e:
        print(f"\n[ERROR] Execution failed: {e}")


def run_full_experiment():
    # Synthetic benchmark suite scaling by powers of 2
    instances = [
        "References/Synthetic/synth_64.txt",
        "References/Synthetic/synth_128.txt",
        "References/Synthetic/synth_256.txt",
        "References/Synthetic/synth_512.txt",
        "References/Synthetic/synth_1024.txt",
        "References/Synthetic/synth_2048.txt",
    ]

    timestamp = datetime.now().strftime("%Y-%m-%d_%H%M%S")
    results_file = f"Results/benchmark_metrics_{timestamp}.csv"
    latest_file = "Results/benchmark_metrics_latest.csv"

    headers = [
        "Instance",
        "Algorithm",
        "Trials",
        "Runtime_Avg",
        "Runtime_Std",
        "CoverSize_Avg",
        "CoverSize_Std",
        "Optimality_Gap",
    ]

    print("==================================================")
    print(f"  LAUNCHING FULL BENCHMARK SUITE [{timestamp}]    ")
    print("==================================================")

    os.makedirs("Results", exist_ok=True)

    for target_path in [results_file, latest_file]:
        with open(target_path, mode="w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(headers)

    for instance in instances:
        print(f"\n[BENCHMARK] Processing: {instance}")
        subsets, universe_size = load_or_library_instance(instance)

        # --- ILP EXACT SOLVER BASELINE ---
        print(" -> Running ILP Exact Solver for baseline...")
        ilp_start = time.time()
        _, ilp_opt_cover = run_ilp_solver(subsets, universe_size, time_limit_sec=60)
        ilp_runtime = time.time() - ilp_start

        ilp_row = [
            os.path.basename(instance),
            "ILP Exact Solver",
            1,
            f"{ilp_runtime:.4f}",
            "0.0000",
            f"{ilp_opt_cover:.1f}",
            "0.00",
            "0.00%",
        ]

        for target_path in [results_file, latest_file]:
            with open(target_path, mode="a", newline="") as f:
                csv.writer(f).writerow(ilp_row)

        print(
            f" -> ILP complete. Optimal Cover Size: {ilp_opt_cover} | Runtime: {ilp_runtime:.4f}s"
        )

        # Helper to compute optimality gap
        def calc_gap(heuristic_avg, optimal_val):
            if optimal_val == 0:
                return "0.00%"
            gap = ((heuristic_avg - optimal_val) / optimal_val) * 100
            return f"{gap:.2f}%"

        # --- GREEDY TRIALS ---
        greedy_runtimes, greedy_covers = [], []
        for trial in range(10):
            start_time = time.time()
            _, best_fitness = run_greedy_approach(subsets, universe_size)
            greedy_runtimes.append(time.time() - start_time)
            greedy_covers.append(best_fitness)

        greedy_cover_avg = np.mean(greedy_covers)
        greedy_row = [
            os.path.basename(instance),
            "Greedy Heuristic",
            10,
            f"{np.mean(greedy_runtimes):.4f}",
            f"{np.std(greedy_runtimes):.4f}",
            f"{greedy_cover_avg:.1f}",
            f"{np.std(greedy_covers):.2f}",
            calc_gap(greedy_cover_avg, ilp_opt_cover),
        ]

        for target_path in [results_file, latest_file]:
            with open(target_path, mode="a", newline="") as f:
                csv.writer(f).writerow(greedy_row)

        print(
            f" -> Greedy complete. Avg Runtime: {np.mean(greedy_runtimes):.4f}s | Avg Cover: {greedy_cover_avg:.1f} | Gap: {calc_gap(greedy_cover_avg, ilp_opt_cover)}"
        )

        # --- GENETIC ALGORITHM TRIALS ---
        ga_runtimes, ga_covers = [], []
        for trial in range(10):
            start_time = time.time()
            _, best_fitness = run_genetic_algorithm(subsets, universe_size)
            ga_runtimes.append(time.time() - start_time)
            ga_covers.append(best_fitness)

        ga_cover_avg = np.mean(ga_covers)
        ga_row = [
            os.path.basename(instance),
            "Genetic Algorithm",
            10,
            f"{np.mean(ga_runtimes):.4f}",
            f"{np.std(ga_runtimes):.4f}",
            f"{ga_cover_avg:.1f}",
            f"{np.std(ga_covers):.2f}",
            calc_gap(ga_cover_avg, ilp_opt_cover),
        ]

        for target_path in [results_file, latest_file]:
            with open(target_path, mode="a", newline="") as f:
                csv.writer(f).writerow(ga_row)

        print(
            f" -> GA complete. Avg Runtime: {np.mean(ga_runtimes):.4f}s | Avg Cover: {ga_cover_avg:.1f} | Gap: {calc_gap(ga_cover_avg, ilp_opt_cover)}"
        )

        # --- HARMONY SEARCH TRIALS ---
        hs_runtimes, hs_covers = [], []
        for trial in range(10):
            start_time = time.time()
            _, best_fitness = run_harmony_search(subsets, universe_size)
            hs_runtimes.append(time.time() - start_time)
            hs_covers.append(best_fitness)

        hs_cover_avg = np.mean(hs_covers)
        hs_row = [
            os.path.basename(instance),
            "Harmony Search",
            10,
            f"{np.mean(hs_runtimes):.4f}",
            f"{np.std(hs_runtimes):.4f}",
            f"{hs_cover_avg:.1f}",
            f"{np.std(hs_covers):.2f}",
            calc_gap(hs_cover_avg, ilp_opt_cover),
        ]

        for target_path in [results_file, latest_file]:
            with open(target_path, mode="a", newline="") as f:
                csv.writer(f).writerow(hs_row)

        print(
            f" -> HS complete. Avg Runtime: {np.mean(hs_runtimes):.4f}s | Avg Cover: {hs_cover_avg:.1f} | Gap: {calc_gap(hs_cover_avg, ilp_opt_cover)}"
        )

    print("\n==================================================")
    print(f"[SUCCESS] Experiment complete. Saved to: {results_file}")
    print("==================================================")

    # Automatically trigger plot generation using the newly written CSV
    print("\n[PIPELINE] Launching plotting engine...")
    generate_benchmark_plots()


if __name__ == "__main__":
    run_full_experiment()
    main()
