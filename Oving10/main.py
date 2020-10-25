import tkinter
import kulebane
import math
import random


class System:
    def __init__(self):
        self.integrateInterval = 0.02
        self.animationTimestep = 15

        self.score = 0
        self.newTarget = 0

        self.GRAVITASJON = 100
        self.LUFTMOTSTAND = 0.0003

        self.xWind = (0.5 - random.random()) * 6
        self.yWind = (0.5 - random.random()) * 4
        self.wind = [self.xWind, self.yWind]

        self.tid = 50.0

        self.integrator = kulebane.Integrasjon(self.integrateInterval, self.tid)

        self.windowWidth = 1532
        self.windowHeight = 740

        self.mainwindow = tkinter.Tk()
        self.drawer = tkinter.Canvas(self.mainwindow, width=self.windowWidth, height=self.windowHeight)
        self.drawer.grid(column=0, row=1, columnspan=3, sticky=(tkinter.W, tkinter.E))

        self.windText = tkinter.Label(self.mainwindow, text="")
        self.windXText = ""
        self.windYText = ""

        self.shooterAngle = tkinter.IntVar(self.mainwindow, 40)
        self.shooterStrength = tkinter.IntVar(self.mainwindow, 200)
        self.gamemodeVar = tkinter.IntVar(self.mainwindow, 0)

        self.scoreLabel = tkinter.Label(self.mainwindow, text=f"Score: {self.score}", font="Georgia")
        self.scoreLabel.grid(column=0, row=0, sticky=tkinter.W)

        self.xStartPos = 17 + 35 * math.cos(math.radians(self.shooterAngle.get()))
        self.yStartPos = self.windowHeight - 35 * math.sin(math.radians(self.shooterAngle.get()))
        self.xStartV = 0
        self.yStartV = 0

        self.shots = []
        self.xShotPos = 0
        self.yShotPos = 0

        self.kule = kulebane.BasisKulebane(self.GRAVITASJON)

        self.xTarget = random.random() * ((self.windowWidth / 2) - 30) + self.windowWidth / 2
        self.yTarget = self.windowHeight - 30
        self.mainwindow.attributes('-fullscreen', True)

        self.heightObstacle = random.random() * 300 + 100
        self.widthObstacle = 20 + random.random() * 30
        self.xObstacle = random.random() * ((self.windowWidth / 2) - 150) + 150
        self.yObstacle = self.windowHeight - self.heightObstacle - random.random() * 100

        # Tegner
        self.drawer.create_rectangle(2, 2, self.windowWidth + 1, self.windowHeight + 1, fill="#FFE4E4")  # Window
        self.drawer.create_arc(2, self.windowHeight - 15, 32, self.windowHeight + 15,
                               start=0, extent=180, fill="black")  # Shooter body
        self.gun = self.drawer.create_line(17, self.windowHeight,
                                           17 + 35 * math.cos(math.radians(self.shooterAngle.get())),
                                           self.windowHeight - 35 * math.sin(math.radians(self.shooterAngle.get())),
                                           width=5)  # Gun
        self.target = self.drawer.create_rectangle(self.xTarget, self.yTarget, self.xTarget + 30, self.yTarget + 30, fill="red")
        self.obstacle = self.drawer.create_rectangle(self.xObstacle, self.yObstacle, self.xObstacle + self.widthObstacle,
                                                     self.yObstacle + self.heightObstacle, fill="black")

        # Nederst
        self.strengthSlider = tkinter.Scale(self.mainwindow, from_=100, to=500, orient=tkinter.HORIZONTAL, font="Georgia",
                                            variable=self.shooterStrength)
        self.strengthSlider.grid(column=0, row=2, sticky=(tkinter.W, tkinter.E))
        self.strengthText = tkinter.Label(self.mainwindow, text="STRENGTH", font="Georgia")
        self.strengthText.grid(column=0, row=3)

        self.angleSlider = tkinter.Scale(self.mainwindow, from_=0, to=90, orient=tkinter.HORIZONTAL, font="Georgia",
                                         variable=self.shooterAngle, command=self.move_gun)
        self.angleSlider.grid(column=1, row=2, sticky=(tkinter.W, tkinter.E))
        self.strengthText = tkinter.Label(self.mainwindow, text="ANGLE", font="Georgia")
        self.strengthText.grid(column=1, row=3)

        self.buttons = tkinter.Frame(self.mainwindow)
        self.shootButton = tkinter.Button(self.buttons, text="Shoot!", font="Georgia", command=self.shoot)
        self.shootButton.grid(column=0, row=0, columnspan=1, sticky=tkinter.W)
        self.closeGameButton = tkinter.Button(self.buttons, text="Close game", font="Georgia", command=self.mainwindow.destroy)
        self.closeGameButton.grid(column=1, row=0, sticky=tkinter.E)
        self.buttons.grid(column=2, row=2, columnspan=3, sticky=(tkinter.W, tkinter.E))

        self.gamemodes = tkinter.Frame(self.mainwindow)
        self.basic = tkinter.Radiobutton(self.gamemodes, text="Basic        ", variable=self.gamemodeVar,
                                         value=0, font="Georgia", command=self.hide_wind)
        self.basic.grid(column=0, row=0)
        self.air = tkinter.Radiobutton(self.gamemodes, text="Air Resistance        ", variable=self.gamemodeVar,
                                       value=1, font="Georgia", command=self.hide_wind)
        self.air.grid(column=1, row=0)
        self.windbutton = tkinter.Radiobutton(self.gamemodes, text="Wind", variable=self.gamemodeVar, value=2, font="Georgia",
                                        command=self.show_wind)
        self.windbutton.grid(column=2, row=0)
        self.gamemodes.grid(column=2, row=3, columnspan=3, sticky=(tkinter.W, tkinter.E))

        tkinter.mainloop()

    def shoot(self):
        self.xStartPos = 17 + 35 * math.cos(math.radians(self.shooterAngle.get()))
        self.yStartPos = self.windowHeight - 35 * math.sin(math.radians(self.shooterAngle.get()))

        if self.gamemodeVar.get() == 1:
            self.kule = kulebane.AvaKulebane(self.GRAVITASJON, self.LUFTMOTSTAND)
            self.windText.destroy()
        elif self.gamemodeVar.get() == 2:
            self.kule = kulebane.SuperAvaKulebane(self.GRAVITASJON, self.LUFTMOTSTAND, self.wind)
        else:
            self.kule = kulebane.BasisKulebane(self.GRAVITASJON)
            self.windText.destroy()

        self.xStartV = self.shooterStrength.get() * math.cos(math.radians(self.shooterAngle.get()))
        self.yStartV = -self.shooterStrength.get() * math.sin(math.radians(self.shooterAngle.get()))

        starttilstand = [self.xStartPos, self.yStartPos, self.xStartV, self.yStartV]
        self.integrator.integrer(self.kule, starttilstand)

        self.xShotPos = 0
        self.yShotPos = 0
        self.shots.append(self.drawer.create_oval(self.xShotPos - 5, self.yShotPos - 5, self.xShotPos + 5,
                                                  self.yShotPos + 5, fill="black"))

        self.mainwindow.after(self.animationTimestep, self.move_bullet)

    def move_bullet(self):
        position = next(self.integrator)

        self.xShotPos = position[1]
        self.yShotPos = position[2]
        self.drawer.coords(self.shots[-1], self.xShotPos - 5, self.yShotPos - 5, self.xShotPos + 5, self.yShotPos + 5)
        self.bullet_in_target()
        if position[2] <= self.windowHeight and 0 <= position[1] <= self.windowWidth and \
                not self.bullet_in_obstacle(self.xObstacle, self.yObstacle, self.widthObstacle, self.heightObstacle):
            self.mainwindow.after(self.animationTimestep, self.move_bullet)
            return
        elif self.newTarget:
            self.create_new_target()
            self.newTarget = 0
            self.reset_shots()
            self.create_obstacle()
        self.update_wind()

    def move_gun(self, var):
        self.drawer.coords(self.gun, 17, self.windowHeight, 17 + 35 * math.cos(math.radians(self.shooterAngle.get())),
                           self.windowHeight - 35 * math.sin(math.radians(self.shooterAngle.get())))

    def bullet_in_target(self):
        if self.bullet_in_obstacle(self.xTarget, self.yTarget, 30, 30):
            self.newTarget = 1
            self.drawer.delete(self.target)

    def bullet_in_obstacle(self, x, y, width, height):
        if abs(self.xShotPos - x - width/2) <= width/2 + 5 \
                and abs(self.yShotPos - y - height/2) <= height/2 + 5:
            return True
        else:
            return False

    def create_new_target(self):
        self.xTarget = random.random() * ((self.windowWidth / 2) - 30) + self.windowWidth / 2
        self.yTarget = self.windowHeight - 30
        self.target = self.drawer.create_rectangle(self.xTarget, self.yTarget, self.xTarget + 30, self.yTarget + 30, fill="red")
        self.score += 1
        self.scoreLabel = tkinter.Label(self.mainwindow, text=f"Score: {self.score}", font="Georgia")
        self.scoreLabel.grid(column=0, row=0, sticky=tkinter.W)

    def create_obstacle(self):
        self.heightObstacle = random.random() * 300 + 100
        self.widthObstacle = 20 + random.random() * 30
        self.xObstacle = random.random() * ((self.windowWidth / 2) - 150) + 150
        self.yObstacle = self.windowHeight - self.heightObstacle - random.random() * 100
        self.drawer.coords(self.obstacle, self.xObstacle, self.yObstacle, self.xObstacle + self.widthObstacle,
                           self.yObstacle + self.heightObstacle)

    def reset_shots(self):
        self.xShotPos = -10
        self.yShotPos = -10
        for shot in range(len(self.shots)):
            self.drawer.delete(self.shots[shot])
        self.shots = []

    def show_wind(self):
        if self.xWind < 0:
            self.windXText = "west"
        else:
            self.windXText = "east"
        if self.yWind < 0:
            self.windYText = "down"
        else:
            self.windYText = "up"
        self.windText = tkinter.Label(self.mainwindow, text=f"       WIND: {round(abs(self.xWind))} {self.windXText}, "
                                                            f"{round(abs(self.yWind))} {self.windYText}",
                                      font="Georgia")
        self.windText.grid(column=2, row=0, columnspan=2, sticky=tkinter.E)

    def hide_wind(self):
        self.windText.destroy()

    def update_wind(self):
        if self.gamemodeVar.get() == 2:
            self.xWind = (0.5 - random.random()) * 6
            self.yWind = (0.5 - random.random()) * 4
            self.wind = [self.xWind, self.yWind]
            self.hide_wind()
            self.show_wind()


if __name__ == '__main__':
    gui = System()
