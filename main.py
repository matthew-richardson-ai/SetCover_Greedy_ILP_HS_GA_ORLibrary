import os
import time

# Pulling your optimization engine from src
from Code.genetic_algorithm import run_genetic_algorithm


def load_or_library_instance(file_path):
    """
    HUMAN TRANSLATION: This function opens the raw OR-Library text file (like scp41.txt),
    cleans up the formatting, and builds the mathematical data structure our algorithm needs.

    Beasley's OR-Library files are formatted as a giant, continuous stream of numbers separated
    by spaces, which makes standard line-by-line file reading completely useless.
    """
    # Defensive check: Make sure the file actually exists before trying to read it
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

    # STEP 1: The very first two numbers in an OR-Library file are ALWAYS the metadata header.
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
    target_instance = "references/scp41.txt"

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

        # 4. Final output display for your professor's grading script / team analysis
        print("\n" + "=" * 50)
        print("                 BENCHMARK METRICS SUMMARY        ")
        print("=" * 50)
        print(f" Target Benchmark File  : {target_instance}")
        print(f" Computational Runtime  : {execution_runtime:.4f} seconds")
        print(f" Optimal Cover Size     : {best_fitness_score} subsets utilized")
        print("=" * 50)

        # Quick data check to prove to your professor that the result is functional code
        selected_indices = [
            idx for idx, selected in enumerate(best_cover_chromosome) if selected == 1
        ]
        print(f" Selected Subset Indices: {selected_indices}")
        print("=" * 50)

    except FileNotFoundError:
        print(f"\n[ERROR] Missing data file: '{target_instance}'")
        print(
            "-> Make sure you put your OR-Library text files inside the 'references/' directory."
        )
    except Exception as e:
        print(f"\n[CRITICAL ERROR] Execution broken: {e}")


if __name__ == "__main__":
    main()
