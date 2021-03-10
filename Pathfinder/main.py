import tkinter as tk
import math

from typing import List

from graph import Graph, Node
import time, datetime
from PIL import Image, UnidentifiedImageError
import numpy as np
import c_prgms.dijkstra.dijkstra as dijkstra

SCREEN_RESOLUTION = tuple

AMPLIFY_VAL = 100


class Living:
    def __init__(self, x, y, color):
        self.is_spawned = False if x is None or y is None else True
        self.x = x
        self.y = y
        self.color = color

    @property
    def coords(self):
        return [self.x, self.y]

    @coords.setter
    def coords(self, value):
        if type(value) is not list or len(value) != 2:
            raise ValueError(f"Can't set {value} as coords")
        self.x = value[0]
        self.y = value[1]

    def update_pos(self, x, y):
        self.x = x
        self.y = y

    def move_relative(self, x, y):
        self.update_pos(self.x + x, self.y + y)
        return self.x, self.y

    def get_relative(self, x, y):
        return self.x + x, self.y + y

    def get_from_relative(self, x, y):
        return x - self.x, y - self.y


class Player(Living):
    def __init__(self, x=None, y=None):
        super().__init__(x, y, "green")


class Enemy(Living):
    def __init__(self, x, y):
        super().__init__(x, y, "red")


class Enemies:
    def __init__(self):
        self.enemylist: List[Enemy] = []

    def add(self, enemy: Enemy):
        self.enemylist.append(enemy)

    def remove(self, enemy: Enemy):
        for index, e in enumerate(self.enemylist):
            if e == enemy:
                del self.enemylist[index]
                return True
        return False

    def get_enemy_at_coord(self, x, y):
        for enemy in self.enemylist:
            if enemy.coords == [x, y]:
                return enemy
        return None

    def is_enemy_at_coord(self, x, y):
        for enemy in self.enemylist:
            if enemy.coords == [x, y]:
                return True
        return False

    def get_enemy_coord_list(self):
        coord_list = []
        for enemy in self.enemylist:
            coord_list.append(enemy.coords)
        return coord_list

    def __iter__(self):
        return self.enemylist.__iter__()

    def __len__(self):
        return self.enemylist.__len__()


