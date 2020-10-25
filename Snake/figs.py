from myfuncs import pen
import math


def middlestartfunc(xlength, ylength, turt):
    penisdown = turt.isdown()
    turt.penup()
    turt.setheading(0)
    turt.forward(ylength / 2)
    turt.setheading(270)
    turt.forward(xlength / 2)
    if penisdown:
        turt.pendown()
    elif not penisdown:
        turt.penup()


def rectangle(xlength, ylength, turt=pen, middlestart=0, color=None):
    if middlestart:
        middlestartfunc(xlength, ylength, turt)
    if color is not None:
        turt.fillcolor(color)
        turt.begin_fill()
    for k in [90, 270]:
        turt.setheading(k)
        turt.forward(xlength)

        turt.setheading(k + 90)
        turt.forward(ylength)
    if color is not None:
        turt.end_fill()


def circle(diameter, turt=pen, color=None):
    penisdown = turt.isdown()
    direction = turt.heading()
    turt.penup()
    turt.setheading(90)
    turt.forward(diameter / 2)
    if penisdown:
        turt.pendown()
    elif not penisdown:
        turt.penup()
    turt.setheading(0)
    if color is not None:
        turt.fillcolor(color)
        turt.begin_fill()
    turt.circle(diameter / 2)
    if color is not None:
        turt.end_fill()
    turt.setheading(direction)


def star(length, turt=pen, color=None):
    penisdown = turt.isdown()
    direction = turt.heading()
    turt.penup()
    turt.setheading(0)
    turt.forward(0.5 * math.sqrt(length**2 + length / (2 * math.tan(54))))
    turt.setheading(162)
    if penisdown:
        turt.pendown()
    elif not penisdown:
        turt.penup()
    if color is not None:
        turt.fillcolor(color)
        turt.begin_fill()
    for k in range(5):
        turt.forward(length)
        turt.right(144)
    if color is not None:
        turt.end_fill()
    turt.setheading(direction)
