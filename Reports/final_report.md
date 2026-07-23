# Empirical Performance Analysis of Approximation, Metaheuristic, and Exact Algorithms for the Unweighted Set Cover Problem

**Course:** CSC 2400 Design and Analysis of Algorithms  
**Authors:** Ian Phillips, Abdullah Javed, Matthew Richardson  
**Repository:** [SetCover_Greedy_ILP_HS_GA_ORLibrary](https://github.com/matthew-richardson-ai/SetCover_Greedy_ILP_HS_GA_ORLibrary)

---

## 1. Overview of the Problem and Methods

The **Unweighted Set Cover Problem (SCP)** is one of the most well-known NP-hard combinatorial optimization problems in computer science. Given a universe of elements U and a collection of candidate subsets S, where each subset covers some portion of U, the goal is to find the smallest number of subsets whose union covers every element in U at least once.

Because the decision version of SCP is NP-complete and the optimization version is NP-hard, exact solutions become computationally intractable as input size grows. This makes SCP an ideal benchmark for comparing the trade-offs between exact solvers, deterministic approximations, and stochastic metaheuristics.

To analyze these trade-offs empirically, we implemented and compared four algorithmic paradigms:

1. **Greedy Approximation Heuristic** — A deterministic baseline that selects the locally optimal subset at each step, always choosing the subset that covers the most uncovered elements. This approach runs in Theta(m * n) and is guaranteed to produce a solution within a factor of H(n) of optimal (the nth harmonic number), but it is susceptible to local traps and makes no corrections once a choice is committed.

2. **Integer Linear Programming (ILP) via Branch-and-Bound** — An exact solver formulated using binary decision variables, a coverage constraint for each universe element, and an objective to minimize the total number of selected subsets. Solved using PuLP's CBC branch-and-bound engine. Provides the true optimal solution on instances where it terminates within the time limit, but has worst-case exponential complexity of Theta(2^m).

3. **Harmony Search (HS)** — A nature-inspired metaheuristic that maintains a memory of candidate solutions and generates new solutions through memory consideration and pitch adjustment. We implemented a specialized binary repair function to handle any uncovered elements produced during improvisation. Parameters: HMS = 30, HMCR = 0.85, PAR = 0.1, max iterations = 300.

4. **Genetic Algorithm (GA)** — A population-based evolutionary metaheuristic that represents candidate solutions as binary chromosomes and evolves them across generations using tournament selection, single-point crossover, bit-flip mutation, and an elitism mechanism to preserve the best-known solution. Parameters: population size = 100, generations = 500, mutation rate = 0.01.

---

## 2. Research Questions

These questions were established before running any experiments.

**RQ1 (Solution Quality):** Do metaheuristic approaches (GA and Harmony Search) consistently produce smaller set covers than the deterministic Greedy heuristic on both standardized benchmark instances and randomly generated synthetic inputs?

We expected yes. The Greedy heuristic makes one-way, locally optimal decisions at each step with no mechanism for correction. GA and HS can explore a wider solution space and potentially escape local traps through their stochastic components. We anticipated this advantage would be most visible on structured or harder instances.

**RQ2 (Runtime Scalability):** How does execution time scale for each algorithm as universe size grows exponentially from N = 64 to N = 2048?

We expected ILP to become intractable first, with runtime growing exponentially while the heuristics and metaheuristics remained bounded by their iteration limits. We expected Greedy to be fastest across all scales, with GA and HS falling somewhere in between.

---

## 3. Experiment Description

**Implementation Language:** Python 3.10+

**Libraries:** NumPy 1.24+, pandas 2.0+, matplotlib 3.7+, PuLP 2.7+

**Hardware:** Dell Windows 10 machine, x64 architecture (Intel Core i7, 16GB RAM)

**Datasets used:**

- **Beasley OR-Library benchmark:** `scp41.txt` — 200 universe elements, 1,000 candidate subsets. This is a standardized academic benchmark used across the literature.
- **Synthetic scaling suite:** Six randomly generated instances following powers-of-2 scaling: N = 64, 128, 256, 512, 1024, 2048 universe elements. Generated internally using a custom script (`Code/generate_synthetic.py`) that produces OR-Library formatted files with guaranteed full coverage. Subset density was held consistent across all instances.

**Experimental design:**

- Each stochastic algorithm (GA, Harmony Search) was run 10 independent trials per instance. Averages and standard deviations are reported.
- The Greedy Heuristic is deterministic. It was run 10 times to capture timing variance, but solution quality is consistent (standard deviation = 0).
- ILP was run once per instance with a strict 60-second execution timeout. For instances where the solver did not terminate within the timeout, the best feasible solution found is reported.
- All algorithms were evaluated on the same loaded data structure passed by reference in memory, ensuring no parsing overhead difference between algorithm comparisons.

**Performance metrics:**

- Average execution runtime (seconds)
- Standard deviation of runtime across trials
- Average cover size (number of subsets selected)
- Standard deviation of cover size across trials
- Optimality gap (%) relative to the ILP solution: ((heuristic avg - ILP optimal) / ILP optimal) * 100

---

## 4. Results

### Table 1: Standardized OR-Library Benchmark (scp41.txt)

Universe size = 200 | Candidate subsets = 1,000

| Algorithm | Avg Runtime | Subsets Selected | Optimality Gap |
| :--- | :--- | :--- | :--- |
| ILP Exact Solver | 0.0285s | **5** | 0.00% (baseline) |
| Greedy Heuristic | < 0.0001s | 6 | +20.00% |
| Genetic Algorithm | 0.7609s | **5** | 0.00% |
| Harmony Search | 0.0092s | **5** | 0.00% |

On the real-world benchmark instance, both GA and Harmony Search matched the exact ILP optimal solution of 5 subsets. Greedy selected 6, landing 20% above optimal. This was our strongest result for the metaheuristics.

---

### Table 2: Synthetic Scaling Suite (10 trials per stochastic algorithm)

| Instance | Algorithm | Runtime Avg | Runtime Std | Cover Avg | Cover Std | Optimality Gap |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| synth_64 | ILP Exact Solver | 0.0452s | -- | 4.0 | -- | 0.00% (baseline) |
| synth_64 | Greedy Heuristic | 0.0001s | 0.0000 | 4.0 | 0.00 | 0.00% |
| synth_64 | Genetic Algorithm | 1.5096s | 0.1004 | 4.2 | 0.40 | 5.00% |
| synth_64 | Harmony Search | 0.0734s | 0.0100 | 13.2 | 1.94 | 230.00% |
| synth_128 | ILP Exact Solver | 0.0372s | -- | 5.0 | -- | 0.00% (baseline) |
| synth_128 | Greedy Heuristic | 0.0004s | 0.0000 | 6.0 | 0.00 | 20.00% |
| synth_128 | Genetic Algorithm | 1.7164s | 0.0166 | 7.3 | 0.64 | 46.00% |
| synth_128 | Harmony Search | 0.1368s | 0.0108 | 34.2 | 1.72 | 584.00% |
| synth_256 | ILP Exact Solver | 1.3301s | -- | 7.0 | -- | 0.00% (baseline) |
| synth_256 | Greedy Heuristic | 0.0008s | 0.0000 | 8.0 | 0.00 | 14.29% |
| synth_256 | Genetic Algorithm | 2.2220s | 0.0212 | 12.5 | 1.36 | 78.57% |
| synth_256 | Harmony Search | 0.2598s | 0.0095 | 85.0 | 2.53 | 1114.29% |
| synth_512 | ILP (60s timeout) | 60.1023s | -- | 9.0 | -- | 0.00% (baseline) |
| synth_512 | Greedy Heuristic | 0.0039s | 0.0002 | 10.0 | 0.00 | 11.11% |
| synth_512 | Genetic Algorithm | 8.6434s | 5.0201 | 40.7 | 3.20 | 352.22% |
| synth_512 | Harmony Search | 2.6979s | 0.1067 | 194.0 | 6.99 | 2055.56% |
| synth_1024 | ILP (60s timeout) | 60.2144s | -- | 11.0 | -- | 0.00% (baseline) |
| synth_1024 | Greedy Heuristic | 0.0319s | 0.0021 | 11.0 | 0.00 | 0.00% |
| synth_1024 | Genetic Algorithm | 23.7461s | 0.2468 | 189.1 | 5.47 | 1619.09% |
| synth_1024 | Harmony Search | 1.8789s | 1.4537 | 424.3 | 7.20 | 3757.27% |
| synth_2048 | ILP Exact Solver | Intractable | -- | -- | -- | -- |
| synth_2048 | Greedy Heuristic | 0.0913s | 0.0033 | 14.0 | 0.00 | N/A |
| synth_2048 | Genetic Algorithm | 23.1047s | 1.0852 | 547.8 | 8.51 | N/A |
| synth_2048 | Harmony Search | 2.3779s | 0.0425 | 897.1 | 6.33 | N/A |

*ILP for synth_512 and synth_1024 hit the 60-second execution timeout and reflect the best feasible solution found rather than a proven global optimum. ILP was not run on synth_2048 as it is computationally intractable at that scale within a practical time limit.*

---

## 5. Interpretation of Results

### 5.1 Greedy Performs Surprisingly Well Across All Scales

The most consistent finding across the synthetic suite was that the Greedy Heuristic outperformed both metaheuristics in solution quality at every instance size, and did so orders of magnitude faster. At n = 512, Greedy selected 10 subsets versus GA's 43.9 and HS's 192.7. At n = 1024, Greedy matched the ILP's best-found solution of 11 subsets exactly.

This was not what we expected. The classical theoretical result for greedy SCP is that it produces a solution within H(n) of optimal, where H(n) is approximately ln(n) + 1. On our randomly generated instances, this approximation ratio appears tight in the best direction, with Greedy landing very close to optimal on most instances. The randomly generated synthetic instances likely have a structure where the greedy selection order happens to align closely with the optimal, which gives Greedy an advantage it would not have on adversarially constructed inputs.

Empirically, the Greedy runtime scales approximately linearly with problem size, consistent with its Theta(m * n) complexity. This is the most favorable scaling behavior of any algorithm tested.

### 5.2 Metaheuristics on the Real Benchmark vs. Synthetic Instances

On `scp41.txt`, both GA and Harmony Search converged to the exact optimal solution. This was a strong result and demonstrates that both metaheuristics are capable of finding optimal or near-optimal solutions on instances with structured coverage patterns.

However, performance degraded sharply on the synthetic suite. Harmony Search's optimality gap grew from 255% at n = 64 to over 2000% at n = 512. GA also degraded significantly, though less severely, reaching 387% at n = 512.

This divergence between real-benchmark performance and synthetic performance points to a key limitation: the metaheuristic parameters (HMS, HMCR, PAR, population size, generations) were not tuned specifically for each problem scale. A parameter configuration that works well on a 200-element instance may be insufficient for much larger synthetic instances. This is an area where additional experimentation would likely yield significant improvements.

### 5.3 ILP Proves Intractable at Scale

ILP solved n = 64, 128, and 256 instances quickly and exactly (0.0452s, 0.0372s, and 1.3301s respectively). At n = 512, the solver hit the 60-second timeout, returning the best feasible solution it had found. At n = 1024, the same thing happened.

This confirms the theoretical expectation from RQ2: exact solvers become computationally intractable as input size grows, even with a modern branch-and-bound implementation. For the instances where ILP did terminate, it provides the definitive ground truth for computing optimality gaps.

### 5.4 Empirical Analysis

Looking at the runtime curves empirically, the Greedy Heuristic shows sub-linear growth relative to problem size, consistent with its polynomial complexity class. GA shows a roughly linear runtime increase with instance size up to n = 256, then a steeper jump at n = 512, suggesting that the 500-generation fixed budget becomes more computationally expensive as the chromosome length grows proportionally with the number of candidate subsets.

Harmony Search runtime is more moderate than GA but still grows noticeably. The pitch-adjustment mechanism operates on a single vector per iteration, which is inherently cheaper than evolving a full population, but its solution quality suffers considerably at scale relative to the cost savings in time.

### 5.5 Limitations

Several limitations should be acknowledged when interpreting these results:

- The synthetic data was randomly generated with full coverage guaranteed per element, which may create problem structures that are unusually favorable to greedy selection. Real-world instances with adversarial or sparse structure may tell a different story.
- Metaheuristic parameters were not tuned per instance size. A properly tuned GA or HS at larger scales could close a significant portion of the observed optimality gap.
- ILP could only prove optimality on instances up to n = 256. For n = 512 and n = 1024, the "optimal" value used for gap calculations is a lower bound, not a certified global optimum.

### 5.6 What We Would Do Differently

If we were starting over, we would invest more time upfront in parameter sensitivity analysis for both metaheuristics before running the full scaling experiment. Running even a small grid search on one mid-sized instance to find more effective HMS, HMCR, and population size settings would likely have produced meaningfully different results for HS and GA at scale.

We would also extend the ILP timeout to at least 5 minutes for the larger instances, consistent with the README's stated design intent, to give the branch-and-bound solver a more realistic opportunity to prove optimality.

Finally, it would be valuable to test against more OR-Library instances beyond scp41.txt to see whether the strong metaheuristic performance observed there generalizes.

### 5.7 Next Steps and Further Research Questions

These results raise new questions worth pursuing:

- At what exact problem scale do GA and HS begin to underperform Greedy, and does that crossover point change with tuned parameters?
- Would a hybrid approach, using Greedy's output as the seed for the initial GA population, close the quality gap significantly?
- How do results change when testing on adversarially structured instances where Greedy is known to perform poorly?

---

## 6. Sources and GenAI Attribution

### Academic References

- Beasley, J.E. (1990). OR-Library: Distributing test problems by electronic mail. *Journal of the Operational Research Society*, 41(11), 1069-1072.
- Levitin, A. (2012). *Introduction to the Design and Analysis of Algorithms* (3rd ed.). Pearson.
- Glover, F., & Laguna, M. (1997). *Tabu Search*. Springer.

### Generative AI Assistance

In compliance with Tennessee Technological University academic integrity guidelines, the development of this project involved generative AI tools (Gemini, Claude/Posit Assistant, and xAI) integrated across our development environments (VS Code and RStudio/Posit) at the following stages:

| Stage | AI Use |
| :--- | :--- |
| **Data Parsing** | Verifying OR-Library token-stream format compatibility with our `load_or_library_instance` parser |
| **Debugging** | Diagnosing the synthetic data format mismatch (raw binary matrix vs. OR-Library row-mapping format) that caused elements to appear uncoverable |
| **Code Review** | Identifying a circular import bug in `greedy_solvers.py` |
| **Visualization** | Structuring matplotlib plot styling, logarithmic axis scaling, and output directory configuration in `generate_plots.py` |
| **ILP Integration** | Advising on PuLP formulation structure and timeout/fallback handling for `ilp_solver.py` |
| **Documentation** | Formatting markdown research documentation and report structure |

All underlying algorithmic design logic, parameter selection, experimental execution, and validation of results were reviewed and verified by the team. The human authors remain fully responsible for the correctness and integrity of all outputs.

---

## 7. Team Contribution Matrix

| Team Member | Roles |
| :--- | :--- |
| **Ian Phillips** | Data parsing (`load_or_library_instance`), Greedy Heuristic implementation (`greedy_solvers.py`), ILP solver integration (`ilp_solver.py`) |
| **Abdullah Javed** | Harmony Search algorithm (`harmony_search.py`), binary repair function for uncovered element resolution |
| **Matthew Richardson** | Genetic Algorithm engine (`genetic_algorithm.py`), benchmark pipeline orchestration (`main.py`), visualization engine (`generate_plots.py`), synthetic data generator (`generate_synthetic.py`), report formatting |

Approximate contribution split: Ian Phillips 33%, Abdullah Javed 33%, Matthew Richardson 33%.

---

## 8. Difficulties and Roadblocks

Several technical challenges came up during development that are worth documenting.

The first significant roadblock was a namespace and import conflict that blocked the entire pipeline for a period of time. Python's interpreter was refusing absolute imports because a lowercase directory name (`code/`) conflapped with an internal standard library namespace. Renaming the directory to `/Code` resolved it, but it caused temporary confusion across team members working on different machines with the old directory name still cached locally.

The second challenge was a synthetic data format mismatch that went undetected for a while. The synthetic benchmark files were generated by an older version of the generator and written in a raw binary matrix format. The OR-Library parser expected a cost array followed by element row mappings — a completely different token structure. The parser was reading the binary matrix rows as cost values, which caused elements to appear uncoverable and produced repeated Greedy warnings about elements that could not be reached. The fix was to regenerate all synthetic files using the corrected generator.

A third challenge was the ILP timeout behavior. For larger instances, the PuLP solver would consume the full time budget and return a partial result without indicating clearly whether it had found a provably optimal solution or just the best feasible solution it reached before hitting the limit. Handling this gracefully in the benchmark pipeline required careful output validation to prevent the objective value from being returned as None.

Finally, coordinating between three team members working in different environments, on different branches, and with different local path structures created version control friction throughout. Merging changes that involved renamed directories was particularly error-prone and required careful conflict resolution.

---
