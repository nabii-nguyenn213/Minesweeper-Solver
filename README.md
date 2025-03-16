# Minesweeper-Solver

- Use `MLPClassifier` and `Random Forest` and `Heuristic` to solve Minesweeper.
  - The `Heuristic` is used to solve the obvious cases, usually early stages of the game when the board is mostly unrevealed cells. Not enough feature for `MLPClassifier` and `Random Forest` to predict.
  - The `MLP` and `Random Forest` is used to solve the certain cases when the `Heuristic` cannot find the obvious cases.

- Why we need `Heuristic`?
  - `Heuristic` helps solve the early stage of the game. Minesweeper; however, is a game of chance in the early game.
  - Removing the `Heuristic` leaves `MLP` and `Random Forest` with insufficient information to predict, making the **win rate** close to 0.
  - But with the help of the `Heuristic`, the **win rate** of Easy mode is approximately 90% for 100 games, over 73% for Medium mode.
 
- Run `play.py` file to let the model plays automatically on [MineSweeper Online](https://minesweeperonline.com/), set the `number_of_time_playing` in `play()` function.
- Run `display.py` file to play locally with pygame, you can see what the probability of `MLP` and `Random Forest` predict along with `Heuristic`.
