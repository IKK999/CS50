# PageRank AI (Python)

A production-style implementation of the PageRank algorithm, showcasing both **stochastic (sampling-based)** and **deterministic (iterative)** approaches to ranking nodes in a directed graph.

---

## Overview
This project simulates how search engines rank web pages by modeling link structures as a graph and computing node importance via PageRank.

It includes:
- HTML corpus parsing and graph construction
- Probabilistic transition modeling (random surfer)
- Dual PageRank implementations for validation and comparison

---

## Features
- **Two independent algorithms**
  - Monte Carlo sampling (probabilistic estimation)
  - Iterative convergence (deterministic solution)
- **Robust edge case handling**
  - Dangling nodes (pages with no outgoing links)
- **Normalized probability distributions**
- **Configurable parameters**
  - Damping factor
  - Number of samples
  - Convergence threshold

---

## Tech Stack
- Python 3.x (standard library only)
- No external dependencies
