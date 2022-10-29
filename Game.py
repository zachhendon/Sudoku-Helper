import pygame
from BoardCreator import Board
from PIL import ImageGrab
import numpy as np

running = True

pygame.init()
SELECTED_COLOR = (187, 222, 251)


WIDTH, HEIGHT = 800, 600

SQUARE_SIZE = min(WIDTH, HEIGHT) / 15
GRID_SIZE = SQUARE_SIZE * 9

LEFT_DISTANCE = (WIDTH - GRID_SIZE) / 10
RIGHT_DISTANCE = LEFT_DISTANCE + GRID_SIZE

TOP_DISTANCE = (HEIGHT - GRID_SIZE) * 3 / 4
BOTTOM_DISTANCE = TOP_DISTANCE + GRID_SIZE


screen = pygame.display.set_mode((WIDTH, HEIGHT))

pygame.display.set_caption("Sudoku Helper")
icon = pygame.image.load('Images/game.png')
pygame.display.set_icon(icon)

myfont = pygame.font.SysFont('Calibri', int(SQUARE_SIZE / 1.5))

# Get image from clipboard
PIL_image = ImageGrab.grabclipboard()
image = np.array(PIL_image)

if PIL_image != None:
    # Create board object
    board = Board(image)
    grid = board.grid
    solved_grid = board.solved_grid
else:
    print("Copy an image to your clipboard")
    running = False


# Solution button
SOLUTION_BUTTON_WIDTH = 6 * SQUARE_SIZE
SOLUTION_BUTTON_HEIGHT = 1.5 * SQUARE_SIZE

LEFT_SOLUTION_BUTTON_POS = (
    (WIDTH + RIGHT_DISTANCE) / 2) - (SOLUTION_BUTTON_WIDTH / 2)
RIGHT_SOLUTION_BUTTON_POS = LEFT_SOLUTION_BUTTON_POS + SOLUTION_BUTTON_WIDTH

TOP_SOLUTION_BUTTON_POS = TOP_DISTANCE + (2 * SQUARE_SIZE)
BOTTOM_SOLUTION_BUTTON_POS = TOP_SOLUTION_BUTTON_POS + SOLUTION_BUTTON_HEIGHT

# Solution grid
SOLUTION_SQUARE = SQUARE_SIZE / 2
SOLUTION_SIZE = SOLUTION_SQUARE * 9

SOLUTION_LEFT = (LEFT_SOLUTION_BUTTON_POS +
                 SOLUTION_BUTTON_WIDTH / 2) - (4.5 * SOLUTION_SQUARE)
SOLUTION_TOP = BOTTOM_SOLUTION_BUTTON_POS + (SOLUTION_SQUARE * 1.5)

show_solution_grid = False


# Helper button
HELPER_BUTTON_WIDTH = 5 * SQUARE_SIZE
HELPER_BUTTON_HEIGHT = 1.5 * SQUARE_SIZE

LEFT_HELPER_BUTTON_POS = ((WIDTH + RIGHT_DISTANCE) /
                          2) - (HELPER_BUTTON_WIDTH / 2)
RIGHT_HELPER_BUTTON_POS = LEFT_HELPER_BUTTON_POS + HELPER_BUTTON_WIDTH

TOP_HELPER_BUTTON_POS = TOP_DISTANCE - (SQUARE_SIZE / 5)
BOTTOM_HELPER_BUTTON_POS = TOP_HELPER_BUTTON_POS + HELPER_BUTTON_HEIGHT

compare_grids = False


def reset_board():
    for i in range(9):
        for j in range(9):
            if grid[i][j].mutable == True:
                board.update_square((i, j), None)


def solve_all_cells():
    for i in range(9):
        for j in range(9):
            board.update_square((i, j), solved_grid[i][j].value)


def copy_solved_value(pos):
    i, j = pos[0], pos[1]

    board.update_square(pos, solved_grid[i][j].value)


