import cv2
import numpy as np
import tensorflow as tf

SIZE = 100


class Number():

    def __init__(self, value, is_original):
        self.value = value
        self.mutable = not is_original


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
                number = Number(int(predictions[n]), True)
                n += 1
            else:
                number
                number = Number(None, False)

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
        cv2.imwrite(f"Images/{n}.png", digit_img)

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


def get_board_square(board_img):
    board_img = cv2.cvtColor(board_img, cv2.COLOR_BGR2GRAY)

    board_img = cv2.threshold(board_img, 20, 255, cv2.THRESH_BINARY)[1]
    contours = cv2.findContours(
        board_img, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)[0]

    board_contour = max(contours, key=cv2.contourArea)
    x, y, w, h = cv2.boundingRect(board_contour)

    board_square = board_img[y:y+h, x:x+w]

    return board_square, (w, h)


class Board():

    def __str__(self):
        grid_str = "|-----------------------------------|\n"

        for line in self.grid:
            grid_str += "|"

            for square in line:
                if square == None:
                    grid_str += "   |"
                else:
                    grid_str += f" {str(square)} |"

            grid_str += f"\n|-----------------------------------|\n"

        return grid_str

    def evaluate_board(self):
        for i in range(9):
            row_nums = []
            column_nums = []

            for j in range(9):
                row_value = self.grid[i][j].value

                if row_value != None:
                    if row_value not in row_nums:
                        row_nums.append(row_value)
                    else:
                        return "Row error"

                column_value = self.grid[j][i]
                
                if column_value != None:
                    if column_value not in column_nums:
                        column_nums.append(column_value)
                    else:
                        return "Column Error"


        for m in range(0, 9, 3):
            for n in range(0, 9, 3):
                nonet_nums = []

                for i in range(m, m+3):
                    for j in range(n, n+3):
                        nonet_value = self.grid[i][j].value

                        if nonet_value != None:
                            if nonet_value not in nonet_nums:
                                nonet_nums.append(nonet_value)
                            else:
                                return "Nonet Error"
                                

        if len(nonet_nums) < 9 or len(row_nums) < 9 or len(column_nums) < 9:
            return "Incomplete"


        return "SUCCESS"

    def update_square(self, pos, digit):
        i, j = pos[0], pos[1]
        current_value = self.grid[i][j]

        if current_value.mutable:
            number = Number(digit, False)
            self.grid[i][j] = number

        print(self.evaluate_board())

    def __init__(self, img_path):
        board_img = cv2.imread(img_path)
        board_img = np.invert(board_img)

        board_square_img, (board_width,
                           board_height) = get_board_square(board_img)

        squares = get_squares(board_square_img, board_width, board_height)

        adjusted_squares = get_adjusted_squares(squares)

        nonempty_squares, nonempty_positions = get_nonempty_squares(
            adjusted_squares)

        predictions = get_predictions(nonempty_squares, False)

        self.grid = get_grid(predictions, nonempty_positions)
