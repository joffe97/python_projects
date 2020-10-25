import tkinter
import funcs
import time
import random


class Route:
    def __init__(self, canvas, side_length: int, coords: tuple, column, row):
        self.canvas: tkinter.Canvas = canvas
        self.side_length = side_length
        self.x_coord = coords[0]
        self.y_coord = coords[1]
        self.x = column
        self.y = row
        self.form: Form = None
        self.drawing = []
        self.outline = None

    def add_form(self, form):
        self.form = form
        self.draw_form()

    def remove_form(self):
        self.form = None
        for drawing in self.drawing:
            self.canvas.delete(drawing)
        self.drawing = []

    def remove_outline(self):
        self.canvas.delete(self.outline)
        self.outline = None

    def draw_new(self, color1="#1d1d1d", color2="#28201d", fill="#1a1a1a"):
        canvas = self.canvas
        half_route = self.side_length / 2
        canvas.create_rectangle(self.x_coord - half_route, self.y_coord - half_route,
                                self.x_coord + half_route, self.y_coord + half_route,
                                outline=color2, fill=fill, width=1)
        canvas.create_rectangle(self.x_coord - half_route * 0.8, self.y_coord - half_route * 0.8,
                                self.x_coord + half_route * 0.8, self.y_coord + half_route * 0.8,
                                outline=color1, width=1)

    def draw_form(self):
        half_route = self.side_length / 2
        x_coord = self.x_coord
        y_coord = self.y_coord
        self.drawing.append(self.canvas.create_rectangle(x_coord - half_route, y_coord - half_route,
                                                         x_coord + half_route, y_coord + half_route,
                                                         outline=self.form.colors[1], fill=self.form.colors[0],
                                                         width=0))
        self.drawing.append(self.canvas.create_rectangle(x_coord - (half_route * 0.6), y_coord - (half_route * 0.6),
                                                         x_coord + (half_route * 0.6), y_coord + (half_route * 0.6),
                                                         outline=self.form.colors[0], fill=self.form.colors[1],
                                                         width=1))

    def draw_outline(self, color: str = "#750000"):
        half_route = self.side_length / 2
        x_coord = self.x_coord
        y_coord = self.y_coord
        self.outline = self.canvas.create_rectangle(x_coord - half_route, y_coord - half_route,
                                                    x_coord + half_route, y_coord + half_route,
                                                    outline=color, width=3)


class Grid:
    def __init__(self, system, canvas, columns, rows):
        self.system: System = system
        self.canvas: tkinter.Canvas = canvas
        self.columns = columns
        self.rows = rows
        self.route_side = int((self.canvas.winfo_width()-1) / columns)
        self.grid = self.create_grid()
        self.draw_all_routes()

    def create_grid(self):
        route_side = self.route_side
        half_route_side = int(route_side / 2)
        grid = []
        for column in range(self.columns):
            column_list = []
            x_coord = route_side * column + half_route_side + 2
            for row in range(self.rows):
                y_coord = route_side * row + half_route_side + 2
                column_list.append(Route(self.canvas, route_side, (x_coord, y_coord), column, row))
            grid.append(column_list)
        self.resize_canvas_after_grid()
        return grid

    def draw_all_routes(self):
        for row in self.grid:
            for route in row:
                route.draw_new()

    def get_route(self, x, y):
        if x < 0 or y < 0:
            raise IndexError("Arguments can't be lower than 0")
        route: Route = self.grid[x][y]
        return route

    def get_row(self, row):
        row_list = []
        for column in range(self.columns):
            row_list.append(self.get_route(column, row))
        return row_list

    def is_full_row(self, row):
        for route in self.get_row(row):
            if route.form is None or route.form == self.system.current_form:
                return False
        return True

    def move_route(self, route: Route, direction=(0, 1)):
        route_under = self.get_route(route.x + direction[0], route.y + direction[1])
        route_under.add_form(route.form)
        route.remove_form()

    def resize_canvas_after_grid(self):
        width = self.columns * self.route_side
        height = self.rows * self.route_side
        self.canvas.config(width=width, height=height)


