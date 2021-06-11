import math
import numpy as np


def amount_of_squares(p, v, busbar_sheet_r, ptc_sheet_r, coat_ptc, coat_silver):
    watt_density = 0.2
    # this is suggested by Henkel (in W/cm2)

    r = v ** 2 / p
    i = v / r

    busbar_width = (math.sqrt((busbar_sheet_r * 25 / coat_silver) * i ** 2 / watt_density))*10
    # in mm
    squares = (ptc_sheet_r * 25 / coat_ptc) / r
    print(squares)

    return [busbar_width, squares]


def calculate(h, w, p, v, busbar_sheet_r, ptc_sheet_r, coat_ptc, coat_silver):

    solutions = {}
    sol = 0
    # calculate the amount of FULL squares with the function amount_of_squares
    spec = amount_of_squares(p, v, busbar_sheet_r, ptc_sheet_r, coat_ptc, coat_silver)
    squares = spec[1]
    busbar_width = spec[0]
    w = int(w - 2*float(busbar_width))
    h = int(h - float(busbar_width))
    print(h)
    print(w)

    for margin_H in np.arange(0.5, 3, 0.2):

        if sol >= 400000000:
            print("break")
            break

        for margin_W in np.arange(0.5, 3, 0.2):

            h_real = h - 2*margin_H
            w_real = w - 2*margin_W

            for square_W in np.arange(0.5, 5, 0.5):

                for space_W in np.arange(0.5, 5, 0.5):

                    for square_H in np.arange(0.5, 5, 0.5):

                        for space_H in np.arange(0.5, 5, 0.5):

                            # the amount of squares depend on the width and height of the squares:
                            real_squares = round(square_H / square_W * squares)

                            if square_W*square_H*real_squares < h_real*w_real:

                                amount_sq_H = int((h_real+space_H)/(square_H + space_H))
                                amount_sq_W = int((w_real+space_W) / (square_W + space_W))

                                coverage = real_squares*square_H*square_W/(h*w)
                                if amount_sq_H*amount_sq_W == real_squares and coverage >= 0.3:
                                    solutions[f"{sol}"] = {
                                        "space_H": space_H,
                                        "space_W": space_W,
                                        "square_H": square_H,
                                        "square_W": square_W,
                                        "margin_H": (h-((space_H+square_H)*amount_sq_H-space_H))/2,
                                        "margin_W": (w-((space_W+square_W)*amount_sq_W-space_W))/2,
                                        "amount_sq_H": amount_sq_H,
                                        "amount_sq_W": amount_sq_W,
                                        "h": h,
                                        "w": w,
                                        "busbar_width": busbar_width
                                    }
                                    sol += 1

    return solutions
