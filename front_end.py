import tkinter as t


class Input:
    def __init__(self, text, col, row):
        self.label = t.Label(text=text, font=("Arial", 10), bg="#283747", fg="white")
        self.label.grid(column=col, row=row, columnspan=2)
        self.input = t.Entry()
        self.input.grid(column=col+2, row=row, ipadx=20, ipady=5, padx=5, pady=5)

    def get_input(self):
        value = self.input.get()
        if "," in value:
            value = value.replace(",", ".")
        return float(value)
