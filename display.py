import numpy as np 
import pygame
from data_generator.Minesweeper_Gen_Partial import Minesweeper_Partial
from data_generator.processing import extract_feature
import joblib
from models.heuristic import Heuristic

#constant
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BG_COLOR = 'gray60'
LINE_COLOR = 'gray90'
REVEAL_CELL_BG = 'gray80'
SAFE_COLOR = (0, 255, 0) # green
MINE_COLOR = (255, 0, 0) # red

MINE_VAL = -2
FLAG_VAL = -1
HIDDEN_VAL = -0.5
BORDER_VAL = -10

class PygameInterface:
    
    def __init__(self):
        self.init()
        self.game = Minesweeper_Partial()
        self.board = self.game.board
        self.size_board = self.board.shape[0]

        self.revealed_coor = []
        self.flag_coor = []
        
        self.cell_size = 65
        self.border = 65
        # model
        
        self.mlp_model = joblib.load('D:/Dev/Project/AI/THE_FINAL_MINESWEEPER/models/mlp_model.pkl')
        self.dt_model = joblib.load('D:/Dev/Project/AI/THE_FINAL_MINESWEEPER/models/dt_model.pkl')
        
    
    def init(self):
        pygame.init()
        win_size = (1000, 700)
        self.window = pygame.display.set_mode(win_size)
        self.window.fill(BG_COLOR)
        pygame.display.set_caption("Minesweeper Solver")
    
    def draw_grid(self):
        for r in range(self.size_board+1):
            pygame.draw.line(self.window, LINE_COLOR, (r * self.cell_size + self.border, self.border), (r * self.cell_size + self.border, self.size_board * self.cell_size + self.border), width=5)
            pygame.draw.line(self.window, LINE_COLOR, (self.border, r * self.cell_size + self.border), (self.size_board * self.cell_size + self.border, r * self.cell_size + self.border), width=5)
    
    def reveal_cell(self):
        # TODO : This function will reveal the cell was picked. Reveal all cell 
        # TODO : Reveal all the cell that in self.revealed_coor
        font = pygame.font.SysFont(None, 36)
        for r, c in self.revealed_coor:
            # ! draw a square 
            if self.board[r, c] == 0:
                pygame.draw.rect(self.window, REVEAL_CELL_BG, ((self.border + self.cell_size * c), (self.border + self.cell_size * r), self.cell_size, self.cell_size))
            else:
                pygame.draw.rect(self.window, REVEAL_CELL_BG, ((self.border + self.cell_size * c), (self.border + self.cell_size * r), self.cell_size, self.cell_size))
                number = font.render(f"{int(self.board[r, c])}", True, BLACK)
                self.window.blit(number, (self.border + self.cell_size * c + self.cell_size / 2.5, self.border + self.cell_size * r + self.cell_size / 2.5))
    
    def current_cell_proba(self, current_row, current_col, current_board):
        # TODO : This function will compute the probability of the current cell if there is mine or not.
        board_features = extract_feature(current_board)
        # print(board_features.shape)
        features = board_features[current_row * self.size_board + current_col].reshape((1, 27))
        proba_mlp = self.mlp_model.predict_proba(features)
        # current_cell_proba = proba[current_row * self.size_board + current_col]    
        proba_dt = self.dt_model.predict_proba(features)
        return proba_mlp[0, 1], proba_dt[0, 1]
    
    def overall_proba(self):
        # TODO : This function will calculate the probability of all the hidden cell -> make the most optimal move.
        pass
        
    def get_current_board(self):
        current_board = np.full((self.size_board, self.size_board), HIDDEN_VAL)
        for r in range(self.size_board):
            for c in range(self.size_board):
                if (r, c) in self.revealed_coor:
                    # NOTE : numbered cell
                    current_board[r, c] = self.board[r, c]
                elif (r, c) in self.flag_coor:
                    # NOTE : flag cell
                    current_board[r, c] = FLAG_VAL
        return current_board
    
    def heuristic_solve(self, current_board):
        heuristic = Heuristic(board=current_board)
        safes = heuristic.find_safe()
        mines = heuristic.find_mine()
        return safes, mines
    
    def paint_heuristic(self, safes, mines):
        for r in range(self.size_board):
            for c in range(self.size_board):
                if (r, c) in safes:
                    pygame.draw.rect(self.window, SAFE_COLOR, ((self.border + self.cell_size * c), (self.border + self.cell_size * r), self.cell_size, self.cell_size))
                elif (r, c) in mines:
                    pygame.draw.rect(self.window, MINE_COLOR, ((self.border + self.cell_size * c), (self.border + self.cell_size * r), self.cell_size, self.cell_size))
                    
    
    def draw_proba(self, proba_mlp, proba_dt):
        # TODO : This function will draw probability of the current cell on the left of the window.
        proba_mlp = proba_mlp * 100
        proba_dt = proba_dt * 100
        font = pygame.font.SysFont('sans', 25)    
        mlp_text = font.render(f'MLPClassifier Probability : {proba_mlp:.1f} %', True, BLACK)
        pygame.draw.rect(self.window, BG_COLOR, (917, 210, 80, 30))
        dt_text = font.render(f'Random Forest Probability : {proba_dt:.1f} %', True, BLACK)
        pygame.draw.rect(self.window, BG_COLOR, (930, 410, 70, 30))
        
        self.window.blit(mlp_text, (670, 210))
        self.window.blit(dt_text, (670, 410))
    
    def flag(self, current_row, current_col):
        if (current_row, current_col) not in self.flag_coor:
            self.flag_coor.append((current_row, current_col))
            self.window.blit(self.img_flag, (self.border + self.cell_size * current_col, self.border + self.cell_size * current_row))
        else:
            pygame.draw.rect(self.window, BG_COLOR, ((self.border + self.cell_size * current_col), (self.border + self.cell_size * current_row), self.cell_size, self.cell_size))
            self.flag_coor.remove((current_row, current_col))

    def draw_button(self):
        # TODO : This function will create the new game button.
        font = pygame.font.SysFont('sans', 25)    
        clear_text = font.render('NEW GAME', True, BLACK)
        pygame.draw.rect(self.window, REVEAL_CELL_BG, (750, 600, 150, 50)) # *clear button
        self.window.blit(clear_text, (770, 610))
        
        
    def current_pos(self):
        # TODO : This function will track the current row and colunm of the pointer. 
        # ! Each cell is 65 is pixels width. with border to the left is 65 px. 
        # ! The first cell will be row = 0 and col = 0, the mouse must be in range (65 * 1 <= x, y <= 65 * 2) 
        # ! The second cell will be row = 0 and col = 1, the mouse must be in range (65 * 2 <= x <= 65 * 3) and (65 * 1 <= y <= 65 * 2)
        # ! --> The current row will be self.mouse_y // 65 - 1 and the current colunm will be self.mouse_x // 65 - 1
        current_row = self.mouse_y // self.cell_size - 1
        current_col = self.mouse_x // self.cell_size - 1
        current_row = min(self.size_board - 1, current_row)
        current_col = min(self.size_board - 1, current_col)
        return current_row, current_col
    
    def dig(self, current_row, current_col): 
        self.revealed_coor.append((current_row, current_col))
        if self.board[current_row, current_col] == MINE_VAL:
            # ! dig a bomb
            return False 
        elif self.board[current_row, current_col] > 0: 
            # ! dig a number > 0
            return True 
        
        for r in range(max(0, current_row - 1), min(self.size_board - 1, current_row + 1) + 1):
            for c in range(max(0, current_col - 1), min(self.size_board - 1, current_col + 1) + 1):
                if (r, c) in self.revealed_coor:
                    continue
                self.dig(r, c)
                
        return True
    
    def appear_mines(self):
        for r, c in self.game.mine_coordinate:
            self.window.blit(self.img_mine, (self.border + self.cell_size * c, self.border + self.cell_size * r))
            
                
    def clear_board(self):
        self.window.fill(BG_COLOR)
        self.draw_grid()
        self.revealed_coor = []
        self.game = Minesweeper_Partial()
        self.board = self.game.board      
    
    def game_over(self):
        pass
    
    def run(self):
        running = True
        self.img_flag = pygame.image.load('D:/Dev/Project/AI/THE_FINAL_MINESWEEPER/img/flag.png')
        self.img_flag = pygame.transform.scale(self.img_flag, (self.cell_size, self.cell_size))
        self.img_mine = pygame.image.load('D:/Dev/Project/AI/THE_FINAL_MINESWEEPER/img/mine.png')
        self.img_mine = pygame.transform.scale(self.img_mine, (self.cell_size, self.cell_size))
        while running:
            self.mouse_x, self.mouse_y = pygame.mouse.get_pos()
            self.draw_grid()
            self.draw_button()
            current_row, current_col = self.current_pos()
            if (self.border < self.mouse_x < self.border + self.size_board * self.cell_size) and (self.border < self.mouse_y < self.border + self.size_board * self.cell_size):
                current_board = self.get_current_board()
                safes, mines = self.heuristic_solve(current_board=current_board)
                self.paint_heuristic(safes=safes, mines=mines)
                if (current_row, current_col) not in self.revealed_coor:
                    proba_mlp, proba_dt = self.current_cell_proba(current_row, current_col, current_board)
                    print(proba_mlp, proba_dt)  
                    self.draw_proba(proba_mlp, proba_dt)
                    
            self.draw_grid()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
        
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if pygame.mouse.get_pressed()[0]:
                        # ! left button mouse click
                        if (self.border < self.mouse_x < self.border + self.size_board * self.cell_size) and (self.border < self.mouse_y < self.border + self.size_board * self.cell_size):
                            # ! press inside the board
                            # print(f"Current row : {current_row}, Current colunm : {current_col}")
                            safe = self.dig(current_row, current_col)
                            if not safe:
                                # ! if you dig a bom, lose the game.
                                # ! appear every mines, wait type a keys then quit the loop
                                waiting = True
                                while waiting:
                                    self.appear_mines()
                                    for event in pygame.event.get():
                                        if event.type == pygame.KEYDOWN:  # Any key is pressed
                                            waiting = False  # Exit loop
                                            running = False
                                            break
                                    pygame.display.flip()      
                            self.reveal_cell()

                        if (750 < self.mouse_x < 900) and (600 < self.mouse_y < 650): 
                            # ! new game button click
                            self.clear_board()
                            
                        
                    if pygame.mouse.get_pressed()[2]:
                        # ! right button mouse click
                        if (self.border < self.mouse_x < self.border + self.size_board * self.cell_size) and (self.border < self.mouse_y < self.border + self.size_board * self.cell_size):
                            if (current_row, current_col) not in self.revealed_coor:
                                self.flag(current_row, current_col)

            pygame.display.flip()
            

        
        
            
game = PygameInterface()
game.run()