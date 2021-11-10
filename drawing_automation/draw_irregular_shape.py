import cv2 as cv
from drawing_automation.autoClass import Heater
from pynput import keyboard
from all_other_functions.irregular_shape_other_functions import *
import pandas
import tkinter as t
from all_other_functions.no_options_class import NoOptions


def draw_irregular_in_corel(solution, h_mm, w_mm, min_finger_width):
    H = Heater(h_mm, w_mm, 10)
    square_W = solution["square"][1]
    square_H_calculated = solution["square"][0] + 2 * min_finger_width + 0.6
    solution.pop("square")
    with keyboard.Listener(on_press=on_press, suppress=False) as listener:
        H.open_corel()
        H.go_back_to_properties_tab()
        for i in solution:
            first_value = True
            length_row = to_mm(solution[i][len(solution[i]) - 1] - solution[i][0])
            middle_index = to_mm(solution[i][0]) + length_row/2
            H.draw_line_horizontal()
            H.adjust_width_of_non_lines(str(length_row + square_W + 1))
            H.adjust_width(str(min_finger_width))
            H.adjust_y(str(to_mm(float(i)) + (square_H_calculated - 2 * min_finger_width - 0.6)/2))
            H.adjust_x(str(middle_index - 0.5))
            H.copy_paste_previous_element()
            H.adjust_y(str(to_mm(float(i)) - (square_H_calculated - 2 * min_finger_width - 0.6)/2))
            H.adjust_x(str(middle_index + 0.5))
            for j in solution[i]:
                H.copy_paste_previous_element()
                if first_value:
                    H.adjust_width_of_non_lines(str(square_W))
                    H.adjust_width(str(square_H_calculated))
                    first_value = False
                    H.adjust_y(str(to_mm(float(i))))
                H.adjust_x(str(to_mm(j)))

    listener.join()


def draw_irregular(n, PATH, window_to_close):
    d = pandas.read_csv("././CSV_files/answers.csv")

    spacing_H = float(d["space_H"][n])
    spacing_W = float(d["space_W"][n])
    square_H_calculated = float(d["square_H"][n])
    square_W = float(d["square_W"][n])
    margin_H = float(d["margin_H"][n])
    margin_W = float(d["margin_W"][n])
    amount = float(d["amount_sq_H"][n])*float(d["amount_sq_W"][n])
    busbar_width = float(d["busbar_width"][n])
    min_finger_width = float(d["min_finger_width"][n])

    image = cv.imread(PATH)
    h_pix = image.shape[0]
    w_pix = image.shape[1]
    h_mm = to_mm(h_pix)
    w_mm = to_mm(w_pix)
    matrix = get_matrix(h_pix, w_pix, image)
    matrix = matrix[~np.all(matrix == 0, axis=1)]
    matrix_rows, matrix_columns = matrix.shape
    # solution = loop_trough_possibilities(amount, margin_H, margin_W, square_H_calculated, square_W, spacing_W,
    #                                      spacing_H, busbar_width, min_finger_width, matrix, matrix_rows)
    options = NoOptions(amount, margin_H, margin_W, square_H_calculated, square_W, spacing_W,
                        spacing_H, busbar_width, min_finger_width, matrix, matrix_rows)
    solution = loop_trough_possibilities(options, window_to_close)
    amount_of_keys = len(solution.keys()) - 1

    if busbar_width / amount_of_keys > min_finger_width:
        min_finger_width = busbar_width / amount_of_keys

    popup1 = t.Tk()
    popup1.minsize(width=400, height=200)
    popup1.wm_title("Your chosen settings")
    label = t.Label(popup1, text="do you want to continue?\n\nYou can stop the program any\n"
                                "time by pressing the space key", font=("Arial", 15))
    label.pack(side="top", fill="x", pady=10)

    B1 = t.Button(popup1, text="Continue", command=lambda: [
        popup1.destroy(), draw_irregular_in_corel(solution, h_mm, w_mm, min_finger_width)])
    B1.pack()
    popup1.mainloop()
