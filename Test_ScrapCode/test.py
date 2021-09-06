from drawing_automation.autoClass import Heater
import pdfplumber
heat = Heater(1, 2, 3)
c = 0.35277578

with pdfplumber.open("Untitled-1.pdf") as pdf:
    curves = pdf.curves
    all_points = curves[0]["points"]
    print(all_points)

heat.open_corel()
heat.draw_line()
heat.adjust_height("1")
heat.adjust_width("1")
for i in all_points:
    heat.adjust_x(str(float(i[0])*c))
    heat.adjust_y(str(float(i[1])*c))
    heat.copy_paste(float(i[0])*c, float(i[1])*c)
