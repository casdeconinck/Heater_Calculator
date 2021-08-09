from drawing_automation.autoClass import Heater
import pandas
import os
from pynput import keyboard
from pynput.keyboard import Key

# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# keep into account before starting automated drawing:
# adjust for personalised coordinates
# make sure coreldraw opens on full PC (not separate screen)
# make sure properties tab in corel draw is always open when coreldraw starts
# make sure everything is in 'mm' also in properties tab!


def draw(n):

    # safety to stop function
    def on_press(key):
        if key == Key.space:
            os._exit(0)

    with keyboard.Listener(on_press=on_press, suppress=False) as listener:
        # reading the csv file we got from our main program (which triggered calculator.py)
        d = pandas.read_csv("./CSV_files/answers.csv")

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

        # create an object of class Heater (contains steps for drawing in coreldraw)
        heater = Heater(height, width, busbar_width)

        # command you need to run to know position on screen: print(heater.mouse.position)
        # open coreldraw and create the first line at position (30, 200)
        heater.open_corel()
        heater.go_back_to_properties_tab()
        heater.draw_line()
        heater.adjust_x("30")
        heater.adjust_y("200")

        # PTC elements
        # draw dimensions of first ptc element
        # we make sure there is some overlap of ptc elements and the silver fingers
        if float(space_H) - 2 * float(silver_fingers_width) - 0.4 > 0.5:
            heater.adjust_height(str(float(square_H) + 2 * float(silver_fingers_width) + 0.6))
        else:
            heater.adjust_height(str(float(square_H) + 2 * float(silver_fingers_width) + 0.4))
        heater.adjust_width(str(square_W))

        # change coordinates of this element
        heater.last_xcor = 30 + float(busbar_width) / 2 + margin_W + square_W / 2
        heater.last_ycor = 200 + float(height) / 2 - margin_H - square_H / 2
        heater.adjust_x(str(heater.last_xcor))
        heater.adjust_y(str(heater.last_ycor))

        # first we create one row by transforming/copying this element
        heater.go_to_transform_tab()
        heater.transform_x_cor(str(space_W+square_W))
        heater.transform_y_cor("0")
        heater.transform_copies(str(amount_sq_W-1))
        heater.go_back_to_properties_tab()

        # make silver fingers
        heater.silver_fingers(silver_fingers_width, float(silver_fingers_length), float(height), float(margin_H),
                              float(busbar_width), float(square_H), float(margin_W))

        # select this row and transform/copy in -y direction
        heater.select_everything()
        heater.go_to_transform_tab()
        heater.transform_y_cor("-"+str(space_H + square_H))
        heater.transform_x_cor("0")
        heater.transform_copies(str(amount_sq_H - 1))
        heater.go_back_to_properties_tab()

        # create the busbars
        heater.create_busbar("30", height, busbar_width)
        heater.create_busbar(str(float(width)+30), height, busbar_width)
    listener.join()
