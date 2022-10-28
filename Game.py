import pygame
from BoardCreator import Board

pygame.init()
SELECTED_COLOR = (187,222,251)

screen = pygame.display.set_mode((800, 600))

pygame.display.set_caption("Sudoku Board")
icon = pygame.image.load('game.png')
pygame.display.set_icon(icon)

myfont = pygame.font.SysFont('Calibri', 35)


image_path = 'Grids/board1.png'

board = Board(image_path)
grid = board.grid


def initialize_board(grid):
    screen.fill((255, 255, 255))


    for i in range(9):
            for j in range(9):
                cell = grid[i][j]

                if (i, j) == board.selected_cell:
                    color = SELECTED_COLOR
                else:
                    color = cell.cell_color

                pygame.draw.rect(screen, color, pygame.Rect(175 + j * 50, 75 + i * 50, 50, 50), 0, -1)


    for i in range(10):
        if i % 9 == 0:
            line_width = 5
        elif i % 3 == 0:
            line_width = 3
        else:
            line_width = 1     

        pygame.draw.line(screen, (52,72,97), (175 + i * 50, 75), (175 + i * 50, 450 + 75), line_width)
        pygame.draw.line(screen, (52,72,97), (175, 75 + i * 50), (450 + 175, 75 + i * 50), line_width)

    
    for i in range(9):
        for j in range(9):
            cell = grid[i][j]

            if cell.value != None:
                value = myfont.render(str(cell.value), True, cell.value_color)
                screen.blit(value, (175 + 17 + j * 50, 75 + 10 + i * 50))


running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYUP and event.key == 27):
            running = False


        if event.type == pygame.MOUSEBUTTONUP:
            pos = pygame.mouse.get_pos()
            i = (pos[1] - 75) // 50
            j = (pos[0] - 175) // 50

            if i >= 0 and i <= 8 and j >= 0 and j <= 8:
                board.select_cell(i, j)


        if event.type == pygame.KEYDOWN and board.selected_cell != None:
            key = event.key

            if key >= 49 and key <= 57:
                key = int(chr(key))

                board.update_square(board.selected_cell, key)

            elif key == 8 or key == 127:
                board.update_square(board.selected_cell, None)
            
            elif key == 1073741906:
                # up
                if board.selected_cell != None:
                    if board.selected_cell[0] == 0:
                        board.select_cell(8, board.selected_cell[1])
                    else:
                        board.select_cell(board.selected_cell[0] - 1, board.selected_cell[1])
            elif key == 1073741903 or key == 9:
                # right
                if board.selected_cell != None:
                    if board.selected_cell[1] == 8:
                        board.select_cell(board.selected_cell[0], 0)
                    else:
                        board.select_cell(board.selected_cell[0], board.selected_cell[1] + 1)
            elif key == 1073741905:
                # down
                if board.selected_cell != None:
                    if board.selected_cell[0] == 8:
                        board.select_cell(0, board.selected_cell[1])
                    else:
                        board.select_cell(board.selected_cell[0] + 1, board.selected_cell[1])
            elif key == 1073741904:
                # left
                if board.selected_cell != None:
                    if board.selected_cell[1] == 0:
                        board.select_cell(board.selected_cell[0], 8)
                    else:
                        board.select_cell(board.selected_cell[0], board.selected_cell[1] - 1)
            
    initialize_board(grid)

    pygame.display.update()