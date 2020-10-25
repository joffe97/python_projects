import tkinter
import time
import numpy as np
import math
import random


class Ball:
    def __init__(self, canvas, startpos, radius, massetetthet=1, bounciness=0.6, color="red"):
        self.canvas = canvas

        self.radius = radius
        self.radius_physics = self.radius / 50
        self.volum = (4/3) * math.pi * self.radius_physics ** 3
        self.massetetthet = massetetthet * self.volum
        self.masse = self.volum * self.massetetthet
        self.bounciness = bounciness

        self.__xPos = np.array([startpos[0] - self.radius, startpos[0] + self.radius])
        self.__yPos = np.array([startpos[1] - self.radius, startpos[1] + self.radius])
        self.__xFart = 0
        self.__yFart = 0
        self.xAcc = 0
        self.yAcc = 0

        self.__xMidtPos = self.__xPos[0] + self.radius
        self.__yMidtPos = self.__yPos[0] + self.radius

        self.maxSpeed = 1000
        self.isgrounded = False

        self.gui = self.canvas.create_oval(self.xPos[0], self.yPos[0], self.xPos[1], self.yPos[1], fill=color)

        self.last_addforce = 0

    @property
    def xPos(self):
        return self.__xPos

    @xPos.setter
    def xPos(self, value):
        self.__xMidtPos = value[0] + self.radius
        self.__xPos = np.array(value)

    @property
    def yPos(self):
        return self.__yPos

    @yPos.setter
    def yPos(self, value):
        self.__yMidtPos = value[0] + self.radius
        self.__yPos = np.array(value)

    @property
    def xMidtPos(self):
        return self.__xMidtPos

    @xMidtPos.setter
    def xMidtPos(self, value):
        self.__xPos = np.array([value - self.radius, value + self.radius])
        self.__xMidtPos = value

    @property
    def yMidtPos(self):
        return self.__yMidtPos

    @yMidtPos.setter
    def yMidtPos(self, value):
        self.__yPos = np.array([value - self.radius, value + self.radius])
        self.__yMidtPos = value

    @property
    def xFart(self):
        return self.__xFart

    @xFart.setter
    def xFart(self, value):
        if value > self.maxSpeed:
            self.__xFart = self.maxSpeed
        elif value < -self.maxSpeed:
            self.__xFart = -self.maxSpeed
        else:
            self.__xFart = value

    @property
    def yFart(self):
        return self.__yFart

    @yFart.setter
    def yFart(self, value):
        if value > self.maxSpeed:
            self.__yFart = self.maxSpeed
        elif value < -self.maxSpeed:
            self.__yFart = -self.maxSpeed
        else:
            self.__yFart = value

    def set_pos(self, x, y):
        self.xPos = np.array([x - self.radius, x + self.radius])
        self.yPos = np.array([y - self.radius, y + self.radius])

    def set_gravity(self, gravity):
        self.yAcc = gravity

    def if_hit_wall(self, left_wall, right_wall, top_wall, bot_wall, elastic=False):
        if self.xPos[0] <= left_wall or right_wall <= self.xPos[1]:
            if self.xPos[0] <= left_wall:
                self.xPos = np.array([left_wall, left_wall + 2 * self.radius])
            elif right_wall <= self.xPos[1]:
                self.xPos = np.array([right_wall - 2 * self.radius, right_wall])
            self.xFart *= -self.bounciness
        if self.yPos[0] <= top_wall:
            self.yPos = np.array([top_wall, top_wall + 2 * self.radius])
            self.yFart *= -self.bounciness
        if bot_wall <= self.yPos[1]:
            self.yPos = np.array([bot_wall - 2 * self.radius, bot_wall])
            if elastic:
                self.yFart *= -1
            else:
                self.yFart *= -self.bounciness
            self.isgrounded = True
        else:
            self.isgrounded = False

    def calculate_pos(self, timestep, luftmotstand, gravitasjon):
        fart = math.sqrt(self.xFart ** 2 + self.yFart ** 2)
        self.xAcc = -luftmotstand * fart * self.xFart
        self.yAcc = gravitasjon - luftmotstand * fart * self.yFart
        self.xFart += self.xAcc * timestep
        self.yFart += self.yAcc * timestep
        self.xPos += self.xFart * timestep
        self.yPos += self.yFart * timestep

    def draw(self):
        self.canvas.coords(self.gui, self.xPos[0], self.yPos[0], self.xPos[1], self.yPos[1])

    def add_force(self, event, force=50):
        if type(event) is str:
            button = str(event).lower()
        else:
            button = str(event.char).lower()
        try:
            force = float(force)
        except ValueError:
            raise ValueError(f"{round(force, 4)} is not a number...")
        akselerasjon = force / self.masse
        if button == "a":
            self.xFart -= akselerasjon
        elif button == "d":
            self.xFart += akselerasjon
        elif button == "w":
            self.yFart -= akselerasjon
        elif button == "s":
            self.yFart += akselerasjon

    def add_force_by_vector(self, vector):
        # print(f"Old: ({self.xFart},{self.yFart})")
        self.add_force("d", vector[0]/30)
        self.add_force("w", vector[1]/30)
        # print(f"New: ({self.xFart},{self.yFart})")
        # print(f"{vector}")

    def update_isgrounded(self, ground):
        if self.yPos[1] < ground:
            self.isgrounded = False
        else:
            self.isgrounded = True

    def inside(self, x, y, radius=0):
        katet1 = self.xMidtPos - x
        katet2 = self.yMidtPos - y
        hypotenus = math.sqrt(katet1 ** 2 + katet2 ** 2)
        hypotenus_corrected = radius + self.radius
        hyp_difference = hypotenus_corrected / hypotenus
        # print([katet1 * hyp_difference, katet2 * hyp_difference])
        # vinkel = math.acos(katet1 / hypotenus)
        # print(vinkel)
        if hypotenus < hypotenus_corrected:
            iscolliding = True
        else:
            iscolliding = False
        return iscolliding, [katet1 * hyp_difference, katet2 * hyp_difference], hypotenus_corrected

    def ball_collision(self, ball):
        iscolliding, kateter, hypotenus = self.inside(ball.xMidtPos, ball.yMidtPos, ball.radius)
        if iscolliding:
            self.xMidtPos = ball.xMidtPos + kateter[0]
            self.yMidtPos = ball.yMidtPos + kateter[1]
            xFart_temp = self.xFart
            yFart_temp = self.yFart
            xFart_temp_ball = ball.xFart
            yFart_temp_ball = ball.yFart
            if xFart_temp == 0:
                xFart_temp += 0.0001
            if yFart_temp == 0:
                yFart_temp += 0.0001
            b_old = ((ball.xMidtPos - self.xMidtPos) ** 2) / \
                (math.sqrt((ball.xMidtPos - self.xMidtPos) ** 2 + (ball.yMidtPos - self.yMidtPos) ** 2) * abs(
                    (ball.xMidtPos - self.xMidtPos)))
            alfa2 = math.atan((ball.yMidtPos - self.yMidtPos) / (ball.xMidtPos - self.xMidtPos))
            alfa2_old = math.acos(b_old)
            # print(f"alfa2: {math.degrees(alfa2_old)} = {math.degrees(alfa2)}")
            alfa1_old = math.acos((xFart_temp ** 2) / (math.sqrt(xFart_temp ** 2 + yFart_temp ** 2) * abs(xFart_temp)))
            alfa1 = math.atan(yFart_temp / xFart_temp)
            alfa3 = math.pi - alfa1 - alfa2
            # print(f"alfa1: {math.degrees(alfa1_old)} = {math.degrees(alfa1)}")
            a = math.sqrt(xFart_temp ** 2 + yFart_temp ** 2) * math.sin(alfa3)
            px = a * math.sin(alfa2)
            py = a * math.cos(alfa2)
            if kateter[0] >= 0:
                xdir = 1
            else:
                xdir = -1
            if kateter[1] >= 0:
                ydir = -1
            else:
                ydir = 1
            self_force = np.array([xdir * abs(px - self.xMidtPos), ydir * abs(py + self.yMidtPos)])
            ball_force = -self_force
            self.add_force_by_vector(self_force)
            ball.add_force_by_vector(ball_force)
            # self_addedforce = - self_force + (+ self_force + self_force * ball.bounciness) / ball.masse
            # self.add_force_by_vector(self_addedforce)
            # ball.add_force_by_vector(self.masse / self.masse ** 2 * (- self_force - self_addedforce))
            # self.xFart = (ball.masse * ball.xFart) / self.masse
            # self.yFart = (ball.masse * ball.yFart) / self.masse
            # ball.xFart = (self.masse * self.xFart) / ball.masse
            # ball.yFart = (self.masse * self.yFart) / ball.masse


