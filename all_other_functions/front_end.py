import tkinter as t
from tkinter import *


class Input:
    def __init__(self, text, col, row, span=2):
        self.label = t.Label(text=text, font=("Arial", 10), bg="#283747", fg="white")
        self.label.grid(column=col, row=row, columnspan=span)
        self.input = t.Entry()
        self.input.grid(column=col+2, row=row, ipadx=20, ipady=5, padx=5, pady=5)

    def get_input(self):
        value = self.input.get()
        if "," in value:
            value = value.replace(",", ".")
        return float(value)


# ////////////////////////////////////////////////////////////////////////////////////////////////////////////////
class DropdownMenu:
    def __init__(self, list_possibilities, window, text_menu: str, text_label: str, col, row, span=2):
        self.label = t.Label(text=text_label, font=("Arial", 10), bg="#283747", fg="white")
        self.label.grid(column=col, row=row, columnspan=span)
        self.variable = StringVar(window)
        self.variable.set(text_menu)

        self.drop = t.OptionMenu(window, self.variable, *list_possibilities, command=self.get_dropdown_value)
        self.drop.config(highlightthickness=0, bd=0)
        self.drop.grid(row=row, column=col+2)
        self.chosen_value = ""

    def get_dropdown_value(self, selection):
        print(selection)
        self.chosen_value = selection
