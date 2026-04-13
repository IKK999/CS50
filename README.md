# Tic-Tac-Toe AI (Minimax)

An interactive Tic-Tac-Toe game with a **perfect-play AI**. The computer uses the **Minimax decision algorithm** to evaluate future game states and always chooses an optimal move—meaning it **never loses** (win or draw with correct play).

## Why this project matters

- **Search & decision-making**: Implements a classic game-search algorithm (Minimax) to compute optimal actions from any board position.
- **Clean separation of concerns**: Game logic + AI live in `tictactoe.py`, while the UI/interaction layer is in `runner.py`.
- **User-facing demo**: A simple Pygame interface makes the algorithm tangible and easy to evaluate in an interview.

## Tech stack

- **Language**: Python
- **UI**: Pygame
- **AI**: Minimax (full-depth search for Tic-Tac-Toe)

## Quickstart

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python runner.py
```

## How it works (high level)

- The board is represented as a 3×3 grid (`X`, `O`, or empty).
- On the AI’s turn, `minimax(board)` explores available moves recursively:
  - **Maximizing player** (`X`) selects moves that maximize outcome.
  - **Minimizing player** (`O`) selects moves that minimize outcome.
- Terminal states are scored via a simple utility function:
  - \(+1\) if `X` wins, \(-1\) if `O` wins, \(0\) for a draw.

## Repository layout

- `tictactoe.py`: board representation, rules, terminal/utility checks, and Minimax.
- `runner.py`: Pygame UI that lets a user play as `X` or `O` vs the AI.
- `requirements.txt`: dependency list.

