import pygame
from Minesweeper_Gen_Partial import *

# Constants
CELL_SIZE = 40  # Kích thước ô
GRID_SIZE = (9, 9)  # Kích thước bảng
WIDTH, HEIGHT = GRID_SIZE[0] * CELL_SIZE * 2 + 20, GRID_SIZE[1] * CELL_SIZE  # Nhân đôi chiều rộng

# Màu sắc
HIDDEN_COLOR = (150, 150, 150)  # Xám
FLAG_COLOR = (200, 50, 50)  # Đỏ
BOMB_COLOR = (0, 0, 0)  # Đen
OPEN_COLOR = (255, 255, 255)  # Trắng
LINE_COLOR = (0, 0, 0)  # Đen

# Khởi tạo Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Minesweeper Visualizer")
font = pygame.font.Font(None, 30)

game = Minesweeper_Partial()
grid = game.transform_partial()

solved_grid = game.board

def draw_grid(grid, offset_x):
    for y in range(GRID_SIZE[1]):
        for x in range(GRID_SIZE[0]):
            value = grid[y, x]
            rect = pygame.Rect(x * CELL_SIZE + offset_x, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            
            if value == -0.5:
                pygame.draw.rect(screen, HIDDEN_COLOR, rect)
            elif value == -1:
                pygame.draw.rect(screen, FLAG_COLOR, rect)
            elif value == -2:
                pygame.draw.rect(screen, BOMB_COLOR, rect)
            else:
                pygame.draw.rect(screen, OPEN_COLOR, rect)
                if value > 0:
                    text = font.render(str(int(value)), True, (0, 0, 0))
                    screen.blit(text, (x * CELL_SIZE + 12 + offset_x, y * CELL_SIZE + 8))
            
            pygame.draw.rect(screen, LINE_COLOR, rect, 1)

def main():
    running = True
    game.cell_ratio(board=grid)
    while running:
        screen.fill((255, 255, 255))
        draw_grid(grid, 0)  # Vẽ bảng hiện tại
        draw_grid(solved_grid, GRID_SIZE[0] * CELL_SIZE + 20)  # Vẽ bảng đã giải
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
    pygame.quit()

if __name__ == "__main__":
    main()

