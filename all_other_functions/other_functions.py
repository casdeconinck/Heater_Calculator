import requests
import tkinter as t
from drawing_automation.automation import draw
from drawing_automation.draw_irregular_shape import draw_irregular
import sys
import os
busbar_style = 1
BG = "#283747"


def get_database(blad):
    """ sends a get request to google sheets, where the info about the ptc ink resides,
    it returns an array with the answers of the selected ink """
    endpoint = "https://api.sheety.co/d4ae87c445d7036d0d836aa0d701312e/ptc/"+blad
    response = requests.get(endpoint).json()[blad]
    return response


def get_database_info(data, ink: str):
    """ sends a get request to google sheets, where the info about the ptc ink resides,
    it returns an array with the answers of the selected ink """
    for i in data:
        if i["ink"] == ink:
            return i


def popup_window(i, irregular, window_to_close, PATH=""):
    """gives a pop-up window to ask if you are sure to start the drawing automation,
    If yes it will start the appropriate automation for a rectangle or an irregular shape"""
    popup = t.Tk()
    popup.minsize(width=400, height=200)
    popup.wm_title("Your chosen settings")
    label = t.Label(popup, text="do you want to continue?\n\nYou can stop the program any\n"
                                "time by pressing the space key", font=("Arial", 15))
    label.pack(side="top", fill="x", pady=10)
    if irregular:
        B1 = t.Button(popup, text="Continue", command=lambda: [popup.destroy(), draw_irregular(i, PATH, window_to_close)])
        B1.pack()
    else:
        B1 = t.Button(popup, text="Continue", command=lambda: [popup.destroy(), draw(i)])
        B1.pack()
    popup.mainloop()


def busbar_styles(window, TEXT_COLOR):
    """Responsible for drawing the 3 busbar configurations in the GUI. And it will also change the value of
     busbar style once it is clicked"""
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


def restart_program():
    """Restarts the current program.
    Note: this function does not return. Any cleanup action (like
    saving data) must be done before calling this function."""
    python = sys.executable
    os.execl(python, python, * sys.argv)
