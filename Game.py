import pygame
from BoardCreator import Board


pygame.init()
SELECTED_COLOR = (187,222,251)


WIDTH, HEIGHT = 800, 600

SQUARE_SIZE = min(WIDTH, HEIGHT) / 15
GRID_SIZE = SQUARE_SIZE * 9

LEFT_DISTANCE = (WIDTH - GRID_SIZE) / 4
RIGHT_DISTANCE = LEFT_DISTANCE + GRID_SIZE

TOP_DISTANCE = (HEIGHT - GRID_SIZE) / 2
BOTTOM_DISTANCE = TOP_DISTANCE + GRID_SIZE


screen = pygame.display.set_mode((WIDTH, HEIGHT))

pygame.display.set_caption("Sudoku Board")
icon = pygame.image.load('game.png')
pygame.display.set_icon(icon)

myfont = pygame.font.SysFont('Calibri', int(SQUARE_SIZE / 1.5))


image_path = 'Grids/board1.png'

board = Board(image_path)
grid = board.grid
solved_grid = board.solved_grid


BUTTON_WIDTH = 3 * SQUARE_SIZE
BUTTON_HEIGHT = 1 * SQUARE_SIZE

LEFT_BUTTON_POS = RIGHT_DISTANCE + SQUARE_SIZE
RIGHT_BUTTON_POS = LEFT_BUTTON_POS + BUTTON_WIDTH

TOP_BUTTON_POS = TOP_DISTANCE + (1 * SQUARE_SIZE)
BOTTOM_BUTTON_POS = TOP_BUTTON_POS + BUTTON_HEIGHT

compare_grids = False



def draw_buttons():
    if compare_grids == True:
        color = (0,255,0)
    else:
        color = (255,0,0)

    pygame.draw.rect(screen, color, pygame.Rect(LEFT_BUTTON_POS, TOP_BUTTON_POS, BUTTON_WIDTH, BUTTON_HEIGHT))

    button_text = myfont.render("BUTTON", True, (0,0,0))
    screen.blit(button_text, (LEFT_BUTTON_POS + (SQUARE_SIZE / 2.5), TOP_BUTTON_POS + (SQUARE_SIZE / 5)))


def draw_values():
    for i in range(9):
        for j in range(9):
            cell = grid[i][j]

            if cell.value != None:
                value = myfont.render(str(cell.value), True, cell.value_color)
                screen.blit(value, (LEFT_DISTANCE + (SQUARE_SIZE / 3) + j * SQUARE_SIZE, TOP_DISTANCE + (SQUARE_SIZE / 5) + i * SQUARE_SIZE))
    

def draw_grid():
    for i in range(10):
        if i % 9 == 0:
            line_width = 5
        elif i % 3 == 0:
            line_width = 3
        else:
            line_width = 1     

        pygame.draw.line(screen, (52,72,97), (LEFT_DISTANCE + i * SQUARE_SIZE, TOP_DISTANCE), (LEFT_DISTANCE + i * SQUARE_SIZE, GRID_SIZE + TOP_DISTANCE), line_width)
        pygame.draw.line(screen, (52,72,97), (LEFT_DISTANCE, TOP_DISTANCE + i * SQUARE_SIZE), (GRID_SIZE + LEFT_DISTANCE, TOP_DISTANCE + i * SQUARE_SIZE), line_width)


def draw_grid_comparisons():
    for i in range(9):
        for j in range(9):
            current_cell = grid[i][j]
            solved_cell = solved_grid[i][j]

            if current_cell.mutable == True and current_cell.value != None:
                if current_cell.value == solved_cell.value:
                    color = (0,255,0)
                else:
                    color = (255,0,0)

                pygame.draw.rect(screen, color, pygame.Rect(LEFT_DISTANCE + j * SQUARE_SIZE, TOP_DISTANCE + i * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE), 0, -1)



def select_cells():
    for i in range(9):
            for j in range(9):
                cell = grid[i][j]

                if (i, j) == board.selected_cell:
                    color = SELECTED_COLOR
                else:
                    color = cell.cell_color

                pygame.draw.rect(screen, color, pygame.Rect(LEFT_DISTANCE + j * SQUARE_SIZE, TOP_DISTANCE + i * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE), 0, -1)


def initialize_board():
    screen.fill((255, 255, 255))

    select_cells()
    if compare_grids == True:
        draw_grid_comparisons()
    
    draw_grid()
   
    draw_values()
    
    draw_buttons()



running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYUP and event.key == 27):
            running = False


        if event.type == pygame.MOUSEBUTTONUP:
            pos = pygame.mouse.get_pos()
            i = (pos[1] - TOP_DISTANCE) // SQUARE_SIZE
            j = (pos[0] - LEFT_DISTANCE) // SQUARE_SIZE

            if i >= 0 and i <= 8 and j >= 0 and j <= 8:
                board.select_cell(i, j)

            elif pos[1] >= TOP_BUTTON_POS and pos[1] <= BOTTOM_BUTTON_POS and pos[0] >= LEFT_BUTTON_POS and pos[0] <= RIGHT_BUTTON_POS:
                compare_grids = not compare_grids
            else:
                board.deselect_cell()



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


    initialize_board()
    pygame.display.update()