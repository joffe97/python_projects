import tkinter
import math


class Number:
    def __init__(self, system, number, userset=False):
        self.canvas: tkinter.Canvas = system.canvas
        self.number = number
        self.drawing: tkinter.Canvas.create_text = None
        self.userset = userset

    def draw(self, x_cor, y_cor, size):
        if self.userset:
            color = "gray"
        else:
            color = "black"
        self.drawing = self.canvas.create_text(x_cor, y_cor, text=str(self.number), font=f"Arial {size} bold",
                                               fill=color)

    def remove(self):
        self.canvas.delete(self.drawing)


class Route:
    def __init__(self, system, side_length: int, coords: tuple, column, row):
        self.system = system
        self.canvas: tkinter.Canvas = system.canvas
        self.side_length = side_length
        self.x_coord = coords[0]
        self.y_coord = coords[1]
        self.x = column
        self.y = row
        self.drawing = []
        self.outline = None
        self.number: Number = None

    def set_number(self, number: int, isuser=False):
        self.number = Number(self.system, number, isuser)
        self.number.draw(self.x_coord, self.y_coord, self.side_length//2)

    def set_number_if_allowed(self, number, isuser=False):
        if self.number is None or self.number.userset or not isuser:
            if self.number is not None:
                self.number.remove()
            self.set_number(number, isuser)

    def remove_number(self):
        self.number.remove()
        self.number = None

    def remove_number_if_allowed(self, isuser=False):
        if self.number is None:
            return
        elif not isuser or self.number.userset:
            self.remove_number()

    def remove_outline(self):
        self.canvas.delete(self.outline)
        self.outline = None

    def draw_new(self, color1="#1d1d1d", color2="#28201d", fill="#1a1a1a", width=1):
        canvas = self.canvas
        half_route = self.side_length / 2
        canvas.create_rectangle(self.x_coord - half_route - width, self.y_coord - half_route - width,
                                self.x_coord + half_route - width, self.y_coord + half_route - width,
                                outline=color2, fill=fill, width=width)
        if color1:
            canvas.create_rectangle(self.x_coord - half_route * 0.8, self.y_coord - half_route * 0.8,
                                    self.x_coord + half_route * 0.8, self.y_coord + half_route * 0.8,
                                    outline=color1, width=1)

    def draw_outline(self, color: str = "#750000"):
        half_route = self.side_length / 2
        x_coord = self.x_coord
        y_coord = self.y_coord
        self.outline = self.canvas.create_rectangle(x_coord - half_route, y_coord - half_route,
                                                    x_coord + half_route, y_coord + half_route,
                                                    outline=color, width=3)

    def __str__(self):
        return f"x:{self.x+1}, y:{self.y+1}"


class Grid:
    def __init__(self, system, columns, rows, routestyle=0, width=1):
        self.system = system
        self.canvas: tkinter.Canvas = system.canvas
        self.columns = columns
        self.rows = rows
        self.route_side = int((self.canvas.winfo_width()-1) / columns)
        self.routestyle = routestyle
        self.width = width

        self.grid = self.create_grid()
        self.draw_all_routes()

    def create_grid(self):
        route_side = self.route_side
        half_route_side = int(route_side / 2)
        grid = []
        for column in range(self.columns):
            column_list = []
            x_coord = route_side * column + half_route_side + 3
            for row in range(self.rows):
                y_coord = route_side * row + half_route_side + 3
                column_list.append(Route(self.system, route_side, (x_coord, y_coord), column, row))
            grid.append(column_list)
        self.resize_canvas_after_grid()
        return grid

    def draw_all_routes(self):
        if self.routestyle == 0:
            color1 = None
            color2 = "black"
            fill = None
        else:
            color1 = "#1d1d1d"
            color2 = "#28201d"
            fill = "#1a1a1a"
        for row in self.grid:
            for route in row:
                route.draw_new(color1, color2, fill, width=self.width)

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

    def get_closest_route(self, x_cor, y_cor):
        closest_dist = 0
        for row in self.grid:
            for route in row:
                dist = math.sqrt((route.x_coord - x_cor) ** 2 + (route.y_coord - y_cor) ** 2)
                if closest_dist == 0:
                    closest_route = route
                    closest_dist = dist
                else:
                    if dist < closest_dist:
                        closest_route = route
                        closest_dist = dist
        return closest_route

    def resize_canvas_after_grid(self):
        width = self.columns * self.route_side
        height = self.rows * self.route_side
        self.canvas.config(width=width, height=height)
