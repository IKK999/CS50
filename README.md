# Knights & Knaves AI (Logic + Model Checking)

A compact AI project that solves classic **Knights and Knaves** logic puzzles by converting natural-language statements into **propositional logic** and using **model checking** to infer which roles (Knight/Knave) must be true.

## Why this is interesting

- **AI reasoning, not heuristics**: solutions come from logical entailment over a knowledge base.
- **Clean logic abstraction**: reusable sentence types (`And`, `Or`, `Not`, `Implication`, `Biconditional`, `Symbol`) with evaluation over truth assignments.
- **End-to-end pipeline**: encode puzzle statements → build knowledge base → check entailment → print forced conclusions.

## How it works (high level)

- Each person’s role is represented as symbols like `"A is a Knight"` / `"A is a Knave"`.
- Puzzle constraints are expressed as a single knowledge base formula (an `And` of rules).
- The solver uses **truth-table model checking**: it enumerates all possible assignments for symbols and verifies whether the knowledge base **entails** a queried symbol.

Core algorithm: `model_check(knowledge, query)` in `logic.py`.

## Run

Requires Python 3.

```bash
python puzzle.py
```

The program prints, for each puzzle, the symbols that are logically entailed by the puzzle’s knowledge base (i.e., facts that must be true in all models consistent with the constraints).

## Project layout

- `logic.py`: Propositional logic sentence classes + model checking (entailment) engine.
- `puzzle.py`: Knights/Knaves puzzles encoded as knowledge bases; prints inferred roles.

## Skills demonstrated

- **Knowledge representation** (encoding constraints as propositional logic)
- **Automated reasoning** (entailment via exhaustive model checking)
- **Readable abstractions** (sentence objects, symbol extraction, formula rendering)

