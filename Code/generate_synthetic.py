import numpy as np
import os


def generate_synthetic_instance(num_elements, num_subsets, density=0.1, seed=42):
    """
    This function generates a valid binary matrix for the Unweighted Set Covering Problem.
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
            f.write(f"{rows} {cols}\n")
            for row in matrix:
                f.write(" ".join(map(str, row)) + "\n")

        print(f"[GENERATOR] Created: {filename} ({rows}x{cols})")
    print("==================================================\n")


if __name__ == "__main__":
    save_synthetic_dataset()
