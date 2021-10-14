import numpy as np
import math
import os
from pynput.keyboard import Key


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

    while index + pixelate(square_H + margin_H + spacing_H) < matrix_rows:
        not_zero = np.where(matrix[index] > 0)[0]
        not_zero_index = not_zero[len(not_zero)-1] - pixelate(margin_W + square_W/2 + 1 + busbar_width)
        x_coord = not_zero[0] + pixelate(margin_W + square_W/2 + 1 + busbar_width)
        top = index - pixelate(square_H/2 + margin_H + spacing_H + min_finger_width + 0.3)
        bottom = index + pixelate(square_H/2 + margin_H + spacing_H + min_finger_width + 0.3)
        element_possible = False

        while not element_possible and x_coord < not_zero_index:

            x_coord_left = x_coord - pixelate(square_W/2)
            x_coord_right = x_coord + pixelate(square_W / 2)
            zero_in_matrix = False
            for i in range(top, bottom+1):
                for j in matrix[i][x_coord_left - pixelate(margin_W):x_coord_right + pixelate(margin_W)]:
                    if j == 0:
                        zero_in_matrix = True

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


def loop_trough_possibilities(amount, margin_H, margin_W, square_H, square_W, spacing_W, spacing_H,
                              busbar_width, min_finger_width, matrix, matrix_rows, i=0, prev=False,
                              list_of_previous=None, iterations=0, no_options=0):
    """This function will call itself again and again until the outcome of the function 'calculate_amount_of_elements'
    is equal to the wanted 'amount'. This by changing margin or spacing every time it gets called"""
    if list_of_previous is None:
        list_of_previous = []
    initial_amount = calculate_amount_of_elements(margin_H, margin_W, square_H, square_W, spacing_W, spacing_H,
                                                  busbar_width, min_finger_width, matrix, matrix_rows)
    list_of_previous.append(initial_amount)
    print(initial_amount)
    print(square_W)
    print(square_H)

    if iterations < 6 and amount-4 <= initial_amount <= amount + 4:
        iterations += 1

    if amount-1 <= initial_amount <= amount + 1:
        solutions_list = calculate_amount_of_elements(margin_H, margin_W, square_H, square_W, spacing_W, spacing_H,
                                                      busbar_width, min_finger_width, matrix, matrix_rows, True)
        return solutions_list
    elif iterations >= 6 and amount-4 <= initial_amount <= amount + 4:
        solutions_list = calculate_amount_of_elements(margin_H, margin_W, square_H, square_W, spacing_W, spacing_H,
                                                      busbar_width, min_finger_width, matrix, matrix_rows, True)
        print(f"the solution will be drawn with {initial_amount} of squares instead of the wanted {amount}")
        return solutions_list

    elif no_options >= 6:
        print(f"there are no more options, do you want to draw the calculator with {initial_amount} elements instead"
              f"of {amount} elements?")
        solutions_list = calculate_amount_of_elements(margin_H, margin_W, square_H, square_W, spacing_W, spacing_H,
                                                      busbar_width, min_finger_width, matrix, matrix_rows, True)
        return solutions_list

    elif initial_amount > amount:
        # adjusting W
        if i % 2 == 0:
            if prev:
                margin_W += 0.4
                if initial_amount > amount + 15 or list_of_previous.count(initial_amount) >= 3:
                    square_W *= 1.1
                    square_H *= 1.1
            else:
                if initial_amount > amount + 15:
                    square_W *= 1.1
                    square_H *= 1.1
                    spacing_W += 0.4
                else:
                    spacing_W += 0.1
                    if list_of_previous.count(initial_amount) >= 3:
                        square_W *= 1.1
                        square_H *= 1.1
        # adjusting H
        else:
            if prev:
                margin_H += 0.4
                if initial_amount > amount + 15 or list_of_previous.count(initial_amount) >= 3:
                    square_H *= 1.1
                    square_W *= 1.1
            else:
                if initial_amount > amount + 15:
                    square_H *= 1.1
                    square_W *= 1.1
                    spacing_H += 0.4
                else:
                    spacing_H += 0.1
                    if list_of_previous.count(initial_amount) >= 3:
                        square_H *= 1.1
                        square_W *= 1.1

        return loop_trough_possibilities(amount, margin_H, margin_W, square_H, square_W, spacing_W, spacing_H,
                                         busbar_width, min_finger_width, matrix, matrix_rows, i + 1, not prev,
                                         list_of_previous, iterations, no_options)

    elif initial_amount < amount:
        if i % 2 == 0:
            if prev:
                if initial_amount < amount - 15 and square_W >= 0.45:
                    margin_W = 0.5
                    square_W *= 0.9
                    square_H *= 0.9
                elif margin_W >= 0.9:
                    margin_W -= 0.4
                    if list_of_previous.count(initial_amount) >= 3 and square_W >= 0.45:
                        square_W *= 0.9
                        square_H *= 0.9
                else:
                    margin_W = 0.5
                    print("no more options")
                    no_options += 1

            else:
                if initial_amount < amount - 15 and square_W >= 0.45:
                    square_W *= 0.9
                    square_H *= 0.9
                    spacing_W = 0.4
                elif spacing_W >= 0.5:
                    spacing_W -= 0.1
                    if list_of_previous.count(initial_amount) >= 3 and square_W >= 0.45:
                        square_W *= 0.9
                        square_H *= 0.9
                else:
                    print("no more options")
                    no_options += 1
        else:
            if prev:
                if initial_amount < amount - 15 and square_H >= 0.45:
                    margin_H = 0.5
                    square_H *= 0.9
                    square_W *= 0.9
                elif margin_H >= 0.9:
                    margin_H -= 0.4
                    if list_of_previous.count(initial_amount) >= 3 and square_H >= 0.45:
                        square_H *= 0.9
                        square_W *= 0.9
                else:
                    margin_H = 0.5
                    print("no more options")
                    no_options += 1
            else:
                if initial_amount < amount - 15 and square_H >= 0.45:
                    square_H *= 0.9
                    square_W *= 0.9
                    spacing_H = 0.4
                elif spacing_H >= 0.5:
                    spacing_H -= 0.1
                    if list_of_previous.count(initial_amount) >= 3 and square_H >= 0.45:
                        square_H *= 0.9
                        square_W *= 0.9
                else:
                    print("no more options")
                    no_options += 1

        return loop_trough_possibilities(amount, margin_H, margin_W, square_H, square_W, spacing_W,
                                         spacing_H, busbar_width, min_finger_width, matrix, matrix_rows, i + 1,
                                         not prev, list_of_previous, iterations, no_options)


def get_area(matrix, busbar_width, min_finger_width):
    """This function approximates the area of an irregular shape by putting in small squares of 0,5*0,5 mm.
    It will then return an approximated area (mm²) and a dimension of a square with this same area"""
    matrix_rows, matrix_columns = matrix.shape
    a = calculate_amount_of_elements(0.5, 0.5, 1, 1, 0.4, 0.4, busbar_width, min_finger_width, matrix, matrix_rows)
    area = a * (1+min_finger_width+0.6)**2
    print(area)
    return math.sqrt(area)
