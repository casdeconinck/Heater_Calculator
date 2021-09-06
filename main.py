from front_end import Input
import tkinter as t
from tkinter import *
from calculator import calculate, amount_of_elements
import pandas
from drawing_automation.Visualisation import visual
from drawing_automation.automation import draw

# colors for GUI
TEXT_COLOR = "white"
BG = "#283747"

# setting up graphical user interface
window = t.Tk()
window.title("Calculate heater dimensions")
window.minsize(width=800, height=1400)
window.config(padx=50, pady=50, bg=BG)

# setting up input fields with the help of the Input class, found in folder front_end
# temp = Input("Temperature [°C]: ", 0, 0)
# temp.input.focus()
power = Input("Power [W]: ", 0, 1)
power.input.focus()
voltage = Input("Voltage [V]: ", 0, 2)
width = Input("Width [mm]: ", 0, 3)
height = Input("Height [mm]: ", 0, 4)
sheet_busbar = Input("Sheet resistance busbar [ohm/sq/25um]: ", 0, 5)
sheet_ptc = Input("Sheet resistance ptc ink [ohm/sq/25um]: ", 0, 6)
coat_thickness_ptc = Input("Coat thickness ptc [um]: ", 0, 7)
coat_thickness_silver = Input("Coat thickness silver [um]: ", 0, 8)
min_finger_width = Input("minimal silver fingers width [mm]: ", 0, 9)

# change color of busbar button when a certain style is picked in the GUI
busbar_style = 1
choose_busbar = t.Label(text="choose your busbar configuration:",
                        font=("Arial", 12), bg=BG, fg=TEXT_COLOR)
choose_busbar.grid(row=10, column=0, columnspan=3, pady=(20, 0))


def first_busbar(_s):
    global busbar_style
    canvas1.config(bg="green")
    canvas2.config(bg=BG)
    canvas3.config(bg=BG)
    busbar_style = 1


def second_busbar(_s):
    global busbar_style
    canvas1.config(bg=BG)
    canvas2.config(bg="green")
    canvas3.config(bg=BG)
    busbar_style = 2


def third_busbar(_s):
    global busbar_style
    canvas1.config(bg=BG)
    canvas2.config(bg=BG)
    canvas3.config(bg="green")
    busbar_style = 3


# draw busbar styles in GUI
canvas1 = t.Canvas(window, width=60, height=60, bg=BG, bd=0, highlightthickness=0)
canvas1.grid(row=11, column=0, pady=(5, 30), padx=70)
canvas1.create_line(20, 20, 40, 20, fill=TEXT_COLOR)
canvas1.create_line(20, 20, 20, 40, fill="red")
canvas1.create_line(40, 20, 40, 40, fill=TEXT_COLOR)
canvas1.bind("<Button-1>", first_busbar)

canvas2 = t.Canvas(window, width=60, height=60, bg=BG, bd=0, highlightthickness=0)
canvas2.grid(row=11, column=1, pady=(5, 30))
canvas2.create_line(20, 20, 20, 40, fill="red")
canvas2.create_line(40, 20, 40, 40, fill=TEXT_COLOR)
canvas2.bind("<Button-1>", second_busbar)

canvas3 = t.Canvas(window, width=60, height=60, bg="#283747", bd=0, highlightthickness=0)
canvas3.grid(row=11, column=2, pady=(5, 30))
canvas3.create_line(20, 20, 40, 20, fill="red")
canvas3.create_line(20, 20, 20, 40, fill="red")
canvas3.create_line(40, 20, 40, 40, fill=TEXT_COLOR)
canvas3.create_line(20, 40, 40, 40, fill=TEXT_COLOR)
canvas3.bind("<Button-1>", third_busbar)

# used in calculation(), will keep all different coverages generated and their associated aspect ratios
list_possibilities = []


