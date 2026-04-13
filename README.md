# Minesweeper AI (Logical Inference)

An interactive Minesweeper implementation with an **AI agent that plays using propositional-style reasoning**. The agent builds a knowledge base of constraints from revealed cells and **infers safe moves and mines via set-based sentence deduction**, falling back to a random move only when logic can’t prove a safe choice.

## Highlights (employer-relevant)

- **Constraint reasoning**: represents local board knowledge as sentences of the form *cells = mine_count* and performs inference by subset relationships.
- **Knowledge base updates**: propagates newly discovered safes/mines through all sentences to continually refine decisions.
- **Interactive demo**: a small `pygame` UI to play manually or step the AI with an **“AI Move”** button.
- **Clean, testable core**: game mechanics (`Minesweeper`) and reasoning engine (`MinesweeperAI`) are separated from the UI runner.

## Tech Stack

- **Language**: Python
- **UI**: `pygame`
- **Core concepts**: knowledge representation, inference, constraint propagation, set operations

## Run Locally

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python runner.py
```

## How the AI Works (quick)

- When a safe cell is revealed, the AI creates a `Sentence(neighbors, count)` describing how many mines exist in the unrevealed neighboring cells.
- If a sentence’s count is `0`, all its cells are **safe**. If the count equals the number of cells, all are **mines**.
- If one sentence’s cells are a subset of another, the AI derives a **new sentence** by subtraction (a classic constraint reduction step).
- The AI selects a **known-safe** move when available; otherwise it chooses a **random** move among cells not known to be mines.
