from drawing_automation.autoClass import Busbar
l = Busbar(1, 2, 3)

l.open_corel()
l.draw_line()
l.got_to_transform_tab()
l.transform_y_cor("10")
l.transform_copies("4")
l.go_back_to_properties_tab()
#
# mouse = MouseController()
# print(mouse.position)



from drawing_automation.autoClass import Busbar
import pandas
import time
import numpy as np
from pynput.keyboard import Key
from pynput.mouse import Button
# from Visualisation import max_coverage
import keyboard

# keep into account before starting automated drawing:
# keeping space key pressed for a while will terminate the program
# adjust for personalised coordinates
# make sure coreldraw opens on full PC (not separate screen)
# make sure properties tab in corel draw is always open when coreldraw starts
# make sure everything is in 'mm' also in properties tab!


def draw(n):
    # reading the csv file we got from our main program
    d = pandas.read_csv("../CSV_files/answers.csv")
    # n = max_coverage(d)[1]
    space_H = d["space_H"][n]
    space_W = d["space_W"][n]
    square_H = d["square_H"][n]
    square_W = d["square_W"][n]
    margin_H = d["margin_H"][n]
    margin_W = d["margin_W"][n]
    amount_sq_H = d["amount_sq_H"][n]
    amount_sq_W = d["amount_sq_W"][n]
    busbar_width = str(d["busbar_width"][n])
    height = str(d["h"][n])
    width = str(d["w"][n]+float(busbar_width))
    if float(busbar_width)/amount_sq_H >= 0.2:
        silver_fingers_width = float(busbar_width)/amount_sq_H
    else:
        silver_fingers_width = 0.2
    silver_fingers_length = float(width)-float(busbar_width)

    # create an object of class Busbar (also used for ptc elements)
    busbar = Busbar(height, width, busbar_width)

    # command you need to run to know position on screen: print(busbar.mouse.position)
    # open coreldraw and create the first line at position (30, 200)
    busbar.open_corel()
    busbar.draw_line()
    busbar.adjust_x("30")
    busbar.adjust_y("200")
    busbar.adjust_height(height)
    busbar.adjust_width(busbar_width)

    # PTC elements
    # first we print one row
    for i in np.arange(0, amount_sq_W):
        if keyboard.is_pressed("space"):
            time.sleep(10)
            break

        if i == 0:
            xcor = 30 + float(busbar_width)/2 + margin_W + square_W/2
            busbar.last_ycor = 200 + float(height)/2 - margin_H - square_H/2
            time.sleep(0.4)
            print(xcor)
            # we make sure there is some overlap of ptc elements and the silver fingers
            if float(space_H) - 2*float(silver_fingers_width) - 0.4 > 0.5:
                busbar.adjust_height(str(float(square_H) + 2*float(silver_fingers_width) + 0.6))
            else:
                busbar.adjust_height(str(float(square_H) + 2 * float(silver_fingers_width) + 0.4))
            busbar.adjust_width(str(square_W))
        else:
            xcor = busbar.last_xcor + space_W + square_W
            busbar.copy_paste(busbar.last_xcor, busbar.last_ycor)
        time.sleep(0.5)
        busbar.adjust_x(str(xcor))
        busbar.adjust_y(str(busbar.last_ycor))
        busbar.last_xcor = xcor

    # we copy paste each row to make it faster
    for j in np.arange(0, amount_sq_H-1):
        if keyboard.is_pressed("space"):
            time.sleep(10)
            break

        if j == 0:
            ycor = 200 + float(height)/2 - margin_H-square_H/2 - space_H - square_H
            busbar.last_xcor = 30+(float(width)/2)
            busbar.mouse.position = (1361, 451)
            busbar.mouse.click(Button.left, 1)
            time.sleep(0.5)
            with busbar.keyboard.pressed(Key.ctrl):
                busbar.keyboard.press("a")
                busbar.keyboard.release("a")
            time.sleep(0.5)
            with busbar.keyboard.pressed(Key.ctrl):
                busbar.keyboard.press("c")
                busbar.keyboard.release("c")
            time.sleep(0.5)
            with busbar.keyboard.pressed(Key.ctrl):
                busbar.keyboard.press("v")
                busbar.keyboard.release("v")
        else:
            busbar.mouse.position = (1361, 451)
            busbar.mouse.click(Button.left, 1)
            ycor = busbar.last_ycor - space_H - square_H
            with busbar.keyboard.pressed(Key.ctrl):
                busbar.keyboard.press('v')
                busbar.keyboard.release('v')
        time.sleep(0.5)
        busbar.adjust_y(str(ycor))
        busbar.last_ycor = ycor

    # create the busbars
    busbar.mouse.position = (26, 275)
    busbar.mouse.click(Button.left, 1)
    time.sleep(1)
    busbar.mouse.position = (69, 289)
    busbar.mouse.click(Button.left, 1)
    time.sleep(1)
    time.sleep(0.5)
    busbar.draw_line()
    busbar.adjust_x("30")
    busbar.adjust_y("200")
    busbar.adjust_height(height)
    busbar.adjust_width(busbar_width)

    # second busbar
    busbar.mouse.position = (26, 275)
    busbar.mouse.click(Button.left, 1)
    time.sleep(1)
    busbar.mouse.position = (69, 289)
    busbar.mouse.click(Button.left, 1)
    time.sleep(1)
    time.sleep(0.5)
    busbar.draw_line()
    busbar.adjust_x(str(float(width)+30))
    busbar.adjust_y("200")
    busbar.adjust_height(height)
    busbar.adjust_width(busbar_width)

    time.sleep(0.4)
    # make silver fingers and scallop at the ends
    # busbar.scallop(silver_fingers_width)
    busbar.silver_fingers(silver_fingers_width, float(silver_fingers_length), int(amount_sq_H),
                          float(height), float(margin_H), float(busbar_width), float(square_H), float(space_H),
                          float(margin_W))

    def silver_fingers(self, fingers_width, fingers_length: float, squares_height, height: float, margin_H: float,
                       busbar_width: float, square_height, space_height, margin_W):
        self.draw_line_horizontal()
        time.sleep(0.5)
        self.adjust_width_of_non_lines(str(fingers_length - 0.5 * margin_W))
        time.sleep(0.5)
        self.adjust_width(str(fingers_width))
        time.sleep(0.5)
        y_top = 0
        y_bottom = 0
        for i in range(0, 2 * squares_height):
            if keyboard.is_pressed("space"):
                time.sleep(10)
                break

            if i % 2 == 0:
                x = 30 + fingers_length / 2 + busbar_width / 2 - 0.6 * margin_W
                if i == 0:
                    ycor_t = 200 + float(height) / 2 - margin_H + fingers_width / 2
                else:
                    time.sleep(0.3)
                    with self.keyboard.pressed(Key.ctrl):
                        self.keyboard.press('c')
                        self.keyboard.release('c')
                    time.sleep(0.3)
                    with self.keyboard.pressed(Key.ctrl):
                        self.keyboard.press('v')
                        self.keyboard.release('v')
                    time.sleep(0.3)
                    ycor_t = y_top - square_height - space_height
                self.adjust_y(str(ycor_t))
                self.adjust_x(str(x))
                y_top = ycor_t
            else:
                x = 30 + fingers_length / 2 + (busbar_width / 2) + 0.6 * margin_W
                time.sleep(0.3)
                with self.keyboard.pressed(Key.ctrl):
                    self.keyboard.press('c')
                    self.keyboard.release('c')
                time.sleep(0.3)
                with self.keyboard.pressed(Key.ctrl):
                    self.keyboard.press('v')
                    self.keyboard.release('v')
                time.sleep(0.3)
                if i == 1:
                    ycor_b = 200 + float(height) / 2 - margin_H - fingers_width / 2 - square_height
                else:
                    ycor_b = y_bottom - square_height - space_height
                self.adjust_y(str(ycor_b))
                self.adjust_x(str(x))
                y_bottom = ycor_b

