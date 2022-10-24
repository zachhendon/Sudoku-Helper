import pygame
from BoardCreator import Board


pygame.init()

screen = pygame.display.set_mode((800, 600))

pygame.display.set_caption("Sudoku Board")
icon = pygame.image.load('game.png')
pygame.display.set_icon(icon)

myfont = pygame.font.SysFont('Calibri', 35)


board = Board('Grids/board1.png')
grid = board.grid

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False


    screen.fill((255, 255, 255))

    for i in range(10):
        if i % 9 == 0:
            line_width = 5
        elif i % 3 == 0:
            line_width = 3
        else:
            line_width = 1

        pygame.draw.line(screen, (0,0,0), (175 + i * 50, 75), (175 + i * 50, 450 + 75), line_width)
        pygame.draw.line(screen, (0,0,0), (175, 75 + i * 50), (450 + 175, 75 + i * 50), line_width)

    for i in range(9):
        for j in range(9):
            if grid[i][j] != None:
                value = myfont.render(str(grid[i][j]), True, (50,50,50))
                screen.blit(value, (175 + 17 + j * 50, 75 + 10 + i * 50))


    pygame.display.update()