class Map:
    def __init__(self):
        self.coords = []
        self.pix_size = 0
        self.grid_width = 1
        self._x_len = 0
        self._y_len = 0
        self._x_pix = 0
        self._y_pix = 0
        self.player = Player()
        self.enemies = Enemies()

    @property
    def x_len(self):
        return self._x_len

    @x_len.setter
    def x_len(self, value):
        self._x_len = value
        self._x_pix = value * self.pix_size

    @property
    def y_len(self):
        return self._y_len

    @y_len.setter
    def y_len(self, value):
        self._y_len = value
        self._y_pix = value * self.pix_size

    @property
    def x_pix(self):
        return self._x_pix

    @property
    def y_pix(self):
        return self._y_pix

    def get_map(self, filename):
        try:
            self.get_map_img(filename)
        except UnidentifiedImageError:
            self.get_map_txt(filename)
        self.update_all_sizes()

    def get_map_txt(self, mapfile):
        self.coords = []
        with open(mapfile, "r") as f:
            for y, line in enumerate(f):
                row = []
                for x, item in enumerate(line.split(" ")):
                    item = item.strip("\n ")
                    if item in "AB":
                        if item == "A":
                            self.player = Player(x, y)
                        elif item == "B":
                            self.enemies.add(Enemy(x, y))
                        item = 0
                    try:
                        row.append(int(item) * AMPLIFY_VAL)
                    except ValueError:
                        continue
                self.coords.append(row)

    def get_map_img(self, imgfile):
        image = Image.open(imgfile).convert("L")
        nparray = np.asarray(image)
        nparray = 9 * AMPLIFY_VAL - (nparray * (9 * AMPLIFY_VAL / 255))
        self.coords = []
        for line in nparray:
            row = []
            for item in line:
                row.append(int(item))
            self.coords.append(row)

    def update_all_sizes(self):
        self.update_pix_size()
        self.update_grid_width()
        self.update_x_len()
        self.update_y_len()

    def update_pix_size(self):
        if SCREEN_RESOLUTION == tuple:
            raise TypeError("Screen resolution variable isn't set")
        if len(self.coords) == 0:
            x = 0
        else:
            x = len(self.coords[0])
        y = len(self.coords)
        self.pix_size = min(SCREEN_RESOLUTION[0] // x, SCREEN_RESOLUTION[1] // y)

    def update_grid_width(self):
        if self.pix_size < 5:
            self.grid_width = 0
        else:
            self.grid_width = 1

    def update_x_len(self):
        if len(self.coords) == 0:
            self.x_len = 0
        self.x_len = len(self.coords[0])

    def update_y_len(self):
        self.y_len = len(self.coords)

    def get_value(self, x, y):
        return self.coords[y][x]

    def set_value(self, x, y, value):
        self.coords[y][x] = value

    def get_closest_route_coords(self, x_pix, y_pix):
        x = x_pix // self.pix_size
        y = y_pix // self.pix_size
        if x < 0:
            x = 0
        elif x > self.x_len - 1:
            x = self.x_len - 1
        if y < 0:
            y = 0
        elif y > self.y_len - 1:
            y = self.y_len - 1
        return x, y

    def coords_is_in_map(self, x, y):
        return 0 <= x < self.x_len and 0 <= y < self.y_len

    def is_player_at_coords(self, x, y):
        return self.player.coords == [x, y]

    def is_enemy_at_coords(self, x, y):
        return self.enemies.is_enemy_at_coord(x, y)

    def is_living_at_coords(self, x, y):
        return self.is_player_at_coords(x, y) or self.is_enemy_at_coords(x, y)

    def is_wall(self, x, y):
        return self.get_value(x, y) != 0

    def is_available_move(self, x, y):
        return self.coords_is_in_map(x, y) and not self.is_living_at_coords(x, y) and not self.is_wall(x, y)

    def move_relative_if_possible(self, canvas: tk.Canvas, living: Living, x_rel, y_rel):
        x, y = living.get_relative(x_rel, y_rel)
        if not self.is_available_move(x, y):
            return living.x, living.y, False
        self.draw_route(canvas, living.x, living.y, self.calc_route_color_coords(living.x, living.y))
        living.update_pos(x, y)
        self.draw_route(canvas, x, y, living.color)
        return x, y, True

    def update_player_nodraw(self, x_pix, y_pix):
        x, y = self.get_closest_route_coords(x_pix, y_pix)
        if self.player.is_spawned:
            self.player.coords = [x, y]
        else:
            self.player = Player(x, y)

    def update_enemy_nodraw(self, x_pix, y_pix):
        x, y = self.get_closest_route_coords(x_pix, y_pix)
        enemy = self.enemies.get_enemy_at_coord(x, y)
        if enemy:
            self.enemies.remove(enemy)
        else:
            self.enemies.add(Enemy(x, y))
        return x, y

    def flip_wall_nodraw(self, x, y):
        old_value = self.get_value(x, y)
        if not (0 <= old_value < 10 * AMPLIFY_VAL):
            return
        elif old_value < 5 * AMPLIFY_VAL:
            new_value = 9 * AMPLIFY_VAL
        else:
            new_value = 0
        self.set_value(x, y, new_value)
        return new_value

    def update_player(self, canvas: tk.Canvas, x_pix, y_pix):
        if self.player.is_spawned:
            cur_x = self.player.x
            cur_y = self.player.y
        else:
            cur_x = None
            cur_y = None
        self.update_player_nodraw(x_pix, y_pix)
        if cur_x and cur_y:
            self.draw_route(canvas, cur_x, cur_y, self.calc_route_color_coords(cur_x, cur_y))
        cur_x = self.player.x
        cur_y = self.player.y
        self.draw_route(canvas, cur_x, cur_y, "green")

    def update_enemy(self, canvas: tk.Canvas, x_pix, y_pix):
        x, y = self.update_enemy_nodraw(x_pix, y_pix)
        new_color = "red" if self.enemies.is_enemy_at_coord(x, y) else self.calc_route_color_coords(x, y)
        self.draw_route(canvas, x, y, new_color)

    def draw_route(self, canvas: tk.Canvas, x, y, color):
        canvas.create_rectangle(x * self.pix_size, y * self.pix_size,
                                (x + 1) * self.pix_size, (y + 1) * self.pix_size,
                                fill=color, width=self.grid_width)

    @staticmethod
    def calc_route_color(item_value):
        intensity = hex(255 - int(255 * (item_value / AMPLIFY_VAL / 10)))[2:]
        return f"#{intensity * 3}"

    def calc_route_color_coords(self, x, y):
        return self.calc_route_color(self.get_value(x, y))

    def draw(self, canvas: tk.Canvas):
        for y, row in enumerate(self.coords):
            for x, item in enumerate(row):
                if [x, y] == self.player.coords:
                    color = "green"
                elif self.enemies.is_enemy_at_coord(x, y):
                    color = "red"
                else:
                    color = self.calc_route_color(item)
                self.draw_route(canvas, x, y, color)

    def cross_route(self, canvas: tk.Canvas, x, y, color="red", width=2):
        canvas.create_line(x * self.pix_size, y * self.pix_size,
                           (x + 1) * self.pix_size, (y + 1) * self.pix_size,
                           fill=color, width=width)
        canvas.create_line((x + 1) * self.pix_size, y * self.pix_size,
                           x * self.pix_size, (y + 1) * self.pix_size,
                           fill=color, width=width)


class MapGraph:
    def __init__(self, the_map: Map):
        self.the_map = the_map
        self.graph = Graph()

    def get_node_index(self, x, y):
        if not (0 <= x < self.the_map.x_len and 0 <= y < self.the_map.y_len):
            return None
        return x + y * self.the_map.x_len

    def get_node_coords(self, node_index):
        if node_index >= self.the_map.x_len * self.the_map.y_len:
            return None
        return node_index % self.the_map.x_len, node_index // self.the_map.x_len

    def is_diagonal_wall_between_xy(self, x, y, neigh_x, neigh_y):
        return self.is_diagonal_wall_between(self.get_node_index(x, y), self.get_node_index(neigh_x, neigh_y))

    def is_diagonal_wall_between(self, node_index, neighbour_index):
        cur_x, cur_y = self.get_node_coords(node_index)
        neigh_x, neigh_y = self.get_node_coords(neighbour_index)
        horizontal_node = self.get_node_index(neigh_x, cur_y)
        vertical_node = self.get_node_index(cur_x, neigh_y)
        if not (horizontal_node and vertical_node and
                self.graph.get_nodedata(horizontal_node) and
                self.graph.get_nodedata(vertical_node)):
            return False
        if math.sqrt((cur_x - neigh_x) ** 2 + (cur_y - neigh_y) ** 2):
            return True

    def make_nodes(self):
        for row in self.the_map.coords:
            for item in row:
                self.graph.add_node(item)

    def make_edges(self):
        for node_index in range(self.graph.get_number_of_nodes()):
            cur_x, cur_y = self.get_node_coords(node_index)
            if cur_x is None:
                continue
            for x_diff in (-1, 0, 1):
                for y_diff in (-1, 0, 1):
                    if x_diff == 0 and y_diff == 0:
                        continue
                    neigh_x = cur_x + x_diff
                    neigh_y = cur_y + y_diff
                    neighbour_index = self.get_node_index(neigh_x, neigh_y)
                    if neighbour_index is None:
                        continue
                    if self.is_diagonal_wall_between(node_index, neighbour_index):
                        continue
                    weight = self.calc_weight(node_index, neighbour_index)
                    self.graph.add_edge(node_index, neighbour_index, weight)

    def calc_weight(self, node_index, neighbour_index):
        if node_index is None or neighbour_index is None:
            return None
        x1, y1 = self.get_node_coords(node_index)
        x2, y2 = self.get_node_coords(neighbour_index)
        x_diff = x1 - x2
        y_diff = y1 - y2
        distance = math.sqrt(x_diff ** 2 + y_diff ** 2)
        walk_const = 1
        node_weight = self.graph.nodes[node_index].data
        neighbour_weight = self.graph.nodes[neighbour_index].data
        return distance * (walk_const + abs(neighbour_weight + node_weight))

    def update_node_value(self, node_index, value):
        self.graph.nodes[node_index].data = value
        for neighbour_index in self.graph.get_neighbours(node_index):
            weight = self.calc_weight(node_index, neighbour_index)
            self.graph.nodes[node_index].neighbours[neighbour_index].weight = weight
            self.graph.nodes[neighbour_index].neighbours[node_index].weight = weight
        x, y = self.get_node_coords(node_index)
        for a in range(0, 360, 90):
            b = a + 90
            x1, y1 = int(x + math.cos(math.radians(a))), int(y + math.sin(math.radians(a)))
            x2, y2 = int(x + math.cos(math.radians(b))), int(y + math.sin(math.radians(b)))
            route_1, route_2 = self.get_node_index(x1, y1), self.get_node_index(x2, y2)
            if route_1 and route_2 and self.is_diagonal_wall_between(route_1, route_2):
                try:
                    del self.graph.nodes[route_1].neighbours[route_2]
                except KeyError:
                    pass
                try:
                    del self.graph.nodes[route_2].neighbours[route_1]
                except KeyError:
                    pass
            elif not (route_2 in self.graph.nodes[route_1].neighbours and route_1 in self.graph.nodes[route_2].neighbours):
                weight = self.calc_weight(route_1, route_2)
                self.graph.add_edge(route_1, route_2, weight)
                self.graph.add_edge(route_2, route_1, weight)

    def make_whole_graph(self):
        self.make_nodes()
        self.make_edges()

    def find_shortest_path(self, player_coords: List[int] = -1, enemies_coords: List[List[int]] = -1, func=None, time_diff=20):
        if player_coords == -1:
            if not self.the_map.player.is_spawned:
                return [], 0
            player_coords = self.the_map.player.coords
        if enemies_coords == -1:
            if len(self.the_map.enemies) == 0:
                return [], 0
            enemies_coords = self.the_map.enemies.get_enemy_coord_list()

        tmp_graph = Graph()
        tmp_graph.nodes = self.graph.nodes.copy()
        player_node = self.get_node_index(player_coords[0], player_coords[1])
        enemies_nodes = []
        for target in enemies_coords:
            enemies_nodes.append(self.get_node_index(target[0], target[1]))
        # print(player_node)
        a = time.time()
        # nodes_found = tmp_graph.dijkstra(player_node, enemies_nodes, func, time_diff)
        nodes_found = int(dijkstra.dijkstra(tmp_graph, player_node, enemies_nodes))
        print(a - time.time())

        shortest_lists = []
        for enemy_node in enemies_nodes:
            shortest_list = []
            cur_node = enemy_node
            while cur_node is not None:
                shortest_list.append(self.get_node_coords(cur_node))
                cur_node = tmp_graph.get_prevnode(cur_node)
            shortest_lists.append(shortest_list)
        # exit(0)
        # print(shortest_lists)
        return shortest_lists, nodes_found


class System:
    def __init__(self, gui: tk.Tk, canvas: tk.Canvas, the_map: Map):
        self.gui = gui
        self.canvas = canvas
        self.the_map = the_map
        self.the_map.draw(canvas)
        self.graph = MapGraph(the_map)
        self.graph.make_whole_graph()

        self.keys = {"w": False, "s": False, "a": False, "d": False}

        self.ticks_count = 1
        self.looptime = 100
        self.start_tick = time.time()
        self.draw_pathfinding()
        # self.systemloop()
        # self.loop(self.move_player, 100)
        # self.loop(self.move_enemies, 200)

    def loop(self, function, ms):
        function()
        self.gui.after(ms, lambda: self.loop(function, ms))

    def systemloop(self):
        # print(time.time() - self.start_tick)
        self.start_tick = time.time()
        self.move_player()

        if self.is_n_tick(2):
            self.move_enemies()

        self.ticks_count += 1
        tmp = time.time()
        time_gone = 1000 * (tmp - self.start_tick)
        waittime = int(self.looptime - time_gone)
        # print(f"{waittime}, {time_gone}")
        if waittime < 0:
            waittime = 1
        self.gui.after(waittime, self.systemloop)

    def is_n_tick(self, n):
        return not self.ticks_count % n

    def reset_movement(self):
        for key in self.keys:
            self.keys[key] = False

    def move_player(self):
        x_dir = 0
        y_dir = 0
        if self.keys["w"]:
            y_dir -= 1
        if self.keys["s"]:
            y_dir += 1
        if self.keys["a"]:
            x_dir -= 1
        if self.keys["d"]:
            x_dir += 1
        if not x_dir and not y_dir:
            return
        self.the_map.move_relative_if_possible(self.canvas, self.the_map.player, x_dir, y_dir)

    def move_enemies(self):
        a = time.time()
        shortest_paths, _ = self.graph.find_shortest_path(time_diff=0)
        # print(time.time() - a)
        for path in shortest_paths:
            self.move_enemy_path(path)
        # print(f"-{time.time() - a}")

    def move_enemy_path(self, path):
        if len(path) == 0:
            return
        elif len(path) <= 2:
            print("You lost")
            return
        enemy = self.the_map.enemies.get_enemy_at_coord(path[0][0], path[0][1])
        x_rel, y_rel = enemy.get_from_relative(path[1][0], path[1][1])
        self.move_enemy(enemy, x_rel, y_rel)

    def move_enemy(self, enemy, x, y):
        self.the_map.move_relative_if_possible(self.canvas, enemy, x, y)

    def draw_pathfinding(self):
        shortest_paths, _ = self.graph.find_shortest_path(time_diff=0)
        for shortest_path in shortest_paths:
            shortest_path.reverse()
            self.draw_shortest_path(shortest_path)

    def draw_pathfinding_animation(self, time_diff=20):
        shortest_paths, num_nodes = self.graph.find_shortest_path(
            func=lambda index, ms: self.gui.after(ms, lambda: self.bluecross(index)), time_diff=time_diff)
        for shortest_path in shortest_paths:
            shortest_path.reverse()
            self.draw_shortest_path(shortest_path, num_nodes * time_diff)

    def draw_shortest_path(self, shortest_path, start_time=0, time_diff=0):
        time = start_time
        runfunc = lambda after_ms, coords: self.gui.after(after_ms,
                                                          lambda: self.the_map.cross_route(self.canvas, coords[0],
                                                                                           coords[1]))
        for item in shortest_path:
            runfunc(time, item)
            time += time_diff

    def bluecross(self, node_index: int):
        coords = self.graph.get_node_coords(node_index)
        self.the_map.cross_route(self.canvas, coords[0], coords[1], color="blue", width=1)

    def flip_wall(self, x_pix, y_pix, last_coords=None):
        x, y = self.the_map.get_closest_route_coords(x_pix, y_pix)
        if [x, y] in [last_coords, self.the_map.player.coords] or self.the_map.enemies.is_enemy_at_coord(x, y):
            return None
        new_value = self.the_map.flip_wall_nodraw(x, y)
        self.graph.update_node_value(self.graph.get_node_index(x, y), new_value)
        self.the_map.draw_route(self.canvas, x, y, self.the_map.calc_route_color(self.the_map.get_value(x, y)))
        return [x, y]


class Gui:
    def __init__(self, mapfile="map.txt"):
        self.gui = tk.Tk()
        self.gui.update()
        global SCREEN_RESOLUTION
        SCREEN_RESOLUTION = (self.gui.winfo_screenwidth(), self.gui.winfo_screenheight())

        the_map = Map()
        the_map.get_map(mapfile)

        self.canvas = tk.Canvas(self.gui, width=the_map.x_pix, height=the_map.y_pix, bg="grey")
        self.canvas.pack()
        self.system = System(self.gui, self.canvas, the_map)

        self.lasttick = {"middle_motion": time.time(), "last_flip_coords": []}

        self.gui.bind_all("<Button-1>", self.left_click)
        self.gui.bind_all("<Button-2>", self.middle_motion)
        self.gui.bind_all("<B2-Motion>", self.middle_motion)
        self.gui.bind_all("<ButtonRelease-2>", self.middle_release)
        self.gui.bind_all("<Button-3>", self.right_click)
        self.gui.bind_all("<space>", self.space_keypress)
        self.gui.bind_all("r", self.redraw)

        # Movement
        self.gui.bind_all("<KeyPress>", self.keypressed)
        self.gui.bind_all("<KeyRelease>", self.keyreleased)
        # self.gui.bind_all("w", self.moveup)
        # self.gui.bind_all("s", self.movedown)
        # self.gui.bind_all("a", self.moveleft)
        # self.gui.bind_all("d", self.moveright)

        tk.mainloop()

    def left_click(self, event):
        self.system.the_map.update_player(self.canvas, event.x, event.y)

    def middle_motion(self, event):
        if time.time() - self.lasttick["middle_motion"] < 0.05:
            return
        self.lasttick["middle_motion"] = time.time()
        coords = self.system.flip_wall(event.x, event.y, self.lasttick["last_flip_coords"])
        if coords:
            self.lasttick["last_flip_coords"] = coords

    def middle_release(self, event):
        self.lasttick["last_flip_coords"] = []

    def right_click(self, event):
        self.system.the_map.update_enemy(self.canvas, event.x, event.y)

    def space_keypress(self, event):
        self.system.draw_pathfinding()
        # self.system.draw_pathfinding_animation()

    def redraw(self, event):
        self.system.the_map.draw(canvas=self.canvas)

    def keypressed(self, event):
        self.system.keys[event.char] = True

    def keyreleased(self, event):
        self.system.keys[event.char] = False


if __name__ == '__main__':
    Gui("map.txt")