class Gui:
    def __init__(self):
        self.hovedvindu = tkinter.Tk()
        self.W = 1080
        self.H = 720
        self.canvas = tkinter.Canvas(self.hovedvindu, width=self.W, height=self.H)
        self.canvas.grid(column=0, row=0)

        self.topleft = (3, 3)
        self.canvas.create_rectangle(self.topleft[0], self.topleft[1], self.W, self.H)

        self.lasttime = time.time()
        self.timestep = time.time() - self.lasttime

        self.LUFTMOTSTAND = 0.0005
        self.GRAVITASJON = 700

        self.ball = Ball(self.canvas, [self.W / 2, self.H / 2], self.W * 0.025)
        self.ball.set_gravity(self.GRAVITASJON)

        self.more_balls = []
        self.ball_added = False

        self.max_balls = 100

        self.all_balls = [self.ball]

        self.keys = {}

        for button in "wasd ":
            self.keys[button] = False
            self.canvas.bind_all(f"<KeyPress-{button}>", lambda x: self.start_pressed_key(x))
            self.canvas.bind_all(f"<KeyRelease-{button}>", lambda x: self.stop_pressed_key(x))

        self.canvas.bind("<ButtonPress-1>", self.left_click)
        self.canvas.bind("<ButtonRelease-1>", self.drop_ball)
        self.canvas.bind("<Motion>", self.update_mousepos)
        self.mousepos = [0, 0]
        self.holded_ball = None

        self.hovedvindu.after(15, self.move_ball)

        tkinter.mainloop()

    def move_ball(self):
        self.timestep = time.time() - self.lasttime
        self.lasttime = time.time()
        self.movement()
        ballnr = 0
        for ball in self.all_balls:
            ballnr += 1
            if ball == self.holded_ball:
                self.holding_ball()
            else:
                ball.calculate_pos(self.timestep, self.LUFTMOTSTAND, self.GRAVITASJON)
            # ball.if_hit_wall(self.topleft[0], self.W, self.topleft[1], self.H)
            self.ball_collision(ball)
            ball.if_hit_wall(self.topleft[0], self.W, self.topleft[1], self.H)
            ball.draw()
        self.hovedvindu.after(15, self.move_ball)

    def start_pressed_key(self, key):
        self.keys[key.char] = True

    def stop_pressed_key(self, key):
        self.keys[key.char] = False

    def movement(self):
        for key in "asd":
            if self.keys[key]:
                self.ball.add_force(key, 20)
        if self.keys[" "]:
            self.ball.update_isgrounded(self.H)
            if self.ball.isgrounded:
                self.ball.add_force("w", 200)
                self.ball.isgrounded = False

    def left_click(self, event):
        for ball in self.all_balls:
            if ball.inside(event.x, event.y)[0]:
                self.holded_ball = ball
                self.holded_ball.xFart = 0
                self.holded_ball.yFart = 0
                return
        self.add_ball(event)

    def add_ball(self, event):
        # size = (0.005 + random.random() * 0.01) * self.W
        size = self.W * 0.025
        colors = ["blue", "yellow", "green", "orange", "purple"]
        random.shuffle(colors)
        self.holded_ball = Ball(self.canvas, [event.x, event.y], size, color=colors[0])
        self.more_balls.insert(1, self.holded_ball)
        self.all_balls.insert(1, self.holded_ball)
        if len(self.all_balls) > self.max_balls:
            removed_ball = self.more_balls.pop()
            self.all_balls.pop()
            self.canvas.delete(removed_ball.gui)
        self.holded_ball.set_gravity(self.GRAVITASJON)
        self.ball_added = True

    def holding_ball(self):
        self.holded_ball.set_pos(self.mousepos[0], self.mousepos[1])

    def drop_ball(self, event):
        self.ball_added = False
        self.holded_ball = None

    def update_mousepos(self, event):
        self.mousepos = [event.x, event.y]

    def ball_collision(self, ball: Ball):
        for ball2 in self.all_balls:
            if ball == ball2:
                continue
            else:
                if ball == self.ball and ball.yPos[1] < ball2.yPos[0] + ball2.radius * 0.8:
                    ball.isgrounded = True
                ball.ball_collision(ball2)


if __name__ == '__main__':
    gui = Gui()