class Form:
    def __init__(self, system, grid, form: int, make_route=True):
        self.system: System = system
        self.grid: Grid = grid
        self.form = form
        self.colors = self.set_color()
        self.__main_route: Route = None
        self.other_routes = []
        if self.form == 1:
            self.__rotation = 2
        else:
            self.__rotation = 0
        self.outlines = []

        if make_route:
            self.make_main_route()

    @property
    def rotation(self):
        return self.__rotation

    @rotation.setter
    def rotation(self, value):
        old_rotation = self.rotation
        first_pos = self.main_route
        try:
            if self.form == 4:
                value = 0
            else:
                if value < 0:
                    value = 4 + value
                elif value > 3:
                    value = 4 - value
            self.__rotation = value
            if self.form == 1:
                if value == 0:
                    self.move((-1, 0))
                elif value == 1:
                    self.move((0, -1))
                elif value == 2:
                    self.move((1, 0))
                elif value == 3:
                    self.move((0, 1))
            self.update_other_routes()
        except IndexError:
            old_xpos = self.main_route.x
            if not self.is_routes_relative_available((-1, 0)):
                self.move_right()
            elif not self.is_routes_relative_available((1, 0)):
                self.move_left()
            if self.main_route.x == old_xpos:
                self.rotation = old_rotation
                self.main_route = first_pos

    @property
    def main_route(self):
        return self.__main_route

    @main_route.setter
    def main_route(self, value):
        try:
            self.remove_from_routes()
            self.__main_route = value
        except AttributeError:
            self.__main_route = value
        self.update_other_routes()
        self.add_to_routes()
        # self.routes_from_obstacle((0, -1))

    def all_routes(self):
        return [self.main_route] + self.other_routes

    def set_color(self):
        if self.form == 1:
            maincolor = "#00ffe5"
        elif self.form == 2:
            maincolor = "#0800ff"
        elif self.form == 3:
            maincolor = "#ffb300"
        elif self.form == 4:
            maincolor = "#ffee00"
        elif self.form == 5:
            maincolor = "#6fff00"
        elif self.form == 6:
            maincolor = "#ff00ae"
        elif self.form == 7:
            maincolor = "#ff0000"
        else:
            raise ValueError("Couldn't set valuecolor")
        darker_color = funcs.make_color_darker(maincolor, 0.15)
        return tuple([maincolor, darker_color])

    def make_main_route(self, main_route_pos: tuple = (4, 1)):
        grid = self.grid
        if self.form == 1:
            main_route = grid.get_route(main_route_pos[0], main_route_pos[1] - 1)
        else:
            main_route = grid.get_route(main_route_pos[0], main_route_pos[1])
        main_route.form = self
        self.main_route = main_route

    def update_other_routes(self):
        for route in self.other_routes:
            route.remove_form()
            route.remove_outline()
        self.other_routes = []
        grid = self.grid
        rotation = self.rotation
        main_x = self.main_route.x
        main_y = self.main_route.y
        if self.form == 1:
            one = (1, 0)
            two = (-1, 0)
            three = (-2, 0)
        elif self.form == 2:
            one = (-1, 0)
            two = (-1, -1)
            three = (1, 0)
        elif self.form == 3:
            one = (-1, 0)
            two = (1, 0)
            three = (1, -1)
        elif self.form == 4:
            one = (0, -1)
            two = (1, -1)
            three = (1, 0)
        elif self.form == 5:
            one = (-1, 0)
            two = (0, -1)
            three = (1, -1)
        elif self.form == 6:
            one = (-1, 0)
            two = (1, 0)
            three = (0, -1)
        elif self.form == 7:
            one = (-1, -1)
            two = (0, -1)
            three = (1, 0)
        else:
            raise ValueError("Couldn't update the other routes")

        for route_diff in (one, two, three):
            if rotation == 0:
                route = grid.get_route(main_x + route_diff[0], main_y + route_diff[1])
            elif rotation == 1:
                route = grid.get_route(main_x - route_diff[1], main_y + route_diff[0])
            elif rotation == 2:
                route = grid.get_route(main_x - route_diff[0], main_y - route_diff[1])
            elif rotation == 3:
                route = grid.get_route(main_x + route_diff[1], main_y - route_diff[0])
            else:
                raise ValueError(f"{self.rotation} is an unavailable rotation")
            if route.form is not None:
                raise IndexError("Route is not empty")
            self.other_routes.append(route)
            route.add_form(self)
        self.update_outline()

    def routes_from_obstacle(self, direction: tuple):
        rows = 0
        columns = 0
        while self.is_routes_relative_available((direction[1] + columns, direction[0] + rows)):
            rows += direction[1]
            columns += direction[0]
        # print(f"({columns}, {rows})")
        return tuple([columns, rows])

    def update_outline(self):
        if self.grid != self.system.grid:
            return
        self.remove_outline()
        lines = 0
        while self.is_routes_relative_available((0, lines)):
            lines += 1
        routes_under = lines - 1
        for route in self.all_routes():
            outline_route = self.grid.get_route(route.x, route.y + routes_under)
            self.outlines.append(outline_route)
            outline_route.draw_outline()

    def remove_outline(self):
        for outline_routes in self.outlines:
            outline_routes.remove_outline()
        self.outlines = []

    def add_to_routes(self):
        for route in self.all_routes():
            route.add_form(self)

    def remove_from_routes(self):
        for route in self.all_routes():
            route.remove_form()

    def move(self, direction: tuple):
        if not self.is_routes_relative_available(direction):
            return
        self.main_route = self.grid.get_route(self.main_route.x + direction[0], self.main_route.y + direction[1])

    def move_down(self):
        self.main_route = self.grid.get_route(self.main_route.x, self.main_route.y + 1)

    def move_left(self):
        if not self.is_routes_relative_available((-1, 0)):
            return
        self.main_route = self.grid.get_route(self.main_route.x - 1, self.main_route.y)

    def move_right(self):
        if not self.is_routes_relative_available((1, 0)):
            return
        self.main_route = self.grid.get_route(self.main_route.x + 1, self.main_route.y)

    def move_to_lowest(self):
        while self.is_routes_relative_available():
            self.move_down()

    def rotate(self, way: str):
        if way == "left":
            self.rotation -= 1
        elif way == "right":
            self.rotation += 1

    def is_routes_relative_available(self, direction=(0, 1)):
        for route in self.all_routes():
            try:
                route_under = self.grid.get_route(route.x + direction[0], route.y + direction[1])
            except IndexError:
                return False
            if route_under.form is not None and route_under.form is not self:
                return False
        return True


