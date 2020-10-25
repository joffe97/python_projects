import keyboard
from turtle import *

# Turtles
# global pen
# global pen2
# global pen3
# global pen4
# global pen5

norm = Turtle()
pen = Turtle()
pen2 = Turtle()
pen3 = Turtle()
pen4 = Turtle()
pen5 = Turtle()


def clear_all():
    norm.clear()
    pen.clear()
    pen2.clear()
    pen3.clear()
    pen4.clear()
    pen5.clear()


def hide_pen(turt):
    while turt.isvisible():
        turt.hideturtle()


def start_draw(coordinates=[0, 0], turt=norm, pen_size=1):
    # if turt is None:
    #     penup()
    #     goto(coordinates)
    #     pendown()
    # else:
    turt.pensize(pen_size)
    turt.penup()
    turt.goto(coordinates)
    turt.pendown()


def stop_draw(turt=norm):
    # if turt is None:
    #     penup()
    # else:
    turt.penup()
    turt.pensize(1)


def draw(coordinates=[0, 0], func=None, input1=None, input2=None, input3=None, input4=None, drawing=1, turt=pen):
    # if turt is None:
    #     penup()
    #     goto(coordinates)
    #     if drawing == 1:
    #         pendown()
    # else:
    turt.penup()
    turt.goto(coordinates)
    if drawing == 1:
        turt.pendown()

    if input1 is None:
        func()
    elif input2 is None:
        func(input1)
    elif input3 is None:
        func(input1, input2)
    elif input4 is None:
        func(input1, input2, input3)
    elif input4 is not None:
        func(input1, input2, input3, input4)


def activetyping():  # Ikke i bruk
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
               'v', 'w', 'x', 'y', 'z', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9']

    while True:
        for k in letters:
            if keyboard.is_pressed('backspace'):
                return '  '
            elif keyboard.is_pressed('enter'):
                return '..'
            elif keyboard.is_pressed(k):
                while keyboard.is_pressed(k):
                    None
                return k

    # if keyboard.is_pressed('backspace'):
    #     while keyboard.is_pressed('backspace'):
    #         None
    #     return 'delete'
