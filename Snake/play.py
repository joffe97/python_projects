from turtle import *
from myfuncs import *

# Definere variabler
border = [1200/2, 800/2]
hastighet = 2


# Starter nytt frame
update()
pen.clear()

# Bevegelse
if pos()[1] < border[1]:
    move('w', 0, hastighet)
if pos()[0] > -border[0]:
    move('a', 270, hastighet)
if pos()[1] > -border[1]:
    move('s', 180, hastighet)
if pos()[0] < border[0]:
    move('d', 90, hastighet)

# Tegner
draw([-border[0] + 20, border[1] + 5], pen.write, str(pos()[1]), False, 'left', ('Arial', 16))
