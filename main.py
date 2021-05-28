from front_end import Input
import tkinter as t
from calculator import calculate
import pandas

window = t.Tk()
window.title("Calculate heater dimensions")
window.minsize(width=500, height=300)
window.config(padx=50, pady=50)

temp = Input("Temperature [°C]: ", 0, 0)
temp.input.focus()
power = Input("Power [W]: ", 0, 1)
voltage = Input("Voltage [V]: ", 0, 2)
width = Input("width [mm]: ", 0, 3)
height = Input("height [mm]: ", 0, 4)
sheet_busbar = Input("Sheet resistance busbar [ohm/sq/25um]: ", 0, 5)
sheet_ptc = Input("sheet resistance ptc ink [ohm/sq/25um]: ", 0, 6)
coat_thickness = Input("Coat thickness [um]: ", 0, 7)


def calculation():

    response = calculate(height.get_input(), width.get_input(), power.get_input(), voltage.get_input(),
                         sheet_busbar.get_input(), sheet_ptc.get_input(), coat_thickness.get_input())
    pandas.DataFrame(response).transpose().to_csv("answers.csv")


button = t.Button(text="calculate", command=calculation)
button.grid(row=8, column=0, columnspan=2, pady=5)

window.mainloop()
