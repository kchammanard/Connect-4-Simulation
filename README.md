# Connect 4 AI Project

## 💡 Objective
Study how a 2 AI Agent system interacts with each other in a game of Connect 4, given random obstacle placement.

## Running
Clone Repository
```bash
git clone https://github.com/kchammanard/Connect-4-Simulation.git
```
Install dependencies
```bash
cd Connect-4-Simulation
pip install -r requirements.txt`
```
Run the program
```bash
python connect4-minimax.py
```

## Rules
1. Agents are allowed to stack their pieces anywhere on a 8x8 board.
2. An 'obstacle' will be placed at random turns.
   - Obstacles can be placed anywhere on the board to most effectively disrupt both players.
3. Winning conditions:
   1. Horizontal array of corresponding pieces.
   2. Vertical array of corresponding pieces.
   3. Diagonal array of corresponding pieces.
4. Each player has full observability of the board: they know where the winning condition of the opposing player is.

## Algorithms
### 1. Game Tree – Minimax
The minimax algorithm facilitates strategic decision-making by recursively exploring potential moves in the game tree, alternating between maximizing and minimizing players. At each level of recursion, the algorithm evaluates the current board position using an evaluation function, which provides a numerical score indicating the strength of the position for the maximizing player relative to the minimizing player. Then, the algorithm selects the move that maximizes the maximizing player's score and minimizes the minimizing player's score, ultimately determining the optimal move for the current player. Optional optimizations such as alpha-beta pruning were applied to reduce computational complexity.

### 2. Obstacle Placement Search
The obstacle placement search algorithm was used to determine the best slot to place an 'obstacle' to disrupt the progress of both players. In general, here is how it works:
1. Simulates placing an obstacle on a column.
2. Scores the board for each player given that obstacle placement.
3. Iterates to generate a list of scores.
4. Find the column with the best score by adding the scores of both players.
5. Place an obstacle there.
It should be noted that the search only looks at the board at the specific instant and does not look ahead. This was intentionally designed so that agents may win.

## Evaluation Function
The evaluation function assesses the strength of a player's position on the board. It assigns a score based on various factors, including piece placements and potential winning positions. Here's an overview of how the evaluation function works:
1. Center Columns: Scores higher for pieces placed in the center columns, as they offer more strategic opportunities.
2. Horizontal Lines: Evaluates each row for potential horizontal winning configurations.
3. Vertical Lines: Assesses each column for potential vertical winning configurations.
4. Diagonal Lines: Considers both upward and downward diagonal configurations for potential winning moves.
5. Piece Placement: Scores based on the presence of a player's own pieces and the absence of opponent pieces.
6. Block Opponent: Penalizes positions where the opponent is close to winning.
7. Spread Pieces: Encourages spreading out pieces to cover more potential winning configurations.
By considering these factors, the evaluation function provides a numerical score that reflects the strength of a player's position on the board. This score is used by the AI agents to make informed decisions during gameplay.
