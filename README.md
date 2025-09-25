# Python Chess Engine

A modular chess engine built in Python with Pygame for the graphical interface.  
This engine handles **game state management, valid move generation, special moves**, and basic AI for move suggestions.

A video demonstration will be added here soon.

---

## Features

- Complete **board representation** using an 8x8 2D list
- Generates **all valid moves** for each piece
- Supports **special moves**:
  - Castling (king-side and queen-side)
  - En passant
  - Pawn promotion
- Tracks **move history** to allow undo operations
- Detects **check, checkmate, and stalemate**
- Simple GUI with **highlighted moves and interactive board**
- AI-based **Smart Move Finder** to suggest optimal moves

---

## Implementation Details

- `GameState` class: Tracks the current board state, valid moves, move log, and special move rights.
- `Move` class: Represents moves, including special moves, and can generate chess notation.
- `CastelRights` class: Keeps track of castling rights for both players.
- Move generation considers checks to **filter out illegal moves**.
- GUI handles **user input, board rendering, piece animations, and highlighting valid moves**.

---

## Tech Stack

- **Language:** Python
- **Library:** Pygame
- **Algorithms:** Move generation, Minimax (Smart Move Finder)

---

## Installation and Run

1. Clone the repository:

```bash
git clone https://github.com/KirtanLakhotia/chess-engine.git
```
2. Install Pygame:
 ```bash
pip install pygame
```
3. Run the main driver
```bash
python ChessMain.py
```
4. Play against AI or manually make moves using mouse clicks