class System:
    def __init__(self, gui):
        self.gui: Gui = gui
        self.mainwindow: tkinter.Tk = gui.mainwindow
        self.canvas: tkinter.Canvas = gui.canvas
        self.grid: Grid = None

        self.canvas_upcoming: tkinter.Canvas = gui.canvas_upcoming
        self.grid_upcoming: Grid = None

        self.canvas_holding: tkinter.Canvas = gui.canvas_holding
        self.grid_holding: Grid = None

        self.holding = None
        self.upcoming_forms = {}
        self.idle_forms = []
        self.current_form: Form = None
        self.current_time = 0
        self.force_time = 0
        self.time_started = 0
        self.is_game_over = True
        self.is_playing = False
        self.first_game = True
        self.name = "Player"
        self.__speed = 0
        self.__score = 0
        self.__combo = 0
        self.switched_holding = False
        self.highscores = []

        self.setup()

    @property
    def speed(self):
        return self.__speed

    @speed.setter
    def speed(self, value):
        if value > 10:
            self.__speed = 10
        else:
            self.__speed = value

    @property
    def score(self):
        return self.__score

    @score.setter
    def score(self, value):
        self.gui.score_var.set(f"Score: {value}")
        self.__score = value

    @property
    def combo(self):
        return self.__combo

    @combo.setter
    def combo(self, value):
        self.__combo = value
        if value == 0:
            self.gui.combo_label["fg"] = "#1a1a1a"
        else:
            self.gui.combo_var.set(f"{value}x ")
            color_intensity = int(value * 25 + 100)
            if color_intensity > 255:
                color_intensity = 255
            self.gui.combo_label["fg"] = funcs.rgb_to_hexcolor((color_intensity, 0, 0))

    def ask_for_name(self):
        self.gui.score_label["fg"] = "#1a1a1a"
        name = tkinter.StringVar()
        if self.name != "Player":
            name.set(self.name)
        name.trace("w", lambda x, y, z: self.limit_stringvar(stringvar=name, limit=10))
        self.gui.name_box = tkinter.Entry(self.mainwindow, textvariable=name, width=10,
                                          font=f"Aharoni {int(self.canvas.winfo_width() / 17)} bold")
        self.gui.name_box.grid(column=2, row=0, sticky=tkinter.W)
        self.gui.name_label = tkinter.Label(self.mainwindow, text="Name: ",
                                            font=f"Aharoni {int(self.canvas.winfo_width() / 17)} bold")
        self.gui.name_label.grid(column=1, row=0, sticky=tkinter.E)
        self.gui.name_label["bg"] = "#1a1a1a"
        self.gui.name_label["fg"] = "white"
        self.game_over()

    def limit_stringvar(self, stringvar: tkinter.StringVar, limit=10):
        if self.is_playing:
            return
        if len(stringvar.get()) > limit:
            stringvar.set(stringvar.get()[:limit])
        if len(stringvar.get()) > 0:
            self.name = stringvar.get().capitalize()
        else:
            self.name = "Player"

    def setup(self):
        self.grid: Grid = Grid(self, self.canvas, 10, 20)
        self.grid_upcoming: Grid = Grid(self, self.canvas_upcoming, 5, 13)
        self.grid_holding: Grid = Grid(self, self.canvas_holding, 4, 4)
        self.upcoming_forms = {0: None, 1: None, 2: None, 3: None}
        self.idle_forms = []
        self.current_form: Form = None
        self.current_time = time.time()
        self.force_time = time.time()
        self.is_game_over = False
        self.is_playing = False
        self.speed = 0
        self.score = 0
        self.combo = 0
        self.switched_holding = False
        self.highscores = []

        self.load_high_scores()
        self.gui.gameover_label.lower(self.canvas)
        if self.first_game:
            self.first_game = False
            self.ask_for_name()
        else:
            self.gui.gameover_label_2.lower(self.canvas)
            self.is_playing = True
            self.gui.score_label["fg"] = "orange"
            for k in range(4):
                self.add_random_form_to_upcoming(k)
            self.add_random_form()
            self.run()

    def run(self):
        if self.is_game_over:
            self.is_playing = False
            self.start_game_over()
        else:
            if not self.current_form.is_routes_relative_available():
                self.force_time = time.time()
            else:
                self.force_time = time.time() - 10

            if funcs.time_has_went_by(self.gui.last_pressed_key["a"], 100) and self.gui.is_pressing_key("a"):
                self.gui.last_pressed_key["a"] = time.time()
                self.current_form.move_left()
            if funcs.time_has_went_by(self.gui.last_pressed_key["d"], 100) and self.gui.is_pressing_key("d"):
                self.gui.last_pressed_key["d"] = time.time()
                self.current_form.move_right()
            if (funcs.time_has_went_by(self.gui.last_pressed_key["s"], 75 / (1 + self.speed * 0.5)) and
                self.gui.is_pressing_key("s") and funcs.time_has_went_by(self.force_time, 100 / 1 + self.speed)) or \
                    funcs.time_has_went_by(self.current_time, 1000 / (1 + self.speed)):
                self.move_down()

            self.mainwindow.after(25, self.run)

    def move_down(self):
        self.gui.last_pressed_key["s"] = time.time()
        self.current_time = time.time()
        if self.current_form.is_routes_relative_available():
            self.current_form.move((0, 1))
        else:
            try:
                self.add_form_from_upcoming()
                self.remove_full_rows()
                self.speed += 0.08
                self.switched_holding = False
            except IndexError:
                self.is_game_over = True

    def add_form(self, form: int):
        if self.current_form is not None:
            self.current_form.remove_outline()
            self.idle_forms.append(self.current_form)
        try:
            self.current_form = Form(self, self.grid, form)
        except IndexError:
            self.is_game_over = True

    def add_random_form(self):
        self.add_form(random.randint(1, 7))

    def add_random_form_to_upcoming(self, place: int = 3):
        formtype = random.randint(1, 7)
        if self.upcoming_forms[place] is not None:
            raise KeyError("Upcoming place is containing a form")
        else:
            form: Form = Form(self, self.grid_upcoming, formtype, make_route=False)
            self.upcoming_forms[place] = form
            form.make_main_route((2, 2 + place * 3))

    def move_upcoming_forms_up(self):
        for index in range(1, 4):
            form = self.upcoming_forms[index]
            form.move((0, -3))
            self.upcoming_forms[index - 1] = form
            self.upcoming_forms[index] = None

    def add_form_from_upcoming(self):
        form = self.upcoming_forms[0]
        form.remove_from_routes()
        self.upcoming_forms[0] = None
        self.move_upcoming_forms_up()
        self.add_random_form_to_upcoming()
        self.add_form(form.form)

    def add_form_to_holding(self):
        holding_type = self.current_form.form
        self.holding = Form(self, self.grid_holding, holding_type, make_route=False)
        self.holding.make_main_route((1, 2))
        self.current_form.remove_from_routes()

    def switch_holding(self):
        if self.switched_holding:
            return
        self.switched_holding = True
        if self.holding is None:
            self.add_form_to_holding()
            self.add_form_from_upcoming()
        else:
            holding_form: Form = self.holding
            holding_form.remove_from_routes()
            self.add_form_to_holding()
            self.add_form(holding_form.form)

    def remove_full_rows(self):
        grid = self.grid
        movedown_by = 0
        for row_index in range(grid.rows - 1, -1, -1):
            if grid.is_full_row(row_index):
                movedown_by += 1
                row = grid.get_row(row_index)
                for route in row:
                    route.remove_form()
            if movedown_by:
                row = grid.get_row(row_index)
                for route in row:
                    if route.form is None or route.form == self.current_form:
                        continue
                    grid.move_route(route, (0, movedown_by))
        if movedown_by != 0:
            self.add_score(movedown_by)
        else:
            self.combo = 0

    def add_score(self, lines_removed):
        self.combo += 1
        self.score += int((lines_removed ** 1.65) * (self.combo ** 1.2))

    def start_game_over(self):
        self.gui.gameover_var.set(f"GAME OVER!\nYour score: {self.score}")
        self.gui.gameover_label.lift(self.canvas)
        self.gui.gameover_label_2.lift(self.canvas)
        self.save_high_score()
        self.ask_for_name()

    def game_over(self):
        if self.gui.is_pressing_key("enter"):
            self.gui.name_label.destroy()
            self.gui.name_box.destroy()
            self.setup()
        else:
            self.mainwindow.after(25, self.game_over)

    def save_high_score(self):
        with open("highscores.txt", "a+") as file:
            file.write(f"{self.name};{self.score}\n")

    def load_high_scores(self):
        top5 = []
        with open("highscores.txt", "r") as file:
            first_line = file.readline()
            first_line = first_line.strip("\n")
            first_line = first_line.split(";")
            top5.append(first_line)
            for line in file:
                line = line.strip("\n")
                words = line.split(";")
                score = int(words[1])
                if score > int(top5[-1][1]) or len(top5) < 5:
                    name_in_list = False
                    for top_entry in top5:
                        if words[0] == top_entry[0]:
                            if score > int(top_entry[1]):
                                top_entry[1] = str(score)
                            name_in_list = True
                            break
                    if not name_in_list:
                        top5.append(words)
                    top5.sort(reverse=True, key=lambda toplist: int(toplist[-1]))
        string = "\n"
        for index, words in enumerate(top5, start=1):
            if index > 5:
                break
            scorelength = len(f"{words[0]}{words[1]}")
            spaces = " " * (12 - scorelength - len(f"{index}"))
            string += f"\n{index}.{words[0]}{spaces}{words[1]}\n"
        self.gui.highscores_var.set(string)


