import cv2
import numpy as np
import tensorflow as tf

SIZE = 100

WHITE = (255, 255, 255)
ORIGINAL_COLOR = (50, 50, 50)
CORRECT_COLOR = (0, 114, 227)
INCORRECT_COLOR = (229, 92, 108)

INCORRECT_BACKGROUND_COLOR = (247, 207, 217)
SELECTED_BACKGROUND_COLOR = (187, 222, 251)
ADJACENT_BACKGROUND_COLOR = (226, 235, 243)
SAME_VALUE_BACKGROUND_COLOR = (195, 215, 234)


def next_cell(pos, is_forward):
    i, j = pos[0], pos[1]

    if is_forward:
        if j == 8:
            i += 1
            j = 0
        else:
            j += 1

    else:
        if j == 0:
            i -= 1
            j = 8
        else:
            j -= 1

    return (i, j)


def backtrack(grid, pos):
    i, j = pos[0], pos[1]
    grid[i][j].value = None

    while True:
        i, j = next_cell((i, j), False)

        cell = grid[i][j]

        if cell.mutable == True:
            return (i, j)


def test_position(grid, pos, digit):
    i, j = pos
    nums = []

    # test rows and columns
    for n in range(9):
        row_value = grid[n][j].value
        column_value = grid[i][n].value

        if row_value != None:
            nums.append(row_value)

        if column_value != None:
            nums.append(column_value)

    # test nonets
    y_start = (i // 3) * 3
    x_start = (j // 3) * 3

    for y in range(y_start, y_start+3):
        for x in range(x_start, x_start+3):
            nonet_value = grid[y][x].value

            if nonet_value != None:
                nums.append(nonet_value)

    if digit in nums:
        return False
    return True


def solve_board(grid):

    solved = False
    i, j = 0, 0

    while solved == False:
        cell = grid[i][j]

        if cell.value == None:
            start = 1
        else:
            start = cell.value + 1

        if cell.mutable == True:
            for m in range(start, 10):
                if test_position(grid, (i, j), m) == True:
                    cell.value = m

                    if (i, j) == (8, 8):
                        solved = True
                    else:
                        i, j = next_cell((i, j), True)
                    break

            else:
                i, j = backtrack(grid, (i, j))

        else:
            if (i, j) == (8, 8):
                solved = True
            i, j = next_cell((i, j), True)

    return grid


def evaluate_model(predictions):

    # board1.png
    correct_digits = [5, 3, 7, 6, 1, 9, 5, 9, 8, 6, 8, 6,
                      3, 4, 8, 3, 1, 7, 2, 6, 6, 2, 8, 4, 1, 9, 5, 8, 7, 9]
    # board2.png
    # correct_digits = [3, 6, 5, 8, 4, 5, 2, 8, 7, 3, 1, 3, 1, 8, 9, 8, 6, 3, 5, 5, 9, 6, 1, 3, 2, 5, 7, 4, 5, 2, 6, 3]

    num_correct = 0
    n = len(predictions)

    for i in range(len(predictions)):
        if predictions[i] == correct_digits[i]:
            num_correct += 1

    print(
        f"Model scored {num_correct}/{n}({round(num_correct / n * 100)}%) correct.")


def get_grid(predictions, nonempty_positions):
    grid = []
    n = 0

    for i in range(9):
        line = []

        for j in range(9):
            if nonempty_positions[(9*i) + j]:
                number = Cell(int(predictions[n]), True)
                n += 1
            else:
                number = Cell(None, False)

            line.append(number)
        grid.append(line)

    return grid


def get_predictions(images, evaluate_model):

    model = tf.keras.models.load_model(
        'Printed Digits/PrintedDigitRecognizer.h5')

    predictions = []

    for image in images:
        image = np.array([image])

        prediction = model.predict(image, verbose=0)
        predictions.append(np.argmax(prediction))

    if evaluate_model:
        evaluate_model(predictions)

    return predictions


def get_nonempty_squares(squares):
    nonempty_squares = []
    nonempty_positions = []

    for i in range(9):
        for j in range(9):
            square = squares[(9*i) + j]

            square_img_center_mean = square[SIZE * 2 //
                                            5:SIZE*3//5, SIZE*2//5:SIZE*3//5].mean()
            if square_img_center_mean > 10:
                nonempty_squares.append(square)
                nonempty_positions.append(True)
            else:
                nonempty_positions.append(False)

    return nonempty_squares, nonempty_positions


def get_adjusted_squares(squares):
    adjusted_squares = []
    n = 0
    low, high = (SIZE // 7), (SIZE - (SIZE // 7))
    x1, x2, y1, y2 = high, low, high, low

    for square in squares:
        adjusted_square = cv2.resize(square, (SIZE, SIZE))
        adjusted_square = cv2.threshold(
            adjusted_square, 100, 255, cv2.THRESH_BINARY)[1]

        for i in range(low, high+1):
            for j in range(low, high+1):
                if adjusted_square[i, j] == 255:
                    x1, x2 = min(x1, j), max(x2, j)
                    y1, y2 = min(y1, i), max(y2, i)

        height, width = (y2 - y1), (x2 - x1)

        digit_img = adjusted_square[y1:y2, x1:x2]

        left_dim = (SIZE // 2) - (width // 2)
        right_dim = (SIZE // 2) + (width // 2)
        if width % 2 == 1:
            right_dim += 1

        top_dim = (SIZE // 2) - (height // 2)
        bottom_dim = (SIZE // 2) + (height // 2)
        if height % 2 == 1:
            bottom_dim += 1

        adjusted_square = np.zeros((SIZE, SIZE))

        adjusted_square[top_dim:bottom_dim, left_dim:right_dim] = digit_img

        adjusted_squares.append(adjusted_square)

        n += 1

    return adjusted_squares


def get_squares(board_img, w, h):
    squares = []

    for i in range(9):
        for j in range(9):
            x1 = (w // 9) * j
            x2 = (w // 9) * (j + 1)

            y1 = (h // 9) * i
            y2 = (h // 9) * (i + 1)

            square = board_img[y1:y2, x1:x2]
            squares.append(square)

    return squares

# Takes an image and returns an image of the board (everything inside the outermost square)
def get_board_square(board_img):
    board_img = cv2.cvtColor(board_img, cv2.COLOR_BGR2GRAY)

    board_img = cv2.threshold(board_img, 20, 255, cv2.THRESH_BINARY)[1]
    contours = cv2.findContours(
        board_img, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)[0]

    board_contour = max(contours, key=cv2.contourArea)
    x, y, w, h = cv2.boundingRect(board_contour)

    board_square = board_img[y:y+h, x:x+w]

    return board_square, (w, h)


class Cell():

    def __init__(self, value, is_original):
        self.value = value
        self.mutable = not is_original
        self.correct = True
        self.cell_color = WHITE

        if is_original:
            self.value_color = ORIGINAL_COLOR
        else:
            self.value_color = CORRECT_COLOR


class Board():

    # Prints out a basic representation of the grid and its values
    def print_grid(self, grid):
        grid_str = "|-----------------------------------|\n"

        for line in grid:
            grid_str += "|"

            for cell in line:
                if cell.value == None:
                    grid_str += "   |"
                else:
                    grid_str += f" {str(cell.value)} |"

            grid_str += f"\n|-----------------------------------|\n"

        print(grid_str)


    # Resets the selected_cell attribute to None
    def deselect_cell(self):
        for y in range(9):
            for x in range(9):
                cell = self.grid[y][x]

                if cell.cell_color != INCORRECT_BACKGROUND_COLOR:
                    cell.cell_color = WHITE
        self.selected_cell = None


    # Sets the selected_cell attribute to (i, j) and adjusts the cell_color of related squares accordingly
    def select_cell(self, i, j):
        i, j = int(i), int(j)

        for y in range(9):
            for x in range(9):
                cell = self.grid[y][x]

                if cell.cell_color != INCORRECT_BACKGROUND_COLOR:
                    cell.cell_color = WHITE

        self.selected_cell = (i, j)

        for i in range(9):
            for j in range(9):
                cell = self.grid[i][j]

                # Cells in the same row or column
                if i == self.selected_cell[0] or j == self.selected_cell[1]:
                    if cell.cell_color != INCORRECT_BACKGROUND_COLOR:
                        cell.cell_color = ADJACENT_BACKGROUND_COLOR

                # Cells in the same nonet
                elif (i // 3, j // 3) == (self.selected_cell[0] // 3, self.selected_cell[1] // 3):
                    if cell.cell_color != INCORRECT_BACKGROUND_COLOR:
                        cell.cell_color = ADJACENT_BACKGROUND_COLOR

                # Cells with the same value
                elif self.grid[self.selected_cell[0]][self.selected_cell[1]].value == self.grid[i][j].value and self.grid[self.selected_cell[0]][self.selected_cell[1]].value != None:
                    if cell.cell_color != INCORRECT_BACKGROUND_COLOR:
                        cell.cell_color = SAME_VALUE_BACKGROUND_COLOR


    # Evaluates the board, changing the colors of squares whether they are correct or 
    # incorrect. Returns True if the board is fully solved
    def evaluate_board(self):
        correct = True

        for i in range(9):
            for j in range(9):
                cell = self.grid[i][j]

                cell.correct = True
                cell.cell_color = WHITE
                if cell.mutable == True:
                    cell.value_color = CORRECT_COLOR
                else:
                    cell.value_color = ORIGINAL_COLOR

        for i in range(9):
            row_nums = []
            column_nums = []

            for iteration in range(2):
                for j in range(9):
                    row_cell = self.grid[i][j]
                    row_value = row_cell.value

                    column_cell = self.grid[j][i]
                    column_value = column_cell.value

                    if iteration == 0:
                        if row_value != None:
                            row_nums.append(row_value)

                        if column_value != None:
                            column_nums.append(column_value)

                    elif iteration == 1:
                        if row_nums.count(row_value) >= 2:
                            correct = False
                            row_cell.correct = False

                            if row_cell.mutable == True:
                                row_cell.value_color = INCORRECT_COLOR
                            row_cell.cell_color = INCORRECT_BACKGROUND_COLOR

                        if column_nums.count(column_value) >= 2:
                            correct = False
                            column_cell.correct = False

                            if column_cell.mutable == True:
                                column_cell.value_color = INCORRECT_COLOR
                            column_cell.cell_color = INCORRECT_BACKGROUND_COLOR

        for m in range(0, 9, 3):
            for n in range(0, 9, 3):
                nonet_nums = []

                for iteration in range(2):

                    for i in range(m, m+3):
                        for j in range(n, n+3):
                            nonet_cell = self.grid[i][j]
                            nonet_value = nonet_cell.value

                            if iteration == 0:
                                if nonet_value != None:
                                    nonet_nums.append(nonet_value)

                            elif iteration == 1:
                                if nonet_nums.count(nonet_value) >= 2:
                                    correct = False
                                    nonet_cell.correct = False

                                    if nonet_cell.mutable == True:
                                        nonet_cell.value_color = INCORRECT_COLOR
                                    nonet_cell.cell_color = INCORRECT_BACKGROUND_COLOR

        if self.selected_cell != None:
            self.select_cell(self.selected_cell[0], self.selected_cell[1])

        if not correct:
            return correct
        elif len(nonet_nums) < 9 or len(row_nums) < 9 or len(column_nums) < 9:
            return "Incomplete"
        else:
            return correct


    # Updates the value of the current square. Also re-evaluates the board determine if it is correct and updates colors accordingly
    def update_square(self, pos, digit):
        i, j = pos[0], pos[1]
        current_value = self.grid[i][j]

        if current_value.mutable:
            number = Cell(digit, False)
            self.grid[i][j] = number

        self.evaluate_board()

    def __init__(self, img):
        board_img = np.invert(img)

        board_square_img, (board_width,
                           board_height) = get_board_square(board_img)

        squares = get_squares(board_square_img, board_width, board_height)

        adjusted_squares = get_adjusted_squares(squares)

        nonempty_squares, nonempty_positions = get_nonempty_squares(
            adjusted_squares)

        predictions = get_predictions(nonempty_squares, False)

        self.grid = get_grid(predictions, nonempty_positions)

        self.solved_grid = solve_board(
            get_grid(predictions, nonempty_positions))

        self.selected_cell = None
