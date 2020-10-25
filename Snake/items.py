import random
from myfuncs import *
import figs

itemattributes_layout = dict(score_instant=0, score_tick=0.05, speed=0, size=0, tales=1)
itemattributes_current = itemattributes_layout.copy()
att1 = itemattributes_layout.copy()
att2 = itemattributes_layout.copy()


class Items:
    def __init__(self, border, itemnumber):
        if itemnumber == 1:
            itemnumber = att1
        elif itemnumber == 2:
            itemnumber = att2
        self.size = 25
        xpos = random.randrange(int(-border[0] + self.size / 2), int(border[0] - self.size / 2), 10)
        ypos = random.randrange(int(-border[1] + self.size / 2), int(border[1] - self.size / 2), 10)
        self.position = [xpos, ypos]
        self.area = [[xpos - self.size / 2, xpos + self.size / 2],
                     [ypos - self.size / 2, ypos + self.size / 2]]
        self.itemname = random.choice((negspeed1, score_tick1, size1, negsize1, tales1))
        self.itemname(self.position, itemnumber)


def negspeed1(coordinates, itemnumber):
    size = 25
    start_draw(coordinates, pen5, 2)
    figs.rectangle(size, size, pen5, 1, 'red')
    if itemattributes_current['speed'] >= 300:
        itemnumber['speed'] -= 300
    itemnumber['score_instant'] -= 50
    stop_draw(pen5)


def score_tick1(coordinates, itemnumber):
    size = 25
    start_draw(coordinates, pen5, 2)
    figs.rectangle(size, size, pen5, 1, 'blue')
    stop_draw(pen5)
    itemnumber['speed'] += 50
    itemnumber['score_tick'] += 0.02


def size1(coordinates, itemnumber):
    size = 30
    start_draw(coordinates, pen5, 2)
    figs.circle(size, pen5, 'pink')
    stop_draw(pen5)
    itemnumber['size'] += 10


def negsize1(coordinates, itemnumber):
    size = 22
    start_draw(coordinates, pen5, 2)
    figs.circle(size, pen5, 'yellow')
    stop_draw(pen5)
    if -20 < itemattributes_current['size'] < 0:
        itemnumber['size'] *= 1.2
    else:
        itemnumber['size'] -= 5
    itemnumber['speed'] += 30
    itemnumber['score_instant'] = 20


def tales1(coordinates, itemnumber):
    size = 30
    start_draw(coordinates, pen5, 2)
    pen5.penup()
    figs.star(size, pen5, 'green')
    stop_draw(pen5)
    itemnumber['tales'] += 1
    itemnumber['score_tick'] += 0.01
