# CSC 2400: Term Project Intermediate Status Report for Deliverable 2

## 1. Current Coding Progress & Architectural Decisions
The core architectural foundation for the Unweighted Set Covering Problem (SCP) optimization framework is complete, functional, and pushed to the remote repository. 

### Completed Core Infrastructure:
* **Token-Stream Matrix Parser:** Developed a high-performance data parser inside the project driver (`Code/main.py`). The parser reads standard space-wrapped token streams from J.E. Beasley’s OR-Library benchmark suite, establishes matrix dimensions, and safely shifts 1-based source indices down to 0-based Python array indices.
* **Genetic Algorithm Engine:** Fully implemented the population-based evolutionary metaheuristic (`Code/genetic_algorithm.py`). The engine utilizes vectorized NumPy operations to manage Tournament Selection, Single-Point Crossover, Boolean-masked Bit-Flip Mutation, and an Elitism preservation mechanism to safeguard historical best-fitness solutions across generations.
* **Pipeline Orchestration:** Built a centralized execution pipeline (`Code/main.py`) that handles environment replication and serves as the single unified benchmark engine for all testing.

---

## 2. Experimental Framework & Scaling Plan
Our plan of experimentation has been directly translated into our orchestration architecture. Rather than running disconnected scripts, the unified driver loads a target benchmark instance and passes identical data array pointers to the solvers in memory, guaranteeing perfect fairness in testing conditions.

### Scaling Sequence:
1. **Beasley Benchmarks:** Primary evaluations will target standard benchmark instances `scp41` through `scp65`, analyzing scaling patterns as datasets expand from 200 rows × 1,000 columns to 200 rows × 2,000 columns.
2. **Synthetic Input Scaling:** Per instructor feedback, our automated scaling experiments will leverage exponential growth bounds (powers of 2), scaling input sizes dynamically from 64 up to 2048 variables to visually plot asymptotic complexity trends.

---

## 3. Team Experience & Current Standing
The overall cooperative experience has been quite productive. We have moved systematically from algorithmic design to concrete code. The main challenges faced thus far involved handling irregular token formatting in the raw data files and structuring the local system path to ensure seamless file I/O operations across different team members' operating systems. In addition to this, we faced momentary version control issues between the repo updates and local machine updates. These conflicts have been resolved.

### Foundational Technical Challenges & Standardizations:
* **Namespace and Import Conflicts:** During local environment verification, we encountered an infrastructure hurdle where the Python interpreter blocked absolute and relative imports. This occurred because a lowercase directory name (`code/`) conflicted with an internal Python standard library namespace. We resolved this by standardizing our repository layout and renaming the directory to a capitalized `/Code` folder, satisfying both the internal compiler and the explicit repository structure criteria.
* **Memory and Representation Mapping:** A significant hurdle was determining a unified internal data representation. While the metaheuristics (GA and Harmony Search) operate efficiently on sparse boolean arrays representing subset selections, the exact Integer Linear Programming (ILP) formulation requires an explicit structural matrix coefficient mapping for constraint evaluation. Ensuring the data parser seamlessly provisions both representations without redundant memory overhead required meticulous engineering.

### Ongoing Algorithmic Refinement & Foundational Challenges:
While the Genetic Algorithm is complete, implementation and refinement for the remaining three algorithms are actively ongoing. Integrating multiple diverse paradigms—ranging from deterministic heuristics to mathematical programming—into a singular, unified pipeline has introduced unique structural hurdles:
* **Memory and Representation Mapping:** A significant hurdle was determining a unified internal data representation. While the metaheuristics (GA and Harmony Search) operate efficiently on sparse boolean arrays representing subset selections, the exact Integer Linear Programming (ILP) formulation requires an explicit structural matrix coefficient mapping for constraint evaluation. Ensuring the data parser seamlessly provisions both representations without redundant memory overhead required meticulous engineering. 
* **Algorithmic Synchronization:** Managing the transition between metaheuristic search spaces and exact solver states has required careful planning to prevent cross-module interference and ensure that standard evaluation metrics are captured uniformly.

### Our roadmap / future implementations:
The project backbone is fully configured to accept the remaining models. The upcoming implementation tasks are cleanly distributed without risk of overlapping code regressions:
* **Ian Phillips:** Currently finalizing the deterministic Greedy Approximation heuristic and integrating the exact Integer Linear Programming (ILP) branch-and-bound solver into the unified driver.
* **Abdullah Javed:** Finalizing the nature-inspired Harmony Search metaheuristic and coding the specialized binary repair routine required to resolve uncovered universe boundaries.
* **Matthew Richardson:** Next steps include writing the file-saving automation to dump runtime metrics directly to the `/Results` folder and implementing `matplotlib` visualization scripts to auto-generate charts inside `/Tables & Graphs`.
