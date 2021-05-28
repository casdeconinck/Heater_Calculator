import math
import numpy as np


def amount_of_squares(p, v, busbar_sheet_r, ptc_sheet_r, coat):
    watt_density = 0.2
    # in W/cm2

    r = v ** 2 / p
    i = v / r

    busbar_width = math.sqrt((busbar_sheet_r * 25 / coat) * i ** 2 / watt_density)
    # in cm
    squares = (ptc_sheet_r * 25 / coat) / r
    print(squares)

    return [busbar_width, squares]


def calculate(h, w, p, v, busbar_sheet_r, ptc_sheet_r, coat):

    solutions = {}
    sol = 0
    # calculate the amount of FULL squares with the function amount_of_squares
    squares = amount_of_squares(p, v, busbar_sheet_r, ptc_sheet_r, coat)[1]

    # # we take h to be the largest side of the rectangle just for ease of calculations
    # if h < w:
    #     c = h
    #     h = w
    #     w = c
    #

    #
    # # Assume we can max have 0.5 square and 2 square:
    # min_squares = squares*0.5
    # max_squares = squares*2
    #
    # # we want at least a coverage of 30% and at max a coverage of 80%:
    # min_area_carbon_elements = 0.3*h*w
    #
    # # Hence, the max and min area of one carbon element/square:
    # min_area_one_element = min_area_carbon_elements/max_squares
    # max_area_one_element = min_area_carbon_elements/min_squares
    #
    # # if we assume squares are between 0.5 and 10mm then the min and max dimension of a square are:
    # min_dimension = min_area_one_element/10
    # max_dimension = max_area_one_element/0.5

    # max_area_left = 7*7
    # min_area_left = 2.5*2.5
    # if min_area_left <= 0.3*0.3:
    #     min_area_left = 0.3*0.3
    # print([math.sqrt(max_area_left), math.sqrt(min_area_left), max_area_left, min_area_left])

    for margin_H in np.arange(1.5, 3, 0.1):

        if sol >= 400000000:
            print("break")
            break

        for margin_W in np.arange(1.5, 3, 0.1):

            h_real = h - 2*margin_H
            w_real = w - 2*margin_W

            for square_W in np.arange(min_dimension, max_dimension, 0.5):

                for space_W in np.arange(math.sqrt(min_area_left), math.sqrt(max_area_left), 0.5):

                    for square_H in np.arange(min_dimension, max_dimension, 0.5):

                        for space_H in np.arange(math.sqrt(min_area_left), math.sqrt(max_area_left), 0.5):

                            # calculations of amount of elements needed considering the ratio square_W, square_H
                            real_squares = squares
                            if square_H <= square_W:
                                real_squares = round(square_W / square_H * squares)
                            elif square_H > square_W:
                                real_squares = round(square_H / square_W * squares)

                            if square_W*square_H*real_squares < h*w:

                                amount_sq_H = int((h_real+space_H)/(square_H + space_H))
                                if h - amount_sq_H*(square_H + space_H) >= square_H:
                                    amount_sq_H += 1
                                amount_sq_W = int((w_real+space_W) / (square_W + space_W))
                                if w - amount_sq_W*(square_W + space_W) >= square_W:
                                    amount_sq_W += 1

                                if amount_sq_H*amount_sq_W == real_squares and squares*square_H*square_W/(h*w) >= 0.3:
                                    solutions[f"{sol}"] = {
                                        "space_H": space_H,
                                        "space_W": space_W,
                                        "square_H": square_H,
                                        "square_W": square_W,
                                        "margin_H": (h-((space_H+square_H)*amount_sq_H-space_H))/2,
                                        "margin_W": (h-((space_W+square_W)*amount_sq_W-space_W))/2,
                                        "amount_sq_H": amount_sq_H,
                                        "amount_sq_W": amount_sq_W,
                                    }
                                    sol += 1

    return solutions
