# Crossword AI (Constraint Satisfaction Solver)

A high-performance **Constraint Satisfaction Problem (CSP) solver** that generates valid crossword puzzles using **AI search algorithms and constraint propagation**.

---

## Overview
This project formulates crossword generation as a CSP and solves it using a combination of:
- **Backtracking search**
- **Arc consistency (AC-3)**
- **Heuristics for efficient search**

It produces valid crossword grids by assigning words that satisfy structural and overlapping constraints.

---

## Features
- **CSP-based modeling** of crossword generation  
- **Constraint propagation (AC-3)** for domain pruning  
- **Backtracking search with heuristics**
  - Minimum Remaining Values (MRV)
  - Degree heuristic
  - Least Constraining Value (LCV)  
- **Conflict detection & consistency enforcement**  
- **Optional image export** of generated crossword  

---

## Tech Stack
- Python 3.x  
- Standard library + PIL (for image generation)