def draw_solution_buttons():
    # Button
    pygame.draw.rect(screen, (20, 20, 20), pygame.Rect(LEFT_SOLUTION_BUTTON_POS,
                     TOP_SOLUTION_BUTTON_POS, SOLUTION_BUTTON_WIDTH, SOLUTION_BUTTON_HEIGHT), 0, -1, 7, 7, 7, 7)

    # Button text
    solution_font = pygame.font.SysFont('Calibri', int(SQUARE_SIZE / 1.5))
    solution_text = solution_font.render(
        "Show Solutions", True, (230, 230, 230))
    screen.blit(solution_text, (((LEFT_SOLUTION_BUTTON_POS + (SOLUTION_BUTTON_WIDTH / 2)) - (solution_text.get_width() / 2)),
                (TOP_SOLUTION_BUTTON_POS + (SOLUTION_BUTTON_HEIGHT / 2)) - (solution_text.get_height() * 2 / 3)))

    tip_font = pygame.font.SysFont('Calibri', int(SQUARE_SIZE / 2.25))
    tip_text = tip_font.render("(Press 's' to toggle)", True, (230, 230, 230))
    screen.blit(tip_text, (((LEFT_SOLUTION_BUTTON_POS + (SOLUTION_BUTTON_WIDTH / 2)) - (tip_text.get_width() / 2)),
                (TOP_SOLUTION_BUTTON_POS + (SOLUTION_BUTTON_HEIGHT / 2)) + (solution_text.get_height() / 3)))

    # Create grid
    if show_solution_grid == True:
        # Add tip
        tip2_text = tip_font.render(
            "(Click to copy to primary board)", True, (50, 50, 50))
        screen.blit(tip2_text, (((LEFT_SOLUTION_BUTTON_POS + (SOLUTION_BUTTON_WIDTH / 2)
                                  ) - (tip2_text.get_width() / 2)), SOLUTION_TOP - SOLUTION_SQUARE))

        # Draw grid
        for i in range(10):
            if i % 9 == 0:
                line_width = 3
            elif i % 3 == 0:
                line_width = 2
            else:
                line_width = 1

            pygame.draw.line(screen, (50, 50, 50), (SOLUTION_LEFT + i * SOLUTION_SQUARE, SOLUTION_TOP),
                             (SOLUTION_LEFT + i * SOLUTION_SQUARE, SOLUTION_SIZE + SOLUTION_TOP), line_width)
            pygame.draw.line(screen, (50, 50, 50), (SOLUTION_LEFT, SOLUTION_TOP + i * SOLUTION_SQUARE),
                             (SOLUTION_SIZE + SOLUTION_LEFT, SOLUTION_TOP + i * SOLUTION_SQUARE), line_width)

        # Add numbers
        for i in range(9):
            for j in range(9):
                cell = solved_grid[i][j]

                value_font = pygame.font.SysFont(
                    'Calibri', int(SOLUTION_SQUARE / 1.5))
                value = value_font.render(
                    str(cell.value), True, cell.value_color)

                x_middle = SOLUTION_LEFT + \
                    (SOLUTION_SQUARE * j) + (SOLUTION_SQUARE * 8 / 15)
                y_middle = SOLUTION_TOP + \
                    (SOLUTION_SQUARE * i) + (SOLUTION_SQUARE * 8 / 15)

                screen.blit(value, (x_middle - value.get_width() /
                            2, y_middle - value.get_height() / 2))


