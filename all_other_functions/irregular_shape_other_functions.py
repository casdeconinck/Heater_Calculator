import numpy as np
import math
import os
import tkinter as t
from pynput.keyboard import Key
from all_other_functions.front_end import Input
import time


def output_of_no_options(go, solution, option, sq_w, sq_h, space_w, space_h, marg_w, marg_h):
    if go:
        option.solution = solution
    else:
        option.amount = (option.amount/(option.square_H/option.square_W))*(sq_h/sq_w)
        option.margin_H = marg_h
        option.margin_W = marg_w
        option.square_W = sq_w
        option.square_H = sq_h
        option.spacing_W = space_w
        option.spacing_H = space_h
        option.i = 0
        option.prev = False
        option.list_of_previous = None
        option.iterations = 0
        option.no_options = 0
    print("hello ")
    option.pop_up_closed = True


def pop_up_function(initial_amount, solution, option, window_to_close):

    popup = t.Tk()
    popup.minsize(width=400, height=200)
    popup.wm_title("Your chosen settings")

    label1 = t.Label(popup, text=f"you currently have {initial_amount} elements, you need {option.amount} for "
                                 f"an aspect ratio"
                                 f" of {round(option.square_H/option.square_W, 2)}")
    label1.grid(row=0, column=0, columnspan=3)

    B1 = t.Button(popup, text="Draw with above settings", command=lambda: [output_of_no_options(
        True, solution, option, 0, 0, 0, 0, 0, 0), popup.destroy(), window_to_close.destroy()
    ])
    B1.grid(row=1, column=1)

    sq_w = Input(f"square_W from {round(option.square_W, 2)} to:", 0, 2, popup)
    sq_h = Input(f"square_W from {round(option.square_H, 2)} to:", 0, 3, popup)
    space_w = Input(f"square_W from {round(option.spacing_W, 2)} to:", 0, 4, popup)
    space_h = Input(f"square_W from {round(option.spacing_H, 2)} to:", 0, 5, popup)
    marg_w = Input(f"square_W from {round(option.margin_W, 2)} to:", 0, 6, popup)
    marg_h = Input(f"square_W from {round(option.margin_H, 2)} to:", 0, 7, popup)

    B2 = t.Button(popup, text="Draw with above settings", command=lambda:
                  [output_of_no_options(
                      False, solution, option, sq_w.get_input(), sq_h.get_input(), space_w.get_input(),
                      space_h.get_input(), marg_w.get_input(), marg_h.get_input()), popup.destroy(), window_to_close.destroy()])
    B2.grid(row=8, column=1)

    popup.mainloop()


def pixelate(number):
    """converts a given number of mm to the equivalent amount of pixels"""
    return int(round(number * math.sqrt(830 * 830 / (70 * 70))))


def to_mm(pixels):
    """converts a given number of pixels to the equivalent amount of mm"""
    return pixels * math.sqrt((70 * 70) / (830 * 830))


def get_matrix(h_pix, w_pix, image):
    """gives the matrix where the image is not white. Rows represent the y-index and columns the x-index.
    All white pixels will show zero in the matrix"""
    y = 0
    x = 0
    matrix = np.zeros((int(h_pix), int(w_pix)))
    while y < h_pix:
        while x < w_pix:
            if image[y, x].tolist() != [255, 255, 255]:
                matrix[y][x] = x
            x += 1
        x = 0
        y += 1
    return matrix


def on_press(key):
    """responsible for exiting the automation"""
    if key == Key.space:
        os._exit(0)


