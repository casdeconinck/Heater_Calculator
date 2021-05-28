from turtle import Turtle, Screen
import pandas
import time
# 200mm equals 500px


n = 30
d = pandas.read_csv("answers.csv")

maximum = 0
index = 0
for i in range(0, len(d["square_W"])):
    m = d["square_W"][i]*d["square_H"][i]*d["amount_sq_H"][i]*d["amount_sq_W"][i]
    if m > maximum:
        maximum = m
        index = i
print([maximum, index])

# print((d["square_W"]*d["square_H"]).max)
# print(d[(d["square_W"]*d["square_H"]) == 85.5].index)

t_w = 500*d["square_W"][n]/200
t_h = 500*d["square_H"][n]/200

m_w = 500*d["margin_W"][n]/200
m_h = 500*d["margin_H"][n]/200

s_w = d["space_W"][n]*500/200
s_h = d["space_H"][n]*500/200

amount_w = int(d["amount_sq_W"][n])
amount_h = int(d["amount_sq_H"][n])

t = Turtle()
screen = Screen()
screen.setup(height=600, width=600)
screen.tracer(0)

t.hideturtle()
t.penup()
t.speed("fastest")
t.goto(-87.5, -112.5)
t.pendown()
t.forward(175)
t.left(90)
t.forward(225)
t.left(90)
t.forward(175)
t.left(90)
t.forward(225)

previous_x = 0
previous_y = 0

for i in range(0, amount_w):
    if i == 0:
        x = -87.5 + (m_w + t_w/2)
    else:
        x = previous_x + s_w + t_w
    for j in range(0, amount_h):
        new_turtle = Turtle()
        new_turtle.shape("square")
        new_turtle.shapesize(t_h / 20, t_w / 20)
        if j == 0:
            y = 112.5 - (m_h+t_h/2)

        else:
            y = previous_y - s_h - t_h
        new_turtle.penup()
        new_turtle.speed("fastest")
        new_turtle.goto(x, y)
        previous_x = x
        previous_y = y
time.sleep(0.1)
screen.update()

screen.mainloop()
