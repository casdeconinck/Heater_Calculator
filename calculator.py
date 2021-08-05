import math
import numpy as np


def amount_of_elements(p, v, busbar_sheet_r, ptc_sheet_r, coat_ptc, coat_silver):
    # this is suggested by Henkel (in W/cm2)
    watt_density = 0.2
    # resistance
    r = v ** 2 / p
    # current
    i = v / r
    # busbar width in mm
    busbar_width = (math.sqrt((busbar_sheet_r * 25 / coat_silver) * i ** 2 / watt_density))*10
    # amount of ptc-elements needed for the given power, voltage
    amount_ptc_elements = (ptc_sheet_r * 25 / coat_ptc) / r

    return [busbar_width, amount_ptc_elements]


def calculate(h, w, p, v, busbar_sheet_r, ptc_sheet_r, coat_ptc, coat_silver, busbar_style):
    # dictionary where we will store design parameters that fulfill the heater specs
    solutions = {}
    sol = 0
    # calculate the amount of ptc elements (for aspect ratio of 1) with the function amount_of_elements
    spec = amount_of_elements(p, v, busbar_sheet_r, ptc_sheet_r, coat_ptc, coat_silver)
    busbar_width = spec[0]
    elements = spec[1]

    # depending on how the busbars look
    w_min_busbar = int(w - 2 * float(busbar_width))
    h_min_busbar = h
    if busbar_style == 1:
        h_min_busbar = int(h - float(busbar_width))
    elif busbar_style == 2:
        h_min_busbar = h
    elif busbar_style == 3:
        h_min_busbar = int(h - 2*float(busbar_width))

    for margin_H in np.arange(0.5, 3, 0.2):

        if sol >= 400000000:
            print("break")
            break

        for margin_W in np.arange(0.5, 3, 0.2):

            h_real = h_min_busbar - 2*margin_H
            w_real = w_min_busbar - 2*margin_W

            # loop through possibilities for width and height of separate ptc elements and space between these elements
            for square_W in np.arange(0.5, 7, 0.2):

                for space_W in np.arange(0.3, 5, 0.3):

                    for square_H in np.arange(0.5, 7, 0.2):

                        for space_H in np.arange(0.3, 5, 0.3):

                            # the amount of squares depend on the width and height of the squares:
                            real_squares = round(square_H / square_W * elements)

                            if square_W*square_H*real_squares < h_real*w_real:

                                amount_sq_H = int((h_real+space_H)/(square_H + space_H))
                                amount_sq_W = int((w_real+space_W) / (square_W + space_W))

                                coverage = real_squares*square_H*square_W/(h_real*w_real)
                                # silver fingers are min 0,2 mm width, min 0,3 mm between overlapping ptc elements
                                # 0,2-0,3 overlap of elements over silver fingers
                                if amount_sq_H*amount_sq_W == real_squares and coverage >= 0.3 and \
                                        space_H - 2*(busbar_width/amount_sq_H) > 0.7 and space_H - 0.8 > 0.3 and \
                                        amount_sq_W*square_W + (amount_sq_W-1)*space_W + 2*margin_W <= w_real and \
                                        amount_sq_H*square_H + (amount_sq_H-1)*space_H + 2*margin_H <= h_real:
                                    solutions[f"{sol}"] = {
                                        "square": round(square_H/square_W, 3),
                                        "space_H": space_H,
                                        "space_W": space_W,
                                        "square_H": round(square_H, 2),
                                        "square_W": round(square_W, 2),
                                        "margin_H": round((h_min_busbar-((space_H+square_H)*amount_sq_H-space_H))/2, 3),
                                        "margin_W": round((w_min_busbar-((space_W+square_W)*amount_sq_W-space_W))/2, 3),
                                        "amount_sq_H": amount_sq_H,
                                        "amount_sq_W": amount_sq_W,
                                        "h": h_min_busbar,
                                        "w": w_min_busbar,
                                        "busbar_width": round(busbar_width, 3),
                                        "coverage [%]": round(coverage*100),
                                        "amount of ptc elements": real_squares,
                                        "square/aspect-ratio": round(square_H / square_W, 2)
                                    }
                                    sol += 1

    return solutions