def draw_helper_buttons():
    # Main text
    helper_font = pygame.font.SysFont('Calibri', int(SQUARE_SIZE / 1.25))
    helper_text = helper_font.render("Helper Mode", True, (50, 50, 50))
    screen.blit(helper_text, (((WIDTH + RIGHT_DISTANCE) / 2) -
                (helper_text.get_width() / 2), TOP_DISTANCE - (SQUARE_SIZE * 4 / 3)))

    # Tip text
    tip_font = pygame.font.SysFont('Calibri', int(SQUARE_SIZE / 2.25))
    tip_text = tip_font.render("(Press 't' to toggle)", True, (50, 50, 50))
    screen.blit(tip_text, (((WIDTH + RIGHT_DISTANCE) / 2) -
                (tip_text.get_width() / 2), TOP_DISTANCE - (SQUARE_SIZE * 2 / 3)))

    # Button
    if compare_grids == True:
        # Right side "On"
        on_color = (25, 255, 25)
        off_color = (255, 153, 153)
    else:
        # Left side "Off"
        on_color = (200, 255, 200)
        off_color = (255, 25, 25)
    pygame.draw.rect(screen, on_color, pygame.Rect(LEFT_HELPER_BUTTON_POS,
                     TOP_HELPER_BUTTON_POS, HELPER_BUTTON_WIDTH, HELPER_BUTTON_HEIGHT), 0, -1, 4, 4, 4, 4)
    pygame.draw.rect(screen, off_color, pygame.Rect(LEFT_HELPER_BUTTON_POS, TOP_HELPER_BUTTON_POS,
                     HELPER_BUTTON_WIDTH / 2, HELPER_BUTTON_HEIGHT), 0, -1, 4, 4, 4, 4)

    # Surrounding box
    pygame.draw.rect(screen, (50, 50, 50), pygame.Rect(LEFT_HELPER_BUTTON_POS,
                     TOP_HELPER_BUTTON_POS, HELPER_BUTTON_WIDTH / 2, HELPER_BUTTON_HEIGHT), 3, -1, 4, 4, 4, 4)
    pygame.draw.rect(screen, (50, 50, 50), pygame.Rect(LEFT_HELPER_BUTTON_POS,
                     TOP_HELPER_BUTTON_POS, HELPER_BUTTON_WIDTH, HELPER_BUTTON_HEIGHT), 3, -1, 4, 4, 4, 4)


def draw_title():
    title_font = pygame.font.SysFont('Calibri', int(SQUARE_SIZE))
    title_text = title_font.render("Sudoku Helper", True, (50, 50, 50))
    screen.blit(title_text, ((WIDTH / 2) -
                (title_text.get_width() / 2), SQUARE_SIZE))


def draw_values():
    for i in range(9):
        for j in range(9):
            cell = grid[i][j]

            if cell.value != None:
                value = myfont.render(str(cell.value), True, cell.value_color)

                x_middle = LEFT_DISTANCE + \
                    (SQUARE_SIZE * j) + (SQUARE_SIZE * 8 / 15)
                y_middle = TOP_DISTANCE + \
                    (SQUARE_SIZE * i) + (SQUARE_SIZE * 8 / 15)

                screen.blit(value, (x_middle - value.get_width() /
                            2, y_middle - value.get_height() / 2))


def draw_grid():
    # Tips
    tip_font = pygame.font.SysFont('Calibri', int(SQUARE_SIZE / 2))

    tip1_text = tip_font.render(
        "Press 'f' to solve the selected cell ", True, (50, 50, 50))
    tip2_text = tip_font.render(
        "Press 'a' to solve the entire board", True, (50, 50, 50))
    tip3_text = tip_font.render(
        "Press 'r' to reset the board", True, (50, 50, 50))

    screen.blit(tip1_text, (LEFT_DISTANCE, TOP_DISTANCE -
                tip1_text.get_height() * 7 / 2))
    screen.blit(tip2_text, (LEFT_DISTANCE, TOP_DISTANCE -
                tip2_text.get_height() * 5 / 2))
    screen.blit(tip3_text, (LEFT_DISTANCE, TOP_DISTANCE -
                tip2_text.get_height() * 3 / 2))

    # Grid
    for i in range(10):
        if i % 9 == 0:
            line_width = 5
        elif i % 3 == 0:
            line_width = 3
        else:
            line_width = 1

        pygame.draw.line(screen, (50, 50, 50), (LEFT_DISTANCE + i * SQUARE_SIZE, TOP_DISTANCE),
                         (LEFT_DISTANCE + i * SQUARE_SIZE, GRID_SIZE + TOP_DISTANCE), line_width)
        pygame.draw.line(screen, (50, 50, 50), (LEFT_DISTANCE, TOP_DISTANCE + i * SQUARE_SIZE),
                         (GRID_SIZE + LEFT_DISTANCE, TOP_DISTANCE + i * SQUARE_SIZE), line_width)


def draw_grid_comparisons():
    for i in range(9):
        for j in range(9):
            current_cell = grid[i][j]
            solved_cell = solved_grid[i][j]

            if current_cell.mutable == True and current_cell.value != None:
                if current_cell.value == solved_cell.value:
                    color = (0, 255, 0)
                else:
                    color = (255, 0, 0)

                pygame.draw.rect(screen, color, pygame.Rect(
                    LEFT_DISTANCE + j * SQUARE_SIZE, TOP_DISTANCE + i * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE), 0, -1)


