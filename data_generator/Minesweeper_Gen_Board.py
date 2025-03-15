import numpy as np
import random # for generate mines 
### Define Constants

MINE_CELL = -2
HIDDEN_CELL = -0.5
FLAG_CELL = -1

class Minesweeper_Board:
	def __init__(self, rows=9, cols=9, num_mines=10):
		self.rows = rows
		self.cols = cols
		self.num_mines = num_mines

	def make_board(self):
		return np.full((self.rows, self.cols), HIDDEN_CELL)

	def generate_mines(self, board):
		self.mine_coordinate = []
		number_of_mines = 0

		while number_of_mines < self.num_mines:
			mine_row, mine_col = (random.randint(0, self.rows-1), random.randint(0, self.cols-1))
			if (mine_row, mine_col) not in self.mine_coordinate:
				self.mine_coordinate.append((mine_row, mine_col))
				number_of_mines += 1
				board[mine_row, mine_col] = MINE_CELL
		return board

	def assign_number(self, board):
		for r in range(self.rows):
			for c in range(self.cols):
					if board[r, c] == MINE_CELL:
						continue
					else:
						board[r, c] = self.neighbor_mines(r, c, board)
		return board

	def neighbor_mines(self, row, col, board):
		neighbors = 0
		for r in range(max(0, row-1), min(self.rows-1, row+1)+1):
			for c in range(max(0, col-1), min(self.cols-1, col+1)+1):
				if board[r, c] == MINE_CELL:
					neighbors += 1
		return neighbors

	def generate_new_board(self):
		board = self.make_board()
		board = self.generate_mines(board)
		board = self.assign_number(board)
		return board

if __name__ == "__main__":
    game = Minesweeper_Board()
    board = game.generate_new_board()
    print(board)
    