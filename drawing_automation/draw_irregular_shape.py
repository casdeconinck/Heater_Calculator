import cv2 as cv
from drawing_automation.autoClass import Heater
from pynput import keyboard
from all_other_functions.irregular_shape_other_functions import *
import pandas


def draw_irregular(n, PATH):
    d = pandas.read_csv("../CSV_files/answers.csv")

    spacing_H = d["space_H"][n]
    spacing_W = d["space_W"][n]
    square_H = d["square_H"][n]
    square_W = d["square_W"][n]
    margin_H = d["margin_H"][n]
    margin_W = d["margin_W"][n]
    amount = d["amount_sq_H"][n]*d["amount_sq_W"][n]
    busbar_width = str(d["busbar_width"][n])
    min_finger_width = d["min_finger_width"][n]

    image = cv.imread(PATH)
    h_pix = image.shape[0]
    w_pix = image.shape[1]
    h_mm = to_mm(h_pix)
    w_mm = to_mm(w_pix)
    H = Heater(h_mm, w_mm, 10)
    matrix = get_matrix(h_pix, w_pix, image)
    matrix = matrix[~np.all(matrix == 0, axis=1)]
    matrix_rows, matrix_columns = matrix.shape

    solution = loop_trough_possibilities(amount, margin_H, margin_W, square_H, square_W, spacing_W, spacing_H, matrix,
                                         matrix_rows)
    spacing_W = solution[0]
    spacing_H = solution[1]

    with keyboard.Listener(on_press=on_press, suppress=False) as listener:
        H.open_corel()
        index = pixelate(margin_H + square_H)

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

            y_value = to_mm(h_pix-index)
            width = min(maximum) - max(minimum) - 2 * margin_W
            amount_elements = int(width/(square_W + spacing_W))
            new_margin_W = (width + - 2 * margin_W - square_W*amount_elements - spacing_W*(amount_elements-1))/2
            x_value = max(minimum) + new_margin_W + square_W

            if amount_elements > 0:
                H.draw_line_horizontal()
                H.adjust_width_of_non_lines(str(square_W))
                H.adjust_width(str(square_H))
                H.adjust_x(str(x_value))
                H.adjust_y(str(y_value))
                x_value = x_value + spacing_W + square_W
                H.go_to_transform_tab()
                H.transform_x_cor(str(square_W + spacing_W))
                H.transform_copies(str(amount_elements - 1))
                H.go_back_to_properties_tab()

            index += pixelate(spacing_H + square_H)

        cv.imshow('square', image)

        cv.waitKey(0)
    listener.join()
