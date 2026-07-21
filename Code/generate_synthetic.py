"""
===============================================================================
CSC 2400 — Term Project: Unweighted Set Cover Problem (SCP)
Module: Synthetic Instance Generator (OR-Library Format)
Author: Matthew Richardson
===============================================================================
Description:
    Generates scalable benchmark datasets following a powers-of-2 sequence.
    Exports files in Beasley's OR-Library sparse column format to ensure 100%
    compatibility with the project parser.
===============================================================================
"""

import os
import numpy as np


def generate_synthetic_instance(num_elements, num_subsets, density=0.1, seed=42):
    """This function generates a valid binary matrix for the Unweighted Set
    Covering Problem.

    Rows = Elements to cover (Universe)
    Columns = Subsets available
    """
    np.random.seed(seed)

    # Generate a random boolean matrix based on target density
    matrix = np.random.rand(num_elements, num_subsets) < density

    # Crucial step: Ensure every single row is covered at least once
    # so the instance has a guaranteed valid mathematical solution
    for i in range(num_elements):
        if not np.any(matrix[i]):
            random_col = np.random.randint(0, num_subsets)
            matrix[i, random_col] = True

    return matrix.astype(int)


def save_synthetic_dataset():
    # Powers of 2 sizing sequence dictated by deliverable 1 feedback
    sizes = [64, 128, 256, 512, 1024, 2048]
    output_dir = "References/Synthetic"
    os.makedirs(output_dir, exist_ok=True)

    print("==================================================")
    print("          SYNTHETIC INSTANCE GENERATOR            ")
    print("==================================================")

    for size in sizes:
        # Scaling elements (rows) proportionally alongside subsets (columns)
        rows = size // 4  # e.g., 64 subsets covers a universe of 16 elements
        cols = size

        matrix = generate_synthetic_instance(rows, cols, density=0.15, seed=size)
        filename = os.path.join(output_dir, f"synth_{size}.txt")

        # Write out using standard spaces matching the Beasley standard parsing interface
        with open(filename, "w") as f:
            # Header: rows (universe size) and cols (num subsets)
            f.write(f"{rows} {cols}\n")

            # Beasley OR-Library expects cost array for subsets (unweighted = 1.0 each)
            f.write(" ".join(["1"] * cols) + "\n")

            # Beasley OR-Library row mapping:
            # For each element row: [count of covering columns] [1-based column indices...]
            for row in matrix:
                # Find indices where subset covers row (+1 for 1-based Beasley indexing)
                covering_cols = [
                    str(col_idx + 1)
                    for col_idx, is_covered in enumerate(row)
                    if is_covered == 1
                ]
                f.write(f"{len(covering_cols)} " + " ".join(covering_cols) + "\n")

        print(f"[GENERATOR] Created: {filename} ({rows}x{cols})")
    print("==================================================\n")


if __name__ == "__main__":
    save_synthetic_dataset()
