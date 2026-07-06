# Comparative Algorithmic Analysis of the Unweighted Set Cover Problem

## Team Members & Contributors
* [Ian Phillips](https://github.com/iaphillips42) - Data Parsing, Greedy, & ILP Implementation
* [Abdullah Javed](https://github.com/Abdullah-Javed-023) - Harmony Search & Binary Repair Function
* [Matthew Richardson](https://github.com/matthew-richardson-ai) - Genetic Algorithm, Plotting, & Formatting

---

## Problem Description
This repository contains a comparative study of the **Unweighted Set Cover Problem (SCP)**. Given a universe of elements $`U`$ and a collection of subsets $`S`$ where each subset covers a portion of $`U`$, the objective is to find the minimum number of subsets required to cover every element in $`U`$ at least once. Because SCP is NP-complete in its decision form and NP-hard in its optimization form, finding exact solutions becomes computationally intractable as the input size scales.

### Implemented Algorithms
To analyze the trade-offs between execution speed and solution quality, we implement and benchmark four distinct algorithmic approaches:
1. **Greedy Approximation ($\Theta(m \cdot n)$):** A deterministic heuristic baseline that picks the locally optimal subset at each step.
2. **Integer Linear Programming (ILP) with Branch-and-Bound ($\Theta(2^m)$ worst-case):** An exact solver to establish mathematical optimality on smaller instances, restricted by a strict 5-minute execution timeout.
3. **Harmony Search (HS) ($\Theta(T \cdot HMS \cdot m)$):** A nature-inspired metaheuristic utilizing a specialized binary repair function to handle uncovered universe elements.
4. **Genetic Algorithm (GA) ($\Theta(G \cdot P \cdot m)$):** An evolutionary metaheuristic evaluating population-based solution generation via selection, crossover, and mutation.

---

## Dataset
Experiments are executed using the official **OR-Library Set Covering Problem benchmark suite** maintained by J.E. Beasley. Our primary evaluation focuses on instances `scp41` through `scp65`, scaling from 200 rows by 1,000 columns up to 200 rows by 2,000 columns. 

Per instructor feedback, synthetic input scaling sequences leverage exponential growth (powers of 2) beginning at 64 up to 2048 variables to clearly visualize asymptotic runtime trends.

---

## Repository Structure
This repository adheres to strict academic project organization guidelines:

```text
├── /Code            # Modular Python source files (Parser, Algorithms, Main Pipeline)
├── /results         # Raw experimental output logs (CSV/JSON formats)
├── /graphs          # High-resolution runtime, optimality gap, and standard deviation plots
├── /report          # Intermediate status updates and final research paper
├── /slides          # Presentation slide decks
├── /references      # Academic papers and theoretical documentation
├── README.md        # Project overview and reproduction instructions
└── requirements.txt # System dependencies for environment replication