def select_cells():
    for i in range(9):
        for j in range(9):
            cell = grid[i][j]

            if (i, j) == board.selected_cell:
                color = SELECTED_COLOR
            else:
                color = cell.cell_color

            pygame.draw.rect(screen, color, pygame.Rect(LEFT_DISTANCE + j * SQUARE_SIZE,
                             TOP_DISTANCE + i * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE), 0, -1)


def initialize_board():
    screen.fill((255, 255, 255))

    select_cells()
    if compare_grids == True:
        draw_grid_comparisons()

    draw_grid()

    draw_values()

    draw_title()
    draw_helper_buttons()
    draw_solution_buttons()


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

            elif pos[1] >= TOP_HELPER_BUTTON_POS and pos[1] <= BOTTOM_HELPER_BUTTON_POS:
                if pos[0] >= LEFT_HELPER_BUTTON_POS and pos[0] <= RIGHT_HELPER_BUTTON_POS - (HELPER_BUTTON_WIDTH / 2) and compare_grids == True:
                    compare_grids = not compare_grids
                elif pos[0] >= LEFT_HELPER_BUTTON_POS + (HELPER_BUTTON_WIDTH / 2) and pos[0] <= RIGHT_HELPER_BUTTON_POS and compare_grids == False:
                    compare_grids = not compare_grids

            elif pos[1] >= TOP_SOLUTION_BUTTON_POS and pos[1] <= BOTTOM_SOLUTION_BUTTON_POS and pos[0] >= LEFT_SOLUTION_BUTTON_POS and pos[0] <= RIGHT_SOLUTION_BUTTON_POS:
                show_solution_grid = not show_solution_grid

            else:
                board.deselect_cell()

            if pos[0] >= SOLUTION_LEFT and pos[0] <= (SOLUTION_LEFT + SOLUTION_SIZE) and pos[1] >= SOLUTION_TOP and pos[1] <= (SOLUTION_TOP + SOLUTION_SIZE) and show_solution_grid == True:
                i = int((pos[1] - SOLUTION_TOP) // SOLUTION_SQUARE)
                j = int((pos[0] - SOLUTION_LEFT) // SOLUTION_SQUARE)

                board.select_cell(i, j)
                copy_solved_value((i, j))

        if event.type == pygame.KEYDOWN:
            key = event.key

            if key == 116:
                compare_grids = not compare_grids

            elif key == 115:
                show_solution_grid = not show_solution_grid

            elif key == 97:
                solve_all_cells()

            elif key == 114:
                reset_board()

            if board.selected_cell != None:
                if key >= 49 and key <= 57:
                    key = int(chr(key))

                    board.update_square(board.selected_cell, key)

                elif key == 102:
                    copy_solved_value(board.selected_cell)

                elif key == 8 or key == 127:
                    board.update_square(board.selected_cell, None)

                elif key == 1073741906:
                    # up
                    if board.selected_cell != None:
                        if board.selected_cell[0] == 0:
                            board.select_cell(8, board.selected_cell[1])
                        else:
                            board.select_cell(
                                board.selected_cell[0] - 1, board.selected_cell[1])
                elif key == 1073741903 or key == 9:
                    # right
                    if board.selected_cell != None:
                        if board.selected_cell[1] == 8:
                            board.select_cell(board.selected_cell[0], 0)
                        else:
                            board.select_cell(
                                board.selected_cell[0], board.selected_cell[1] + 1)
                elif key == 1073741905:
                    # down
                    if board.selected_cell != None:
                        if board.selected_cell[0] == 8:
                            board.select_cell(0, board.selected_cell[1])
                        else:
                            board.select_cell(
                                board.selected_cell[0] + 1, board.selected_cell[1])
                elif key == 1073741904:
                    # left
                    if board.selected_cell != None:
                        if board.selected_cell[1] == 0:
                            board.select_cell(board.selected_cell[0], 8)
                        else:
                            board.select_cell(
                                board.selected_cell[0], board.selected_cell[1] - 1)

    initialize_board()
    pygame.display.update()
