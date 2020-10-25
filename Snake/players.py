import figs
from myfuncs import *
import turtle


class Character:
    def __init__(self, name, size, ccolor):
        self.name = name
        self.size = size
        self.color = ccolor
        self.direction = int(norm.heading())
        self.midtpos = [int(norm.pos()[0]), int(norm.pos()[1])]
        self.rightpos = norm.pos()[0] + self.size / 2
        self.leftpos = norm.pos()[0] - self.size / 2
        self.botpos = norm.pos()[1] - self.size / 2
        self.toppos = norm.pos()[1] + self.size / 2



    def drawplayer(self, coordinates):
        start_draw([coordinates[0], coordinates[1]])
        norm.fillcolor(self.color)
        norm.begin_fill()
        for k in range(4):
            position = norm.pos()
            norm.pendown()
            figs.rectangle(self.size - k * 2, self.size - k * 2, norm, 1, color=self.color)
            norm.penup()
            norm.setpos(position)

        norm.end_fill()
        stop_draw()
        # for k in [270, 90]:
        #     norm.setpos(coordinates)
        #     norm.setheading(k)
        #     norm.forward(self.size / 6.5)
        #     norm.setheading(0)
        #     norm.forward(self.size / 6)
        #     norm.pendown()
        #     figs.circle(self.size / 3.5, norm, 'white')
        # for direction in [1, -1]:
        #     norm.penup()
        #     norm.setpos(coordinates[0], coordinates[1] - self.size / 4)
        #     norm.pendown()
        #     norm.setheading(90 * direction)
        #     for k in range(10):
        #         norm.forward(1)
        #         norm.left(10 * direction)
        norm.setpos(coordinates)


    def drawtale(self, coordinates):
        startposition = norm.pos()
        start_draw([coordinates[0], coordinates[1]])
        norm.pensize(2)
        # figs.rectangle(self.size, self.size, norm, 1, color=self.color)
        figs.circle(self.size, norm, self.color)
        norm.pensize(1)
        stop_draw()
        norm.setpos(startposition)


# Characters
def square(ccolor):
    name = 'Square'
    size = 25
    csquare = Character(name, size, ccolor)
    csquare.drawplayer()
    return [name, size]
