# TSPPC-Hybrid-Solver

This project presents a high-performance metaheuristic solver designed for the **Precedence Constrained Traveling Salesman Problem (TSPPC)**. It utilizes a hybrid approach to find the most efficient route while strictly adhering to complex operational constraints.

## Technical Architecture
The solver is built on a **Lamarckian** framework that combines global exploration with intense local refinement:

* **Hybrid Metaheuristic:** Integrates Genetic Algorithm (GA) for broad search space exploration and Simulated Annealing (SA) for deep local exploitation.
* **Lamarckian Evolution:** Enhancements found during local search phases (2-Opt) are directly "learned" and encoded back into the individual's DNA, passing these traits to future generations.
* **Advanced 2-Opt:** A comprehensive local search layer that untangles crossing paths and optimizes node sequences to minimize total distance.
* **Vectorized Computation:** Powered by `NumPy`, the solver uses an optimized distance matrix to handle 48-node datasets with high-speed processing.



## Project Constraints & Compliance
This solver is fully compliant with academic standards and the following industrial engineering constraints:

1. **Depot Constraint:** Every route strictly starts and ends at Location 1 (Depot).
2. **Precedence Hierarchy:** Priority labels from 1 to 5 are strictly maintained (1 < 2 < 3 < 4 < 5).
3. **Mathematical Precision:** Distances are calculated using Euclidean distance and rounded up (`np.ceil`) per industry standards.



## Installation & Usage
1. Ensure you have Python installed on your system.
2. Place `main.py` and `Sample Problem.txt` in the same directory.
3. Run the solver via terminal:
   ```bash
   python main.py
