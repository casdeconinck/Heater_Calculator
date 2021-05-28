import tkinter as t


class Input:
    def __init__(self, text, col, row):
        self.label = t.Label(text=text)
        self.label.grid(column=col, row=row)
        self.input = t.Entry()
        self.input.grid(column=col+1, row=row, ipadx=20, ipady=5, padx=5, pady=5)

    def get_input(self):
        return float(self.input.get())
