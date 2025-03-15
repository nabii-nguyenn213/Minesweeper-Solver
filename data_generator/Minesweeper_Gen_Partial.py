# from Minesweeper_Gen_Board import Minesweeper_Board
from .Minesweeper_Gen_Board import Minesweeper_Board
import numpy as np
import random

### Define Constants

MINE_CELL = -2
HIDDEN_CELL = -0.5
FLAG_CELL = -1

class Minesweeper_Partial(Minesweeper_Board):
    def __init__(self, rows=9, cols=9, num_mines=10):
        super().__init__(rows, cols, num_mines)
        self.board = self.generate_new_board()
        self.dug = []
        self.flag = []
        
    def cell_ratio(self, board):
        num_cells = np.sum((board >= 0) & (board <= 8))  
        hidden_cells = np.sum(board == HIDDEN_CELL)  
        flag_cells = np.sum(board == FLAG_CELL)  

        total_cells = board.size
        return num_cells / total_cells, hidden_cells / total_cells, flag_cells / total_cells

    def find_largest_zero_cluster(self):
        size = self.board.shape[0]
        visited = np.zeros((size, size), dtype=bool)
        largest_cluster = set()
        
        def bfs(start_x, start_y):
            queue = [(start_x, start_y)]
            cluster = set()
            while queue:
                x, y = queue.pop(0)
                if visited[x, y]:
                    continue
                visited[x, y] = True
                cluster.add((x, y))  
                if self.board[x, y] == 0:  
                    for dx in [-1, 0, 1]:
                        for dy in [-1, 0, 1]:
                            nx, ny = x + dx, y + dy
                            if 0 <= nx < size and 0 <= ny < size and not visited[nx, ny]:
                                queue.append((nx, ny))
            return cluster
        
        for i in range(size):
            for j in range(size):
                if self.board[i, j] == 0 and not visited[i, j]:
                    cluster = bfs(i, j)
                    if len(cluster) > len(largest_cluster):
                        largest_cluster = cluster
        for i in largest_cluster:
            if self.board[i[0], i[1]] == 0:
                return i
    
    def dig(self, current_row, current_col):
        self.dug.append((current_row, current_col))       
        if self.board[current_row, current_col] == MINE_CELL:
            # ! dig a bomb
            return False 
        elif self.board[current_row, current_col] > 0: 
            # ! dig a number > 0
            return True         
        for r in range(max(0, current_row - 1), min(self.rows - 1, current_row + 1) + 1):
            for c in range(max(0, current_col - 1), min(self.cols - 1, current_col + 1) + 1):
                if (r, c) in self.dug:
                    continue
                self.dig(r, c)               
        return True
    
    def attach_flags(self, board):
        for row in range(self.rows):
            for col in range(self.cols):
                num_hidden = 0
                num_revealed = 0
                num_flags_around = 0
                if board[row, col] <= 0:
                    continue
                for r in range(max(0, row - 1), min(self.rows - 1, row + 1) + 1):
                    for c in range(max(0, col - 1), min(self.cols - 1, col + 1) + 1):
                        if r == row and c == col:
                            continue
                        if board[r, c] == HIDDEN_CELL:
                            num_hidden += 1
                        elif board[r, c] == FLAG_CELL:
                            num_flags_around += 1
                        elif board[r, c] >= 0:
                            num_revealed += 1                
                if num_hidden + num_flags_around == board[row, col]:
                    for r in range(max(0, row - 1), min(self.rows - 1, row + 1) + 1):
                        for c in range(max(0, col - 1), min(self.cols - 1, col + 1) + 1):
                            if r == row and c == col: 
                                continue
                            if board[r, c] == HIDDEN_CELL:
                                self.flag.append((r, c))
                                board[r, c] = FLAG_CELL             
        return board

    def transform_partial(self):
        
        coor = self.find_largest_zero_cluster()
        self.dig(coor[0], coor[1])
        
        partial_board = np.full((self.rows, self.cols), HIDDEN_CELL)
        for i in range(self.rows):
            for j in range(self.cols):
                if (i, j) in self.dug:
                    partial_board[i, j] = self.board[i, j]
        partial_board = self.attach_flags(partial_board)
        return partial_board
    
    def get_label(self):
        return np.where(self.board == MINE_CELL, 1, 0).reshape(-1, 1)

        
        
if __name__ == "__main__":
    game = Minesweeper_Partial()
    print(game.board)
    print()
    partial_board = game.transform_partial()
    print(partial_board)
    print()
    game.cell_ratio(partial_board)
    print()