def calculate_amount_of_elements(margin_H, margin_W, square_H, square_W, spacing_W, spacing_H, busbar_width,
                                 min_finger_width, matrix, matrix_rows, full_output=False):
    """Will calculate the amount of elements that fit into an irregular shape, with its characteristic matrix
    given and all other parameters."""
    dict_with_coord = {"square": [square_H, square_W]}
    amount_elements = 0
    height_values = []
    index_height = 0

    for i in matrix:
        if sum(i) > 0:
            height_values.append(index_height)
        index_height += 1
    height = to_mm(height_values[len(height_values)-1] - height_values[0])
    index = height_values[0] + pixelate(margin_H + square_H / 2)
    print(height)

    if busbar_width / (height / (square_H + spacing_H)) > min_finger_width:
        min_finger_width = busbar_width / (height / (square_H + spacing_H))

    while index + pixelate(square_H + margin_H + spacing_H + min_finger_width + 0.3) < matrix_rows:
        not_zero = np.where(matrix[index] > 0)[0]
        not_zero_index = not_zero[len(not_zero)-1] - pixelate(margin_W + square_W/2 + 1 + busbar_width) - 2
        x_coord = not_zero[0] + pixelate(margin_W + square_W/2 + 1 + busbar_width)
        top = index - pixelate(square_H/2 + margin_H + spacing_H + min_finger_width + 0.3)
        bottom = index + pixelate(square_H/2 + margin_H + spacing_H + min_finger_width + 0.3)
        element_possible = False

        while not element_possible and x_coord < not_zero_index:

            x_coord_left = x_coord - pixelate(square_W/2)
            x_coord_right = x_coord + pixelate(square_W / 2)
            zero_in_matrix = False
            for i in range(top, bottom+1):
                for j in matrix[i][x_coord_left - pixelate(margin_W) : x_coord_right + pixelate(margin_W)]:
                    if j == 0:
                        zero_in_matrix = True
                        break

            if not zero_in_matrix:

                if full_output:

                    if str(index) in dict_with_coord:

                        dict_with_coord[str(index)].append(x_coord)
                        x_coord += pixelate(square_W + spacing_W)

                    else:

                        dict_with_coord[str(index)] = [x_coord]
                        x_coord += pixelate(square_W + spacing_W)

                else:
                    amount_elements += 1
                    x_coord += pixelate(square_W + spacing_W)
            else:
                x_coord += 1

            if x_coord >= not_zero_index:
                element_possible = True

        index += int(pixelate(spacing_H + square_H + 2*min_finger_width + 0.6))

    # return [all_elements, all_rows]
    if full_output:
        return dict_with_coord
    else:
        return amount_elements