class Gui:
    def __init__(self):
        self.mainwindow = tkinter.Tk()
        self.mainwindow.title("Tetris")
        self.mainwindow.iconbitmap("icon.ico")

        self.canvas_width = 300
        self.canvas_width = self.mainwindow.winfo_screenheight() * 0.45
        self.canvas_height = self.canvas_width * 2

        self.score_var = tkinter.StringVar()
        self.score_var.set(" Score: 0")
        self.score_label = tkinter.Label(self.mainwindow, textvariable=self.score_var,
                                         font=f"Aharoni {int(self.canvas_width / 17)} bold", anchor=tkinter.NW)
        self.score_label.grid(column=1, row=0, sticky=(tkinter.W, tkinter.E))
        self.score_label.configure(bg="#1a1a1a", fg="orange")

        self.combo_var = tkinter.StringVar()
        self.combo_var.set("0x ")
        self.combo_label = tkinter.Label(self.mainwindow, textvariable=self.combo_var,
                                         font=f"Aharoni {int(self.canvas_width / 17)} bold", anchor=tkinter.NE)
        self.combo_label.grid(column=2, row=0, sticky=(tkinter.W, tkinter.E))
        self.combo_label.configure(bg="#1a1a1a", fg="#1a1a1a")

        self.canvas = tkinter.Canvas(self.mainwindow, width=self.canvas_width, height=self.canvas_height)
        self.canvas.grid(column=1, row=1, columnspan=2, rowspan=4)
        # self.canvas.create_rectangle(0, 0, self.canvas_width + 10, self.canvas_height + 10, fill="#1a1a1a")

        self.canvas_upcoming = tkinter.Canvas(self.mainwindow, width=self.canvas_width * 0.4 * 0.8,
                                              height=self.canvas_height * 0.515 * 0.8)
        self.canvas_upcoming.grid(column=3, row=1, rowspan=2, sticky=tkinter.N)

        self.canvas_holding = tkinter.Canvas(self.mainwindow, width=self.canvas_width * 0.4 * 0.8,
                                             height=self.canvas_height * 0.2 * 0.8)
        self.canvas_holding.grid(column=0, row=1, rowspan=4, sticky=tkinter.N)

        self.highscores_var = tkinter.StringVar()
        self.highscores_label = tkinter.Label(self.mainwindow, textvariable=self.highscores_var,
                                              font=f"Consolas {int(self.canvas_width / 34)}", anchor=tkinter.N,
                                              justify=tkinter.LEFT)
        self.highscores_label.grid(column=3, row=3, sticky=tkinter.NW, pady=int(self.canvas_width / 5), padx=4)
        self.highscores_label.configure(bg="#1a1a1a", fg="orange")

        self.highscores_label_2 = tkinter.Label(self.mainwindow, text="HIGHSCORES:",
                                                font=f"Aharoni {int(self.canvas_width / 30)} bold", anchor=tkinter.N,
                                                justify=tkinter.LEFT)
        self.highscores_label_2.grid(column=3, row=3, sticky=tkinter.N, pady=int(self.canvas_width / 5))
        self.highscores_label_2.configure(bg="#1a1a1a", fg="orange")

        self.gameover_var = tkinter.StringVar()
        self.gameover_var.set("GAME OVER!\nYour score: 0")
        self.gameover_label = tkinter.Label(self.mainwindow, textvariable=self.gameover_var,
                                            font=f"Algerian {int(self.canvas_width / 13)} bold")
        self.gameover_label.grid(column=1, row=2, sticky=(tkinter.W, tkinter.E), columnspan=2, padx=2, ipady=5)
        self.gameover_label.configure(bg="#1a1a1a", fg="red")

        self.gameover_label_2 = tkinter.Label(self.mainwindow, text="Press enter\nto play...",
                                              font=f"Algerian {int(self.canvas_width / 16)} bold")
        self.gameover_label_2.grid(column=1, row=3, columnspan=2, padx=2, ipadx=3, ipady=3)
        self.gameover_label_2.configure(bg="#1a1a1a", fg="red")

        self.name_box: any = None
        self.name_label: any = None

        self.fullscreen = False

        self.mainwindow.configure(bg="#1a1a1a")
        self.mainwindow.update()
        self.mainwindow.geometry(f"+{int((self.mainwindow.winfo_screenwidth() - self.mainwindow.winfo_width()) / 2)}"
                                 f"+{int((self.mainwindow.winfo_screenheight() - self.mainwindow.winfo_height()) / 2)}")

        self.canvas.bind_all("<KeyPress>", self.key_pressed)
        self.canvas.bind_all("<KeyRelease>", self.key_released)
        self.key_to_keycode = {"q": 81, "e": 69, "a": 65, "d": 68, "s": 83, "w": 87, " ": 32, "enter": 13, "shift": 16,
                               "f": 70, "esc": 27, "b": 66}
        self.is_pressing_keycode = {}
        for keycode in self.key_to_keycode.values():
            self.is_pressing_keycode[keycode] = False
        self.last_pressed_key = {"s": time.time(), "a": time.time(), "d": time.time()}

        self.toggle_fullscreen()

        self.system = System(self)

        tkinter.mainloop()

    def is_pressing_key(self, key: str):
        keycode = self.key_to_keycode[key]
        return self.is_pressing_keycode[keycode]

    def key_pressed(self, event):
        print(event)
        key = event.keycode
        if key in range(37, 41):
            if key == 37:
                key = 65
            elif key == 38:
                key = 87
            elif key == 39:
                key = 68
            elif key == 40:
                key = 83

        form = self.system.current_form
        for key_entry in self.key_to_keycode.values():
            if key == key_entry and not self.is_pressing_keycode[key_entry]:
                self.is_pressing_keycode[key_entry] = True
                if self.system.is_playing:
                    if key_entry == 87:
                        form.rotate("right")
                    elif key_entry == 32:
                        form.move_to_lowest()
                    elif key_entry == 16:
                        self.system.switch_holding()
                if key_entry == 70:
                    self.toggle_fullscreen()
                if key_entry == 27:
                    self.mainwindow.destroy()

    def key_released(self, event):
        key = event.keycode
        if key in range(37, 41):
            if key == 37:
                key = 65
            elif key == 38:
                key = 87
            elif key == 39:
                key = 68
            elif key == 40:
                key = 83
        for key_entry in self.key_to_keycode.values():
            if key == key_entry:
                self.is_pressing_keycode[key_entry] = False

    def toggle_fullscreen(self):
        if not self.fullscreen:
            self.mainwindow.attributes("-fullscreen", True)
            self.fullscreen = True
            self.canvas_holding.grid(column=0, row=1, rowspan=4, sticky=tkinter.N,
                                     padx=((self.mainwindow.winfo_width() - self.canvas.winfo_width() -
                                            self.canvas_holding.winfo_width() -
                                            self.canvas_upcoming.winfo_width()) * 0.5, 0))
            self.score_label.grid(column=1, row=0, sticky=(tkinter.W, tkinter.E), pady=10)
        else:
            self.mainwindow.attributes("-fullscreen", False)
            self.fullscreen = False
            self.canvas_holding.grid(column=0, row=1, rowspan=4, sticky=tkinter.N, padx=0)
            self.score_label.grid(column=1, row=0, sticky=(tkinter.W, tkinter.E))


if __name__ == '__main__':
    Gui()
