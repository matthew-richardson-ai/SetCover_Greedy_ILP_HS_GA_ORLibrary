import os
import time
import csv
import numpy as np

# Pulls the main execution loop for our Genetic Algorithm from the companion module
from Code.genetic_algorithm import run_genetic_algorithm
from Code.harmony_search import run_harmony_search

def load_or_library_instance(file_path):
    """
    Opens the raw OR-Library text file (in ../References/scp41.txt),
    cleans up the formatting, and builds the mathematical data structure.

    Note: Beasley's OR-Library files are formatted as a continuous stream of numbers
    separated by spaces, which makes standard line-by-line file reading useless.
    """
    #  We want to make sure the file actually exists before trying to read it
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Data instance missing from directory: {file_path}")

    with open(file_path, "r") as f:
        # read().split() reads the entire file, throws away all newlines/tabs,
        # and turns it into a clean, flat list of standalone numbers (tokens).
        tokens = f.read().split()

    if not tokens:
        raise ValueError("The target data file is completely empty.")

    # An iterator lets us grab the numbers one by one in order via the next() function
    token_iter = iter(tokens)

    # STEP 1: The very first two numbers in an OR-Library file are always the metadata header.
    universe_size = int(next(token_iter))  # Number of rows (Total elements to cover)
    num_subsets = int(next(token_iter))  # Number of columns (Total available subsets)

    # STEP 2: The next chunk of numbers represents the cost of each individual subset.
    # Because our assignment focuses strictly on the UNWEIGHTED version (minimizing the count),
    # we just parse past these costs to get them out of the way of our element reader.
    _costs = [float(next(token_iter)) for _ in range(num_subsets)]

    # STEP 3: Create an empty list for every subset so we can store what elements they cover.
    subsets = [[] for _ in range(num_subsets)]

    # STEP 4: Read the rest of the file row-by-row (element-by-element).
    # The file is structured like this:
    # [How many subsets cover element 0] -> [List of those subset IDs]
    for row_idx in range(universe_size):
        num_covering_columns = int(
            next(token_iter)
        )  # Read how many columns cover this item

        for _ in range(num_covering_columns):
            # CRITICAL OPTIMIZATION: OR-Library data uses 1-based indexing (1 to N).
            # Python arrays use 0-based indexing (0 to N-1). We must subtract 1 here!
            col_idx = int(next(token_iter)) - 1

            # Map this universe element directly into the subset that owns it
            subsets[col_idx].append(row_idx)

    return subsets, universe_size


def main():
    print("=" * 70)
    print("      CSC 2400: UNWEIGHTED SET COVERING PROBLEM BENCHMARK DRIVER      ")
    print("=" * 70)

    # This points directly to the data file inside your references folder.
    # Swap out 'scp41.txt' with any other benchmark instance file to test different sets.
    target_instance = "References/scp41.txt"

    try:
        # 1. Parse and extract the data
        print(f"[DATA LOG] Attempting to read and parse: '{target_instance}'...")
        subsets, universe_size = load_or_library_instance(target_instance)
        print(f"[DATA LOG] Success! Target Universe Size : {universe_size} elements")
        print(f"[DATA LOG] Success! Total Available Subsets: {len(subsets)}\n")

        # 2. Setup your algorithm configuration parameters
        print("[ENGINE] Booting up Genetic Algorithm optimization loop...")
        pop_size = 100  # How many candidate solutions exist in our gene pool
        generations = 300  # How many evolutionary steps we run before stopping
        mutation_rate = (
            0.01  # 1% probability of flipping a bit to maintain genetic diversity
        )

        # 3. Time the execution to measure algorithmic performance (HPC Metric)
        start_time = time.time()

        best_cover_chromosome, best_fitness_score = run_genetic_algorithm(
            subsets=subsets,
            universe_size=universe_size,
            pop_size=pop_size,
            generations=generations,
            mutation_rate=mutation_rate,
        )

        execution_runtime = time.time() - start_time

        print("\n[ENGINE] Booting up Harmony Search optimization loop...")
        start_time_hs = time.time()
        
        best_hs_chromosome, best_hs_fitness_score = run_harmony_search(
            subsets=subsets, 
            universe_size=universe_size, 
            hms=30, hmcr=0.85, par=0.1, max_iter=300
        )
        
        hs_execution_runtime = time.time() - start_time_hs

        # 4. Final output display for your professor's grading script / team analysis
        print("\n" + "=" * 50)
        print("                 BENCHMARK METRICS SUMMARY        ")
        print("=" * 50)
        print(f" Target Benchmark File  : {target_instance}")
        print(f" GA Runtime             : {execution_runtime:.4f} seconds")
        print(f" GA Optimal Cover Size  : {best_fitness_score} subsets utilized")
        print("-" * 50)
        print(f" HS Runtime             : {hs_execution_runtime:.4f} seconds")
        print(f" HS Optimal Cover Size  : {best_hs_fitness_score} subsets utilized")
        print("=" * 50)

        # Quick data check for functional code verification
        selected_indices = [
            idx for idx, selected in enumerate(best_cover_chromosome) if selected == 1
        ]
        print(f" Selected Subset Indices: {selected_indices}")
        print("=" * 50)

    except FileNotFoundError:
        print(f"\n[ERROR] Missing data file: '{target_instance}'")
        print(
            "-> Make sure the OR-Library text files are inside the 'references/' directory."
        )
    except Exception as e:
        print(f"\n[CRITICAL ERROR] Execution broken: {e}")


