from front_end import Input
import tkinter as t
from calculator import calculate, amount_of_squares
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
    sq = amount_of_squares(power.get_input(), voltage.get_input(), sheet_busbar.get_input(), sheet_ptc.get_input(),
                           coat_thickness.get_input())
    busbar_width.config(text=f"busbar-width: {round(sq[0])} mm")
    squares.config(text=f"amount of full squares: {round(sq[1])}")
    response = calculate(height.get_input(), width.get_input(), power.get_input(), voltage.get_input(),
                         sheet_busbar.get_input(), sheet_ptc.get_input(), coat_thickness.get_input())
    pandas.DataFrame(response).transpose().to_csv("answers.csv")



button = t.Button(text="calculate", command=calculation)
button.grid(row=8, column=0, columnspan=2, pady=5)

busbar_width = t.Label(text="busbar-width: 0")
busbar_width.grid(row=9, column=0)

squares = t.Label(text="amount of full squares: 0")
squares.grid(row=9, column=1)

window.mainloop()