# This function shows possibilities of answers in the GUI and is responsible for starting the drawing automation
def start_drawing():
    termination = t.Label(text="!!!! PRESS SPACE TO TERMINATE AUTOMATION !!!!",
                          font=("Arial", 17), bg=BG, fg=TEXT_COLOR)
    termination.grid(row=17, column=0, columnspan=3, pady=(40, 35))

    # display different coverages and aspect ratio belonging with them:
    doc = pandas.read_csv("CSV_files/select.csv")
    for number in range(0, len(doc["coverage [%]"])):
        tup = str(doc['coverage [%]'][number]) + " / " + str(doc["square/aspect-ratio"][number])
        if tup not in list_possibilities:
            list_possibilities.append(tup)

    def callback(selection):
        # selection contains a string "coverage(%) / aspect ratio"
        doc1 = pandas.read_csv("CSV_files/select.csv").transpose().to_dict()
        sel = selection.split("/")
        for i in doc1:
            # we check the csv file with all answers for the row number that matches our selection
            if doc1[i]["coverage [%]"] == float(sel[0]) and doc1[i]["square/aspect-ratio"] == float(sel[1]):
                # start drawing automation of the selection
                draw(i)
                break

    # displays on the drop down menu in the GUI
    variable = StringVar(window)
    variable.set("Draw heater with: coverage(%) / square(H/W)")

    # Input field if you want to choose a row out of the solutions yourself
    choose_row = t.Label(text="Choose a heater configuration to draw or give in the row you want to draw.",
                         font=("Arial", 12), bg=BG, fg=TEXT_COLOR)
    choose_row.grid(row=14, column=0, columnspan=3, pady=(50, 0))

    drop = OptionMenu(window, variable, *list_possibilities, command=callback)
    drop.config(highlightthickness=0, bd=0)
    drop.grid(row=15, column=0, columnspan=3, pady=(10, 10))

    row_input = t.Entry()
    row_input.grid(column=0, row=16, ipadx=20, ipady=5, padx=(190, 0), pady=5)

    # starts drawing of the row you've written in the input field
    def written_input():
        value = row_input.get()
        if "," in value:
            value = value.replace(",", ".")
        draw(int(value))

    # button to trigger written_input() function
    button1 = t.Button(text="draw this row number", command=written_input)
    button1.grid(row=16, column=2, padx=(0, 190), pady=5)


# this function is responsible for starting the calculation (calculator.py)
def calculation():
    # called upon pressing the button in the GUI (arrow to the right). It will generate two csv files.
    # one with all possibilities and all design rules and another one for selecting the best possibility (see CSV_files)
    global list_possibilities, busbar_style

    sq = amount_of_elements(power.get_input(), voltage.get_input(), sheet_busbar.get_input(), sheet_ptc.get_input(),
                            coat_thickness_ptc.get_input(), coat_thickness_silver.get_input())
    busbar_width.config(text=f"busbar-width: {round(sq[0])} mm")
    squares.config(text=f"amount of ptc elements (aspect ratio of 1): {round(sq[1])}")

    response = calculate(height.get_input(), width.get_input(), power.get_input(), voltage.get_input(),
                         sheet_busbar.get_input(), sheet_ptc.get_input(), coat_thickness_ptc.get_input(),
                         coat_thickness_silver.get_input(), busbar_style, min_finger_width.get_input())

    # generating a new dictionary for the select.csv file, especially for selecting a solution
    new_dict = {}
    for key in response:
        new_dict[key] = {
            "coverage [%]": response[key]["coverage [%]"],
            "amount of ptc elements": response[key]["amount of ptc elements"],
            "square/aspect-ratio":  response[key]["square/aspect-ratio"],
        }
    # sorting the dataframes by the aspect-ratio
    pandas.DataFrame(response).transpose().sort_values(by=["square/aspect-ratio", "coverage [%]"],
                                                       ascending=[True, False], ignore_index=True)\
        .to_csv("CSV_files/answers.csv")

    pandas.DataFrame(new_dict).transpose().sort_values(by=["square/aspect-ratio", "coverage [%]"],
                                                       ascending=[True, False], ignore_index=True)\
        .to_csv("CSV_files/select.csv")

    start_drawing()
    # gives a first visualisation drawn with turtle library
    visual()


# Other buttons in the GUI
start = t.PhotoImage(file="images/start.jpg").subsample(5, 5)
start2 = t.PhotoImage(file="images/start2.jpg").subsample(5, 5)

button = t.Button(image=start, command=calculation, highlightthickness=0, bd=0,  bg=BG, fg=TEXT_COLOR)
button.grid(row=12, column=0, columnspan=2, pady=5)
button = t.Button(image=start2, command=start_drawing, highlightthickness=0, bd=0,  bg=BG,
                  fg=TEXT_COLOR)
button.grid(row=12, column=2, pady=5)

busbar_width = t.Label(text="busbar-width: 0", font=("Arial", 12),  bg=BG, fg=TEXT_COLOR)
busbar_width.grid(row=13, column=0)

squares = t.Label(text="amount of ptc elements: 0", font=("Arial", 12), bg=BG, fg=TEXT_COLOR)
squares.grid(row=13, column=2)


window.mainloop()
