import pygame
from BoardCreator import Board

pygame.init()

screen = pygame.display.set_mode((800, 600))

pygame.display.set_caption("Sudoku Board")
icon = pygame.image.load('game.png')
pygame.display.set_icon(icon)

myfont = pygame.font.SysFont('Calibri', 35)


image_path = 'Grids/board1.png'

board = Board(image_path)
grid = board.grid


selected_box = None


def initialize_board(grid):
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
            number = grid[i][j]
            if number.value != None:
                if number.mutable == False:
                    color = (50,50,50)
                else:
                    color = (140,151,200)
                value = myfont.render(str(number.value), True, color)
                screen.blit(value, (175 + 17 + j * 50, 75 + 10 + i * 50))


def select_box(pos):
    i, j = pos[0], pos[1]
    pygame.draw.rect(screen, (25, 25, 25), pygame.Rect(175 + j * 50, 75 + i * 50, 51, 51), 2)



running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False


        if event.type == pygame.MOUSEBUTTONUP:
            pos = pygame.mouse.get_pos()
            i = (pos[1] - 75) // 50
            j = (pos[0] - 175) // 50

            if i >= 0 and i <= 8 and j >= 0 and j <= 8:
                select_box((i, j))
                selected_box = (i, j)


        if event.type == pygame.KEYUP:
            key = chr(event.key)

            if key.isnumeric() and selected_box != None:
                key = int(key)

                if key >= 1 and key <= 9:
                    board.update_square(selected_box, key)
            
    initialize_board(grid)
    if selected_box != None:
        select_box(selected_box)



    pygame.display.update()