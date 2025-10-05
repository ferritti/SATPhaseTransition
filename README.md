# Phase Transition Analysis in k-SAT with WalkSAT

This project studies the phase transition in the Boolean satisfiability problem (k-SAT) by generating random k-CNF formulas and solving them with the WalkSAT algorithm. It produces plots showing:
- the probability that a formula is satisfiable as the m/n ratio (clauses/symbols) varies,
- the average number of iterations taken by WalkSAT.

## Project contents
- `common.py`: common imports (numpy, matplotlib, tqdm, etc.) and shared constants. Defines `NEG = '¬'` as the negation symbol.
- `kcnf_generator.py`: class `KCNFGenerator` to generate k-CNF formulas with:
  - n propositional symbols (letters A, B, ..., and also AA, AB, ... if needed),
  - m distinct clauses,
  - clauses of length k with distinct literals and non-tautological (they do not contain both X and ¬X).
- `walksat.py`: class `WalkSAT`, a randomized local SAT solver with parameters:
  - `formula`: list of clauses (each clause is a `frozenset` of literal strings, e.g., "A", "¬B"),
  - `max_flips`: maximum number of flips allowed (> 0),
  - `p`: probability of randomly choosing a symbol in an unsatisfied clause (0 ≤ p ≤ 1).
- `phase_transition.py`: runs the phase transition analysis:
  - generates formulas for various m/n ratios,
  - solves them with WalkSAT,
  - estimates the satisfiability probability and the average flips,
  - draws two plots with matplotlib.

## Requirements
- Python 3.8+ (3.10+ recommended)
- Python dependencies:
  - numpy
  - matplotlib
  - tqdm

Install dependencies with:
```bash
pip install numpy matplotlib tqdm
```

Note: the project uses the Unicode symbol `¬` (negation). Make sure your terminal/font supports Unicode.

## Quick start
From the terminal, move to the project folder and run:
```bash
python3 phase_transition.py
```
This will start the analysis with the default parameters:
- n = 50 (number of propositional symbols)
- k = 3 (literals per clause, i.e., 3-CNF)
- num_samples = 100 (formulas generated for each m/n ratio)
- num_ratios = 50 (number of m/n values between 0.5 and 8)

At the end, two plots will be shown:
1) Satisfiability probability P(satisfiable) vs m/n.
2) Average number of WalkSAT iterations vs m/n.

During execution you will see a progress bar (tqdm). The analysis may take from tens of seconds to several minutes depending on parameters and your machine.

## How to change parameters
The main parameters are defined in `phase_transition.py`:
- Function `run_analysis()`:
  ```python
  n = 50            # Number of propositional symbols
  k = 3             # Number of literals per clause (k-CNF)
  num_samples = 100 # Number of formulas for each m/n
  num_ratios = 50   # Number of m/n ratios to sample in [0.5, 8]
  ```
  Modify these values to customize the experiment.

- Function `analyze_phase_transition(num_symbols, len_clauses, num_samples, num_ratios)`:
  - Validates that `num_symbols > 0`, `len_clauses > 0`, `num_samples > 0`, `num_ratios >= 2`.
  - For each `ratio` (m/n) it computes `num_clauses = int(ratio * num_symbols)` and:
    - generates a k-CNF formula with `KCNFGenerator(num_symbols, num_clauses, len_clauses)`,
    - solves it with `WalkSAT(formula, max_flips=2000, p=0.5)` (you can change it in the file if you wish),
    - collects outcome (satisfiable or not) and number of iterations used.

- WalkSAT parameters (in `phase_transition.py`):
  ```python
  solver = WalkSAT(formula, 2000, 0.5)  # max_flips=2000, p=0.5
  ```
  You can increase `max_flips` or change `p` (0..1) to explore different behaviors.

## Examples
- Run with smaller parameters (faster):
  ```python
  # In phase_transition.py
  n = 30
  k = 3
  num_samples = 40
  num_ratios = 30
  ```
- Use WalkSAT manually on a generated formula:
  ```python
  from kcnf_generator import KCNFGenerator
  from walksat import WalkSAT

  gen = KCNFGenerator(num_symbols=20, num_clauses=80, len_clause=3)
  formula = gen.formula

  solver = WalkSAT(formula, max_flips=5000, p=0.4)
  model, flips = solver.solve()
  if model is not None:
      print("Satisfiable in", flips, "flips")
  else:
      print("No assignment found within", flips, "flips")
  ```

## Formula representation
- A literal is a string: e.g., "A" or "¬B" (the negation symbol is `NEG = '¬'`).
- A clause is a `frozenset` of distinct literals.
- A formula is a list of clauses.
- `KCNFGenerator` avoids tautologies: it does not produce clauses containing both `X` and `¬X`.

## Folder structure
```
AI project/
├── common.py
├── kcnf_generator.py
├── walksat.py
├── phase_transition.py
└── README.md
```

## Expected output
- A window with two subplots:
  - P(satisfiable) vs m/n (blue line with "+" markers).
  - Average iterations vs m/n (dashed line with "x" markers).
- In the console: progress messages and progress bar.

## Tips and troubleshooting
- Slow execution: reduce `num_samples` and/or `num_ratios`, or lower `n`.
- Too many unsatisfiable cases in the dense regime: increase `max_flips` or change `p`.
- Missing packages errors: install `numpy`, `matplotlib`, `tqdm` as indicated.
- Issues with the `¬` symbol: ensure the file is UTF-8 and the terminal supports Unicode.