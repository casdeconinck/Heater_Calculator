from turtle import Turtle, Screen
import pandas
import time


def max_coverage(file):
    maximum = 0
    index = 0
    for l in range(0, len(file["square_W"])):
        m = file["square_W"][l]*file["square_H"][l]*file["amount_sq_H"][l]*file["amount_sq_W"][l]
        if m > maximum:
            maximum = m
            index = l
    return [maximum, index]


def visual():

    # 200mm equals 2000px (scale). This can be adjusted depending on dimensions of the substrate
    scale = 2000/200
    d = pandas.read_csv(r"./CSV_files/answers.csv")
    n = max_coverage(d)[1]
    coverage = round((float(max_coverage(d)[0])/(float(d[d.index == n]['h'])*float(d[d.index == n]['w'])))*100)
    print(f"maximal covered area of ptc elements: "
          f"{coverage}%")
    print(f"number in answers.csv with max coverage: {max_coverage(d)[1]}")
    print(d[d.index == n])

    h = d["h"][n]*scale
    w = d["w"][n]*scale

    t_w = scale*d["square_W"][n]
    t_h = scale*d["square_H"][n]

    m_w = scale*d["margin_W"][n]
    m_h = scale*d["margin_H"][n]

    s_w = d["space_W"][n]*scale
    s_h = d["space_H"][n]*scale

    amount_w = int(d["amount_sq_W"][n])
    amount_h = int(d["amount_sq_H"][n])

    t = Turtle()
    screen = Screen()
    screen.setup(height=h+100, width=w+100)
    screen.tracer(0)

    t.hideturtle()
    t.penup()
    t.speed("fastest")
    t.goto(-w/2, -h/2)
    t.pendown()
    t.forward(w)
    t.left(90)
    t.forward(h)
    t.left(90)
    t.forward(w)
    t.left(90)
    t.forward(h)

    previous_x = 0
    previous_y = 0

    for i in range(0, amount_w):
        if i == 0:
            x = -w/2 + (m_w + t_w/2)
        else:
            x = previous_x + s_w + t_w
        for j in range(0, amount_h):
            new_turtle = Turtle()
            new_turtle.shape("square")
            new_turtle.shapesize(t_h / 20, t_w / 20)
            if j == 0:
                y = h/2 - (m_h+t_h/2)

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
