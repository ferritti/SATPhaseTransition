# WalkSAT and the Phase Transition in Random SAT Problems

## Description
This project, developed for the Artificial Intelligence exam, explores the phase transition phenomenon in random SAT problems using the WalkSAT algorithm. It includes the generation of random k-CNF formulas, the verification of their satisfiability, and the analysis of results through graphs.

For more details on the implementation and results, refer to the report [here](https://github.com/ferritti/SATPhaseTransition/blob/main/SATPhaseTransition.pdf).

## Source Files Structure
- **`kcnf_generator.py`**  
  Generates random k-CNF formulas according to specified constraints.
  
- **`walksat.py`**  
  Implements the WalkSAT algorithm to verify the satisfiability of k-CNF formulas.
  
- **`phase_transition.py`**  
  Generates graphs to analyze and visualize the phase transition phenomenon in random SAT problems.
  
- **`common.py`**  
  Contains shared utility libraries.

## Instructions to Reproduce Results
To reproduce the results, simply run `phase_transition.py`, which already includes the parameter values needed to generate the relevant graphs.
