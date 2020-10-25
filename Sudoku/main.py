import utils
import tkinter as tk
import random


class System:
    def __init__(self):
        self.h = self.w = 420
        self.mw = tk.Tk()
        self.canvas = tk.Canvas(self.mw, height=self.h, width=self.w)
        self.canvas.grid(column=1, row=1)
        self.canvas.update()

        self.grid3x3 = utils.Grid(self, 3, 3, width=3)
        self.grid9x9 = utils.Grid(self, 9, 9)

        self.create_random_sudoku()

        self.canvas.bind("<Button-1>", self.choose_to_set)
        self.canvas.bind("<Button-3>", self.remove_as_user)
        self.mw.bind("<Key>", self.keypress)
        # self.mw.bind("<KeyRelease>", self.keyrelease)

        self.pressednum = None

        tk.mainloop()

    def choose_to_set(self, event):
        route = self.grid9x9.get_closest_route(event.x, event.y)
        self.set_num_if_pressedkey(route)

    def keypress(self, event):
        key = event.char
        if ord(key) in range(49, 58):
            self.pressednum = int(key)
        print(self.pressednum)

    def keyrelease(self, event):
        key = event.char
        if ord(key) in range(49, 58):
            self.pressednum = None
        print(self.pressednum)

    def remove_as_user(self, event):
        route = self.grid9x9.get_closest_route(event.x, event.y)
        route.remove_number_if_allowed(isuser=True)

    def set_num_if_pressedkey(self, route):
        if self.pressednum:
            route.set_number_if_allowed(self.pressednum, isuser=True)

    def create_random_sudoku(self):
        with open("sudokus.txt", "r") as f:
            for lines, line in enumerate(f):
                pass
            randomlinenr = random.randint(0, lines)
        with open("sudokus.txt", "r") as f:
            for linenr, line in enumerate(f):
                if linenr == randomlinenr:
                    chosenline = line
                    break
        for index, letter in enumerate(chosenline):
            if index == 81:
                break
            elif letter == ".":
                continue
            try:
                self.grid9x9.get_route(index % 9, index // 9).set_number(int(letter))
            except ValueError:
                continue


if __name__ == '__main__':
    System()
