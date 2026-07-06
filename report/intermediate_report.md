# CSC 2400: Term Project Intermediate Status Report for Deliverable 2

## 1. Current Coding Progress & Architectural Decisions
The core architectural foundation for the Unweighted Set Covering Problem (SCP) optimization framework is complete, functional, and pushed to the remote repository. 

### Completed Core Infrastructure:
* **Token-Stream Matrix Parser:** Developed a high-performance data parser inside the root-level driver (`main.py`). The parser reads standard space-wrapped token streams from J.E. Beasley’s OR-Library benchmark suite, establishes matrix dimensions, and safely shifts 1-based source indices down to 0-based Python array indices.
* **Genetic Algorithm Engine:** Fully implemented the population-based evolutionary metaheuristic (`Code/genetic_algorithm.py`). The engine utilizes vectorized NumPy operations to manage Tournament Selection, Single-Point Crossover, Boolean-masked Bit-Flip Mutation, and an Elitism preservation mechanism to safeguard historical best-fitness solutions across generations.
* **Pipeline Orchestration:** Built a centralized execution pipeline (`main.py`) that handles environment replication and serves as the single unified benchmark engine for all testing.

### Key Architectural Pivot:
During local environment verification, we encountered a critical standard library namespace conflict because our development folder was named `code/`. Python’s interpreter interpreted this as a call to its internal interactive shell library, blocking absolute and relative imports. We resolved this by standardizing our layout and renaming the directory to a capitalized `/Code` folder, satisfying both the internal compiler and the explicit repository criteria.

---

## 2. Experimental Framework & Scaling Plan
Our plan of experimentation has been directly translated into our orchestration architecture. Rather than running disconnected scripts, the unified driver loads a target benchmark instance and passes identical data array pointers to the solvers in memory, guaranteeing perfect fairness in testing conditions.

### Scaling Sequence:
1. **Beasley Benchmarks:** Primary evaluations will target standard benchmark instances `scp41` through `scp65`, analyzing scaling patterns as datasets expand from 200 rows × 1,000 columns to 200 rows × 2,000 columns.
2. **Synthetic Input Scaling:** Per instructor feedback, our automated scaling experiments will leverage exponential growth bounds (powers of 2), scaling input sizes dynamically from 64 up to 2048 variables to visually plot asymptotic complexity trends.

---

## 3. Team Experience & Current Standing
The overall cooperative experience has been highly productive, moving systematically from algorithmic design to concrete code. The main challenges faced thus far involved handling irregular token formatting in the raw data files and structuring the local system path to ensure seamless file I/O operations across different team members' operating systems.

### Module Integration Roadmap:
The project backbone is fully configured to accept the remaining algorithms. The upcoming implementation tasks are cleanly distributed without risk of overlapping code regressions:
* **Ian Phillips:** Currently finalising the deterministic Greedy Approximation heuristic and integrating the exact Integer Linear Programming (ILP) branch-and-bound solver into the unified driver.
* **Abdullah Javed:** Finalising the nature-inspired Harmony Search metaheuristic and coding the specialized binary repair routine required to resolve uncovered universe boundaries.
* **Matthew Richardson:** Next steps include writing the file-saving automation to dump runtime metrics directly to the `/results` folder and implementing `matplotlib` visualization scripts to auto-generate charts inside `/graphs`.