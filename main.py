from all_other_functions.front_end import Input, DropdownMenu
import tkinter as t
from calculator import calculate, amount_of_elements
import pandas
from drawing_automation.Visualisation import visual
from all_other_functions.other_functions import get_database_info, busbar_styles
from all_other_functions.drawing_start_function import start_drawing
from TkinterDnD2 import DND_FILES, TkinterDnD
import cv2 as cv
from all_other_functions.irregular_shape_other_functions import *

PATH = ""
irregular = False
# colors for GUI
TEXT_COLOR = "white"
BG = "#283747"

# setting up graphical user interface
window = TkinterDnD.Tk()
window.title("Calculate heater dimensions")
window.minsize(width=800, height=1400)
window.config(padx=50, pady=50, bg=BG)


def not_rectangle():
    global irregular

    def drop_inside_list_box(event):
        global PATH
        listb.insert("end", event.data)
        PATH = event.data
    irregular = True
    width.remove()
    height.remove()
    label = t.Label(text="Drag and drop file:", font=("Arial", 10), bg="#283747", fg="white")
    label.grid(column=0, row=8, columnspan=2)
    listb = t.Listbox(window, selectmode=t.SINGLE, background="green", height=3, width=30)
    listb.grid(column=2, row=8)
    listb.drop_target_register(DND_FILES)
    listb.dnd_bind("<<Drop>>", drop_inside_list_box)


# setting up input fields with the help of the Input class, found in folder front_end
# temp = Input("Temperature [°C]: ", 0, 0)
# temp.input.focus()
power = Input("Power [W]: ", 0, 1)
power.input.focus()
voltage = Input("Voltage [V]: ", 0, 2)
sheet_busbar = Input("Sheet resistance busbar [ohm/sq/25um]: ", 0, 3)
ptc_ink = DropdownMenu(["PTC 40", "PTC 60", "PTC 60-HV", "PTC 90", "PTC 120"], window, "select one", "PTC ink:", 0, 4)
coat_thickness_silver = Input("Coat thickness silver [um]: ", 0, 5)
min_finger_width = Input("minimal silver fingers width [mm]: ", 0, 6)
rectangle = t.Checkbutton(window, text="Irregular shape", command=not_rectangle)
rectangle.grid(column=4, row=8)
width = Input("Width [mm]: ", 0, 8)
height = Input("Height [mm]: ", 0, 9)


# different busbar styles, function can be found in the file all_other_functions.py
busbar_styles(window, TEXT_COLOR)


# this function is responsible for starting the calculation (calculator.py)
def calculation():
    global PATH
    print(PATH)
    from all_other_functions.other_functions import busbar_style
    # called upon pressing the button in the GUI (arrow to the right). It will generate two csv files.
    # one with all possibilities and all design rules and another one for selecting the best possibility (see CSV_files)
    # sheet resistance and coat thickness based on google spreadsheet, ptc printed with 61-64, 65 squeegee, 35 emulsion
    ptc_info = get_database_info(ptc_ink.chosen_value)
    sheet_ptc = float(ptc_info["resistance"])
    coat_thickness_ptc = float(ptc_info["thickness"])

    sq = amount_of_elements(power.get_input(), voltage.get_input(), sheet_busbar.get_input(), sheet_ptc,
                            coat_thickness_ptc, coat_thickness_silver.get_input())
    busbar_width.config(text=f"busbar-width: {round(sq[0])} mm")
    squares.config(text=f"amount of ptc elements (aspect ratio of 1): {round(sq[1])}")
    if irregular:
        image = cv.imread(PATH)
        h_pix = image.shape[0]
        w_pix = image.shape[1]
        matrix = get_matrix(h_pix, w_pix, image)
        matrix = matrix[~np.all(matrix == 0, axis=1)]
        matrix_rows, matrix_columns = matrix.shape
        [area, dimension_rectangle] = get_area(matrix, matrix_rows)
        print(area)
        print(dimension_rectangle)
        response = calculate(dimension_rectangle, dimension_rectangle, power.get_input(), voltage.get_input(),
                             sheet_busbar.get_input(), sheet_ptc, coat_thickness_ptc,
                             coat_thickness_silver.get_input(), busbar_style, min_finger_width.get_input())
    else:
        response = calculate(height.get_input(), width.get_input(), power.get_input(), voltage.get_input(),
                             sheet_busbar.get_input(), sheet_ptc, coat_thickness_ptc,
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

    start_drawing(window, BG, TEXT_COLOR, irregular, PATH)
    # gives a first visualisation drawn with turtle library
    visual()


# Other buttons in the GUI
start = t.PhotoImage(file="images/start.jpg").subsample(5, 5)
start2 = t.PhotoImage(file="images/start2.jpg").subsample(5, 5)

button = t.Button(image=start, command=calculation, highlightthickness=0, bd=0,  bg=BG, fg=TEXT_COLOR)
button.grid(row=12, column=0, columnspan=2, pady=5)

button = t.Button(image=start2, command=lambda: start_drawing(window, BG, TEXT_COLOR, irregular, PATH),
                  highlightthickness=0, bd=0,
                  bg=BG, fg=TEXT_COLOR)
button.grid(row=12, column=2, pady=5)

busbar_width = t.Label(text="busbar-width: 0", font=("Arial", 12),  bg=BG, fg=TEXT_COLOR)
busbar_width.grid(row=13, column=0)

squares = t.Label(text="amount of ptc elements: 0", font=("Arial", 12), bg=BG, fg=TEXT_COLOR)
squares.grid(row=13, column=2)


window.mainloop()
