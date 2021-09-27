import numpy as np
import math
import os
from pynput.keyboard import Key


def pixelate(number):
    return round(number * math.sqrt(830 * 830 / (70 * 70)))


def to_mm(pixels):
    return pixels * math.sqrt((70 * 70) / (830 * 830))


def get_matrix(h_pix, w_pix, image):
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
    if key == Key.space:
        os._exit(0)


def calculate_amount_of_elements(margin_H, margin_W, square_H, square_W, spacing_W, spacing_H, matrix, matrix_rows):
    index = pixelate(margin_H + square_H)
    all_elements = 0

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
        index += int(pixelate(spacing_H + square_H))

    return all_elements


def loop_trough_possibilities(amount, margin_H, margin_W, square_H, square_W, spacing_W, spacing_H, matrix, matrix_rows,
                              i=0, prev=0):
    initial_amount = calculate_amount_of_elements(margin_H, margin_W, square_H, square_W, spacing_W,
                                                  spacing_H, matrix, matrix_rows)
    if amount-1 <= initial_amount <= amount+1:
        solutions_list = [float(spacing_W), float(spacing_H)]
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
    a = calculate_amount_of_elements(0.4, 0.4, 0.5, 0.5, 0, 0, matrix, matrix_rows)
    area = a * 0.5 * 0.5
    return [area, math.sqrt(area)]

