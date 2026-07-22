"""
===============================================================================
CSC 2400 — Term Project: Unweighted Set Cover Problem (SCP)
Module: Empirical Data Visualization & Plotting Engine
Author: Matthew Richardson
===============================================================================
Description:
    Reads benchmarking metrics from 'Results/benchmark_metrics_latest.csv'
    (or the most recent timestamped CSV file in Results/) and generates
    publication-grade comparative charts with embedded tracking timestamps for
    the final research report and presentation slides.

Output Artifacts:
    - Tables & Graphs/scaling_runtime_comparison.png
    - Tables & Graphs/solution_quality_comparison.png
===============================================================================
"""

import glob
import os
from datetime import datetime
import matplotlib.pyplot as plt
import pandas as pd


def generate_benchmark_plots():
    results_dir = "Results"
    output_dir = "Tables & Graphs"

    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)

    # Search for the latest CSV file inside Results/
    csv_files = glob.glob(os.path.join(results_dir, "benchmark_metrics_*.csv"))
    if os.path.exists(os.path.join(results_dir, "benchmark_metrics_latest.csv")):
        csv_file = os.path.join(results_dir, "benchmark_metrics_latest.csv")
    elif csv_files:
        csv_file = max(csv_files, key=os.path.getmtime)
    else:
        csv_file = os.path.join(results_dir, "benchmark_metrics.csv")

    if not os.path.exists(csv_file):
        print(f"[ERROR] Could not find metrics file at '{csv_file}'.")
        print("-> Make sure to run 'python Code/main.py' first!")
        return

    print(f"[PLOTTING ENGINE] Loading metrics from: {csv_file}")
    df = pd.read_csv(csv_file)

    # Extract instance scale integer (e.g., 'synth_64.txt' -> 64)
    df["Instance_Size"] = df["Instance"].str.extract(r"synth_(\d+)").astype(int)
    df = df.sort_values("Instance_Size")

    # Set timestamp watermark for tracking
    run_tag = datetime.now().strftime("%Y-%m-%d_%H%M%S")
    timestamp_display = datetime.now().strftime("%Y-%m-%d %H:%M")

    # Set clean styling for academic presentation
    plt.style.use("seaborn-v0_8-whitegrid")
    plt.rcParams["font.sans-serif"] = "DejaVu Sans"

    algorithms = df["Algorithm"].unique()
    colors = {
        "Greedy Heuristic": "#1f77b4",  # Muted Blue
        "Genetic Algorithm": "#d62728",  # Crimson Red
        "Harmony Search": "#2ca02c",  # Forest Green
    }
    markers = {
        "Greedy Heuristic": "o",
        "Genetic Algorithm": "s",
        "Harmony Search": "^",
    }

    # =========================================================================
    # PLOT 1: RUNTIME SCALING TRENDS (LOGARITHMIC SCALE)
    # =========================================================================
    plt.figure(figsize=(10, 6), dpi=300)

    for algo in algorithms:
        sub_df = df[df["Algorithm"] == algo]
        plt.plot(
            sub_df["Instance_Size"],
            sub_df["Runtime_Avg"],
            label=algo,
            color=colors.get(algo, "black"),
            marker=markers.get(algo, "o"),
            linewidth=2.5,
            markersize=8,
        )

    plt.yscale("log")
    plt.xscale("log", base=2)
    plt.xticks(
        [64, 128, 256, 512, 1024, 2048],
        ["64", "128", "256", "512", "1024", "2048"],
    )

    plt.title(
        "Algorithm Runtime Scaling Behavior (Log-Log Scale)",
        fontsize=14,
        fontweight="bold",
        pad=15,
    )
    plt.xlabel(
        "Instance Size / Variable Count (Powers of 2)",
        fontsize=12,
        labelpad=10,
    )
    plt.ylabel("Execution Runtime (Seconds - Log Scale)", fontsize=12, labelpad=10)
    plt.grid(True, which="both", linestyle="--", alpha=0.5)
    plt.legend(fontsize=11, frameon=True, facecolor="white", framealpha=0.9)

    # Watermark tracking timestamp on bottom right corner
    plt.figtext(
        0.99,
        0.01,
        f"Generated: {timestamp_display}",
        ha="right",
        fontsize=8,
        color="gray",
        style="italic",
    )
    plt.tight_layout()

    plot1_path = os.path.join(output_dir, "scaling_runtime_comparison.png")
    plot1_timestamped = os.path.join(output_dir, f"scaling_runtime_{run_tag}.png")
    plt.savefig(plot1_path)
    plt.savefig(plot1_timestamped)
    plt.close()
    print(f"[PLOTTING ENGINE] Created: {plot1_path}")

    # =========================================================================
    # PLOT 2: SOLUTION QUALITY COMPARISON (COVER SIZE)
    # =========================================================================
    plt.figure(figsize=(10, 6), dpi=300)

    for algo in algorithms:
        sub_df = df[df["Algorithm"] == algo]
        plt.plot(
            sub_df["Instance_Size"],
            sub_df["CoverSize_Avg"],
            label=algo,
            color=colors.get(algo, "black"),
            marker=markers.get(algo, "o"),
            linewidth=2.5,
            markersize=8,
        )

    plt.xscale("log", base=2)
    plt.xticks(
        [64, 128, 256, 512, 1024, 2048],
        ["64", "128", "256", "512", "1024", "2048"],
    )

    plt.title(
        "Solution Quality Comparison: Subsets Utilized (Lower is Better)",
        fontsize=14,
        fontweight="bold",
        pad=15,
    )
    plt.xlabel(
        "Instance Size / Variable Count (Powers of 2)",
        fontsize=12,
        labelpad=10,
    )
    plt.ylabel(
        "Average Cover Size (Number of Subsets Picked)", fontsize=12, labelpad=10
    )
    plt.grid(True, linestyle="--", alpha=0.5)
    plt.legend(fontsize=11, frameon=True, facecolor="white", framealpha=0.9)

    # Watermark tracking timestamp on bottom right corner
    plt.figtext(
        0.99,
        0.01,
        f"Generated: {timestamp_display}",
        ha="right",
        fontsize=8,
        color="gray",
        style="italic",
    )
    plt.tight_layout()

    plot2_path = os.path.join(output_dir, "solution_quality_comparison.png")
    plot2_timestamped = os.path.join(output_dir, f"solution_quality_{run_tag}.png")
    plt.savefig(plot2_path)
    plt.savefig(plot2_timestamped)
    plt.close()
    print(f"[PLOTTING ENGINE] Created: {plot2_path}")

    print("==================================================")
    print(" [SUCCESS] Plot generation complete!")
    print("==================================================")


if __name__ == "__main__":
    generate_benchmark_plots()
