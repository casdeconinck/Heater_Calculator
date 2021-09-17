import pandas
from all_other_functions.other_functions import popup_window
from tkinter import *

# used in calculation(), will keep all different coverages generated and their associated aspect ratios
list_possibilities = []


# This function shows possibilities of answers in the GUI and is responsible for starting the drawing automation
def start_drawing(window, BG, TEXT_COLOR):
    # display different coverages and aspect ratio belonging with them:
    doc = pandas.read_csv("././CSV_files/select.csv")
    for number in range(0, len(doc["coverage [%]"])):
        tup = str(doc['coverage [%]'][number]) + " / " + str(doc["square/aspect-ratio"][number])
        if tup not in list_possibilities:
            list_possibilities.append(tup)

    def callback(selection):
        # selection contains a string "coverage(%) / aspect ratio"
        doc1 = pandas.read_csv("././CSV_files/select.csv").transpose().to_dict()
        sel = selection.split("/")
        for i in doc1:
            # we check the csv file with all answers for the row number that matches our selection
            if doc1[i]["coverage [%]"] == float(sel[0]) and doc1[i]["square/aspect-ratio"] == float(sel[1]):
                # start drawing automation of the selection
                popup_window(i)
                break

    # displays on the drop down menu in the GUI
    variable = StringVar(window)
    variable.set("Draw heater with: coverage(%) / square(H/W)")

    # Input field if you want to choose a row out of the solutions yourself
    choose_row = Label(text="Choose a heater configuration to draw or give in the row you want to draw.",
                       font=("Arial", 12), bg=BG, fg=TEXT_COLOR)
    choose_row.grid(row=14, column=0, columnspan=3, pady=(50, 0))

    drop = OptionMenu(window, variable, *list_possibilities, command=callback)
    drop.config(highlightthickness=0, bd=0)
    drop.grid(row=15, column=0, columnspan=3, pady=(10, 10))

    row_input = Entry()
    row_input.grid(column=0, row=16, ipadx=20, ipady=5, padx=(190, 0), pady=5)

    # starts drawing of the row you've written in the input field
    def written_input():
        value = row_input.get()
        if "," in value:
            value = value.replace(",", ".")
        popup_window(int(value))

    # button to trigger written_input() function
    button1 = Button(text="draw this row number", command=written_input)
    button1.grid(row=16, column=2, padx=(0, 190), pady=5)
    termination = Label(text="!!!! PRESS SPACE TO TERMINATE AUTOMATION !!!!",
                        font=("Arial", 17), bg=BG, fg=TEXT_COLOR)
    termination.grid(row=17, column=0, columnspan=3, pady=(40, 35))