# def loop_trough_possibilities(amount, margin_H, margin_W, square_H, square_W, spacing_W, spacing_H,
#                               busbar_width, min_finger_width, matrix, matrix_rows, i=0, prev=False,
#                               list_of_previous=None, iterations=0, no_options=0):
def loop_trough_possibilities(option, window_to_close):
    """This function will call itself again and again until the outcome of the function 'calculate_amount_of_elements'
    is equal to the wanted 'amount'. This by changing margin or spacing every time it gets called"""
    if option.list_of_previous is None:
        option.list_of_previous = []
    initial_amount = calculate_amount_of_elements(option.margin_H, option.margin_W, option.square_H, option.square_W,
                                                  option.spacing_W, option.spacing_H, option.busbar_width,
                                                  option.min_finger_width, option.matrix, option.matrix_rows)
    option.list_of_previous.append(initial_amount)
    print(initial_amount)
    print(option.square_W)
    print(option.square_H)

    if option.iterations < 6 and round(option.amount-4) <= initial_amount <= round(option.amount + 4):
        option.iterations += 1

    if round(option.amount-1) <= initial_amount <= round(option.amount + 1):
        solutions_list = calculate_amount_of_elements(option.margin_H, option.margin_W, option.square_H,
                                                      option.square_W, option.spacing_W, option.spacing_H,
                                                      option.busbar_width, option.min_finger_width, option.matrix,
                                                      option.matrix_rows, True)
        return solutions_list
    elif option.iterations >= 6 and option.amount-4 <= initial_amount <= option.amount + 4:
        solutions_list = calculate_amount_of_elements(option.margin_H, option.margin_W, option.square_H,
                                                      option.square_W, option.spacing_W, option.spacing_H,
                                                      option.busbar_width, option.min_finger_width, option.matrix,
                                                      option.matrix_rows, True)
        print(f"the solution will be drawn with {initial_amount} of squares instead of the wanted {option.amount}")
        return solutions_list

    elif option.no_options >= 6:
        print(f"there are no more options, do you want to draw the calculator with {initial_amount} elements instead"
              f"of {option.amount} elements?")
        solutions_list = calculate_amount_of_elements(option.margin_H, option.margin_W, option.square_H,
                                                      option.square_W, option.spacing_W, option.spacing_H,
                                                      option.busbar_width, option.min_finger_width, option.matrix,
                                                      option.matrix_rows, True)
        pop_up_function(initial_amount, solutions_list, option, window_to_close)
        while not option.pop_up_closed:
            time.sleep(1)
            print(option.pop_up_closed)

        if option.solution:
            print("yes")
            return option.solution
        else:
            print(option.amount)
            return loop_trough_possibilities(option, window_to_close)

    elif initial_amount > round(option.amount):
        # adjusting W
        if option.i % 2 == 0:
            if option.prev:
                option.margin_W += 0.4
                if initial_amount > option.amount + 15 or option.list_of_previous.count(initial_amount) >= 3:
                    option.square_W *= 1.1
                    option.square_H *= 1.1
            else:
                if initial_amount > option.amount + 15:
                    option.square_W *= 1.1
                    option.square_H *= 1.1
                    option.spacing_W += 0.4
                else:
                    option.spacing_W += 0.1
                    if option.list_of_previous.count(initial_amount) >= 3:
                        option.square_W *= 1.1
                        option.square_H *= 1.1
        # adjusting H
        else:
            if option.prev:
                option.margin_H += 0.4
                if initial_amount > option.amount + 15 or option.list_of_previous.count(initial_amount) >= 3:
                    option.square_H *= 1.1
                    option.square_W *= 1.1
            else:
                if initial_amount > option.amount + 15:
                    option.square_H *= 1.1
                    option.square_W *= 1.1
                    option.spacing_H += 0.4
                else:
                    option.spacing_H += 0.1
                    if option.list_of_previous.count(initial_amount) >= 3:
                        option.square_H *= 1.1
                        option.square_W *= 1.1

        option.i += 1
        option.prev = not option.prev
        return loop_trough_possibilities(option, window_to_close)

    elif initial_amount < option.amount:
        if option.i % 2 == 0:
            if option.prev:
                if initial_amount < option.amount - 15 and option.square_W >= 0.45:
                    option.margin_W = 0.5
                    option.square_W *= 0.9
                    option.square_H *= 0.9
                elif option.margin_W >= 0.9:
                    option.margin_W -= 0.4
                    if option.list_of_previous.count(initial_amount) >= 3 and option.square_W >= 0.45:
                        option.square_W *= 0.9
                        option.square_H *= 0.9
                else:
                    option.margin_W = 0.5
                    print("no more options")
                    option.no_options += 1

            else:
                if initial_amount < option.amount - 15 and option.square_W >= 0.45:
                    option.square_W *= 0.9
                    option.square_H *= 0.9
                    option.spacing_W = 0.4
                elif option.spacing_W >= 0.5:
                    option.spacing_W -= 0.1
                    if option.list_of_previous.count(initial_amount) >= 3 and option.square_W >= 0.45:
                        option.square_W *= 0.9
                        option.square_H *= 0.9
                else:
                    print("no more options")
                    option.no_options += 1
        else:
            if option.prev:
                if initial_amount < option.amount - 15 and option.square_H >= 0.45:
                    option.margin_H = 0.5
                    option.square_H *= 0.9
                    option.square_W *= 0.9
                elif option.margin_H >= 0.9:
                    option.margin_H -= 0.4
                    if option.list_of_previous.count(initial_amount) >= 3 and option.square_H >= 0.45:
                        option.square_H *= 0.9
                        option.square_W *= 0.9
                else:
                    option.margin_H = 0.5
                    print("no more options")
                    option.no_options += 1
            else:
                if initial_amount < option.amount - 15 and option.square_H >= 0.45:
                    option.square_H *= 0.9
                    option.square_W *= 0.9
                    option.spacing_H = 0.4
                elif option.spacing_H >= 0.5:
                    option.spacing_H -= 0.1
                    if option.list_of_previous.count(initial_amount) >= 3 and option.square_H >= 0.45:
                        option.square_H *= 0.9
                        option.square_W *= 0.9
                else:
                    print("no more options")
                    option.no_options += 1

        option.i += 1
        option.prev = not option.prev
        return loop_trough_possibilities(option, window_to_close)


def get_area(matrix, busbar_width, min_finger_width):
    """This function approximates the area of an irregular shape by putting in small squares of 0,5*0,5 mm.
    It will then return an approximated area (mm²) and a dimension of a square with this same area"""
    matrix_rows, matrix_columns = matrix.shape
    a = calculate_amount_of_elements(0.5, 0.5, 1, 1, 0.4, 0.4, busbar_width, min_finger_width, matrix, matrix_rows)
    area = a * (1+min_finger_width+0.6)**2
    print(area)
    return math.sqrt(area)
