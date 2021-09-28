import numpy as np
import math
import os
from pynput.keyboard import Key


def pixelate(number):
    """converts a given number of mm to the equivalent amount of pixels"""
    return round(number * math.sqrt(830 * 830 / (70 * 70)))


def to_mm(pixels):
    """converts a given number of pixels to the equivalent amount of mm"""
    return pixels * math.sqrt((70 * 70) / (830 * 830))


def get_matrix(h_pix, w_pix, image):
    """gives the matrix where the image is not white. Rows represent the y-index and columns the x-index.
    All white pixels will show zero in the matrix"""
    y = 0
    x = 0
    y_index = 0
    x_index = 0
    matrix = np.zeros((int(h_pix), int(w_pix)))
    start = False
    while y < h_pix:
        while x < w_pix:
            if image[y, x].tolist() != [255, 255, 255]:
                matrix[y_index][x_index] = x
                x_index += 1
                start = True
            x += 1
        x = 0
        x_index = 0
        if start:
            y_index += 1
        y += 1
    return matrix


def on_press(key):
    """responsible for exiting the automation"""
    if key == Key.space:
        os._exit(0)


def calculate_amount_of_elements(margin_H, margin_W, square_H, square_W, spacing_W, spacing_H, matrix, matrix_rows):
    """Will calculate the amount of elements that fit into an irregular shape, with its characteristic matrix
    given and aal other parameters."""
    index = pixelate(margin_H + square_H)
    all_elements = 0
    all_rows = 0

    while index + pixelate(square_H) < matrix_rows:
        top = index - pixelate(square_H)
        bottom = index + pixelate(square_H)
        row_top = matrix[top]
        row_mid = matrix[index]
        row_bottom = matrix[bottom]
        minimum = [to_mm(np.min(row_top[np.nonzero(row_top)])),
                   to_mm(np.min(row_mid[np.nonzero(row_mid)])),
                   to_mm(np.min(row_bottom[np.nonzero(row_bottom)]))]
        maximum = [to_mm(np.max(row_top[np.nonzero(row_top)])),
                   to_mm(np.max(row_mid[np.nonzero(row_mid)])),
                   to_mm(np.max(row_bottom[np.nonzero(row_bottom)]))]

        width = min(maximum) - max(minimum) - 2 * margin_W
        all_elements += int(width / (square_W + spacing_W))
        all_rows += 1
        index += int(pixelate(spacing_H + square_H))

    return [all_elements, all_rows]


def loop_trough_possibilities(amount, margin_H, margin_W, square_H, square_W, spacing_W, spacing_H, matrix, matrix_rows,
                              i=0, prev=0):
    """This function will call itself again and again until the outcome of the function 'calculate_amount_of_elements'
    is equal to the wanted 'amount'. This by changing margin or spacing every time it gets called"""
    elements = calculate_amount_of_elements(margin_H, margin_W, square_H, square_W, spacing_W, spacing_H, matrix,
                                            matrix_rows)
    initial_amount = elements[0]
    if amount-1 <= initial_amount <= amount+1:
        solutions_list = [float(spacing_W), float(spacing_H), elements[1]]
        return solutions_list
    elif initial_amount > amount:
        if i % 2 == 0:
            if prev == 1:
                return loop_trough_possibilities(amount, margin_H, margin_W + 0.1, square_H, square_W, spacing_W,
                                                 spacing_H, matrix, matrix_rows, i + 1, 1)
            else:
                return loop_trough_possibilities(amount, margin_H, margin_W, square_H, square_W, spacing_W+0.1,
                                                 spacing_H, matrix, matrix_rows, i+1, 1)
        else:
            if prev == 1:
                return loop_trough_possibilities(amount, margin_H + 0.1, margin_W, square_H, square_W, spacing_W,
                                                 spacing_H, matrix, matrix_rows, i + 1, 1)
            else:
                return loop_trough_possibilities(amount, margin_H, margin_W, square_H, square_W, spacing_W,
                                                 spacing_H+0.1, matrix, matrix_rows, i+1, 1)
    elif initial_amount < amount:
        if i % 2 == 0:
            if prev == 1:
                return loop_trough_possibilities(amount, margin_H, margin_W - 0.1, square_H, square_W, spacing_W,
                                                 spacing_H, matrix, matrix_rows, i + 1, 2)
            else:
                return loop_trough_possibilities(amount, margin_H, margin_W, square_H, square_W, spacing_W-0.1,
                                                 spacing_H, matrix, matrix_rows, i+1, 2)
        else:
            if prev == 1:
                return loop_trough_possibilities(amount, margin_H - 0.1, margin_W, square_H, square_W, spacing_W,
                                                 spacing_H, matrix, matrix_rows, i + 1, 2)
            else:
                return loop_trough_possibilities(amount, margin_H, margin_W, square_H, square_W, spacing_W,
                                                 spacing_H-0.1, matrix, matrix_rows, i+1, 2)


def get_area(matrix, matrix_rows):
    """This function approximates the area of an irregular shape by putting in small squares of 0,5*0,5 mm.
    It will then return an approximated area (mm²) and a dimension of a square with this same area"""
    a = calculate_amount_of_elements(0.4, 0.4, 0.5, 0.5, 0, 0, matrix, matrix_rows)[0]
    area = a * 0.5 * 0.5
    return [area, math.sqrt(area)]
