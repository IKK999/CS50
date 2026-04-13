# Degrees of Separation (Graph Search / BFS)

A small but complete AI search project that finds the **shortest connection between two actors** via co-starring relationships (the “Kevin Bacon game” idea). It loads an IMDB-style dataset of people, movies, and cast lists into an in-memory graph, then uses **breadth-first search (BFS)** to guarantee the minimum number of steps.

## Why this is interesting

- **Graph modeling**: builds a bipartite-style graph from real-world CSV data (people ↔ movies) and queries it as a connectivity problem.
- **Optimal search**: uses **BFS** over an implicit neighbor function to return the shortest path (fewest co-star hops).
- **Practical UX detail**: handles **ambiguous names** by prompting for the intended person ID.
- **Clean data ingestion**: parses and indexes the dataset for efficient lookup (name → ids, person → movies, movie → stars).

## How it works (high level)

1. Load `people.csv`, `movies.csv`, and `stars.csv` into dictionaries/sets.
2. Treat each actor as a node; neighbors are actors who appeared in any of the same movies.
3. Run BFS from the source actor until the target is reached.
4. Reconstruct and print the path as (movie → actor) hops.

## Run

From the project directory:

```bash
python degrees.py
```

By default it uses the `large/` dataset. To run on the smaller dataset:

```bash
python degrees.py small
```

You’ll be prompted for two names; the program prints the number of degrees and the movie-by-movie connection.

## Dataset

- `small/`: tiny dataset for quick testing
- `large/`: larger dataset for more realistic graph traversal

## Tech

- **Language**: Python 3
- **Core concepts**: graph search, BFS frontier, path reconstruction, data indexing