# ... Keep all your existing imports and your load_or_library_instance() function up here ...


def run_full_experiment():
    # Array of benchmark files scaling exponentially
    instances = [
        "References/Synthetic/synth_64.txt",
        "References/Synthetic/synth_128.txt",
        "References/Synthetic/synth_256.txt",
        "References/Synthetic/synth_512.txt",
        "References/Synthetic/synth_1024.txt",
        "References/Synthetic/synth_2048.txt",
    ]

    results_file = "Results/benchmark_metrics.csv"
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
    print("        LAUNCHING LIVE BENCHMARK ENGINE           ")
    print("==================================================")

    os.makedirs("Results", exist_ok=True)

    with open(results_file, mode="w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(headers)

        for instance in instances:
            print(f"\n[BENCHMARK] Processing: {instance}")

            # 1. Load the actual data using your existing parser
            # (Adjust the function name if yours is slightly different, e.g., load_or_library_instance)
            subsets, universe_size = load_or_library_instance(instance)

            ga_runtimes = []
            ga_covers = []

            # Run 10 independent trials per file to collect standard deviation
            for trial in range(10):
                start_time = time.time()

                # 2. Run your actual Genetic Algorithm loop
                best_chromosome, best_fitness = run_genetic_algorithm(
                    subsets, universe_size
                )

                end_time = time.time()

                ga_runtimes.append(end_time - start_time)
                ga_covers.append(best_fitness)

            # Compute statistical metrics requested by the instructor
            runtime_avg = np.mean(ga_runtimes)
            runtime_std = np.std(ga_runtimes)
            cover_avg = np.mean(ga_covers)
            cover_std = np.std(ga_covers)

            # Write row to CSV
            writer.writerow([
                os.path.basename(instance),
                "Genetic Algorithm",
                10,
                f"{runtime_avg:.4f}",
                f"{runtime_std:.4f}",
                f"{cover_avg:.1f}",
                f"{cover_std:.2f}",
                "TBD (Awaiting ILP Baseline)",
            ])
            print(
                f" -> Finished 10 trials. Avg Runtime: {runtime_avg:.4f}s | Avg Cover: {cover_avg:.1f}"
            )

            hs_runtimes = []
            hs_covers = []
            
            for trial in range(10):
                start_time = time.time()
                best_chromosome, best_fitness = run_harmony_search(subsets, universe_size)
                end_time = time.time()
                
                hs_runtimes.append(end_time - start_time)
                hs_covers.append(best_fitness)
                
            hs_runtime_avg = np.mean(hs_runtimes)
            hs_runtime_std = np.std(hs_runtimes)
            hs_cover_avg = np.mean(hs_covers)
            hs_cover_std = np.std(hs_covers)
            
            # Write HS row to CSV
            writer.writerow([
                os.path.basename(instance),
                "Harmony Search",
                10,
                f"{hs_runtime_avg:.4f}",
                f"{hs_runtime_std:.4f}",
                f"{hs_cover_avg:.1f}",
                f"{hs_cover_std:.2f}",
                "TBD"
            ])
            print(f" -> Finished HS 10 trials. Avg Runtime: {hs_runtime_avg:.4f}s | Avg Cover: {hs_cover_avg:.1f}")

    print("\n==================================================")
    print(f"[SUCCESS] Batch execution complete. Saved to: {results_file}")
    print("==================================================")


# This replaces your old single-run block
if __name__ == "__main__":
    run_full_experiment()
    main()
