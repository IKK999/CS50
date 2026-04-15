# Degrees AI (Graph Search Engine)

A search-based AI system that computes the shortest connection between actors via shared movies, demonstrating graph traversal, state-space search, and real-world data modeling.

---

## Overview

- This project models the “degrees of separation” problem as a graph where:
- Nodes represent actors
- Edges represent co-starring relationships
- The system finds the shortest path between two actors using Breadth-First Search (BFS), guaranteeing minimal degrees of separation.

---

## Features
- Graph-based problem modeling - Transforms real-world data into a connected network
- Breadth-First Search (BFS)
- Guarantees shortest path in an unweighted graph
- State-space exploration
- Systematically explores neighbors with frontier tracking
- Path reconstruction
- Backtracks through parent nodes to build the solution path
- Data ingestion pipeline
- Parses and links CSV datasets (people, movies, stars)

---

## Tech Stack
- Python 3.x
- Standard library (csv, sys)
- Core concepts: Graph theory, BFS, search algorithms
