import cv2
import numpy as np
import tensorflow as tf
import math

SIZE = 100


class Board():

    def construct_grid(self, length, digits, nonempty):
        num_digit = 0
        grid = []

        for i in range(length):
            line = []

            for j in range(length):
                if nonempty[(length * i) + j]:
                    line.append(digits[num_digit])
                    num_digit += 1
                else:
                    line.append(None)
            grid.append(line)
        
        return(grid)


    def evaluate_model(self, predictions, correct):
        num_correct = 0
        n = len(predictions)

        for i in range(len(predictions)):
            if predictions[i] == correct[i]:
                num_correct += 1

        print(f"Model scored {num_correct}/{n}({round(num_correct / n * 100)}%) correct.")


    def get_grid(self, img, squares):
        num_squares = len(squares)
        length = int(math.sqrt(num_squares - 1))

        correct_digits = [3, 6, 5, 8, 4, 5, 2, 8, 7, 3, 1, 3, 1, 8, 9, 8, 6, 3, 5, 5, 9, 6, 1, 3, 2, 5, 7, 4, 5, 2, 6, 3]

        grid = []
        nonempty_squares = []
        n = 0
        

        for i in range(length):
            for j in range(length):
                index = num_squares - (i*length) - j - 1
                square_img = self.get_square_img(img, squares[index])
                h, w = square_img.shape

                square_img_center_mean = square_img[h*2//5:h*3//5, w*2//5:w*3//5].mean()
                if square_img_center_mean > 10:
                    adjusted_square_img = self.adjust_square_image(square_img)

                    nonempty_squares.append(True)
                    grid.append(np.array([adjusted_square_img]))

                    n += 1
                else:
                    nonempty_squares.append(False)


        predictions = self.predict_digit(grid)
        
        self.evaluate_model(predictions, correct_digits)

        grid = self.construct_grid(length, predictions, nonempty_squares)

        return grid
    
    def predict_digit(self, imgs):
        
        model = tf.keras.models.load_model('Printed Digits/PrintedDigitRecognizer.h5')

        guesses = []

        for image in imgs:
            prediction = model.predict(image, verbose=0)
            guess = np.argmax(prediction)
            guesses.append(guess)

        return guesses


    def adjust_square_image(self, square_image):
        CROPPED_SIZE = 80
        top, bottom, left, right = CROPPED_SIZE, 0, CROPPED_SIZE, 0
    
        square_image_adjusted = cv2.resize(square_image, (100, 100))
        square_image_adjusted = square_image_adjusted[10:90, 10:90]
        square_image_adjusted = cv2.threshold(square_image_adjusted, 100, 255, cv2.THRESH_BINARY)[1]

        for r in range(CROPPED_SIZE):
            for c in range(CROPPED_SIZE):
                if square_image_adjusted[r, c] > 100:
                    top = min(top, r)
                    bottom = max(bottom, r)
                    left = min(left, c)
                    right = max(right, c)

        height, width = bottom - top, right - left

        square_image_adjusted = square_image_adjusted[top:bottom, left:right]


        left_dim = (SIZE // 2) - (width // 2)
        right_dim = (SIZE // 2) + (width // 2)
        if width % 2 == 1:
            right_dim += 1

        top_dim = (SIZE // 2) - (height // 2)
        bottom_dim = (SIZE // 2) + (height // 2)
        if height % 2 == 1:
            bottom_dim += 1

        adjusted_digit_img = np.zeros((SIZE, SIZE))
        
        adjusted_digit_img[top_dim:bottom_dim, left_dim:right_dim] = square_image_adjusted

        return adjusted_digit_img

    
    def get_square_img(self, board_img, contour):
        yMax, yMin = contour[:,0,0].max(), contour[:,0,0].min()
        xMax, xMin = contour[:,0,1].max(), contour[:,0,1].min()
        
        return board_img[xMin:xMax, yMin:yMax][:,:,0]

    def get_squares(img, contours):
        squares = []
        for i in range(len(contours)):
            contour = contours[i]
            approx = cv2.approxPolyDP(contour, 0.015*cv2.arcLength(contour, True), True)
            if len(approx) == 4:
                squares.append(contour)
        
        return squares

        

    def get_contours(self, board_img):
        board_img = cv2.cvtColor(board_img, cv2.COLOR_BGR2GRAY)

        board_img = cv2.threshold(board_img, 20, 255, cv2.THRESH_BINARY)[1]
        contours = cv2.findContours(board_img, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)[0]

        return contours
    
    def __init__(self, board_img):
        board_img = cv2.imread('Grids/board2.png')
        board_img = np.invert(board_img)

        contours = self.get_contours(board_img)

        squares = self.get_squares(contours)
        print(len(squares))

        cv2.imwrite('img.png', self.get_square_img(board_img, squares[81]))

        self.grid = self.get_grid(board_img, squares)    
Board('test')
