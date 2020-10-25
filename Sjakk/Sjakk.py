import tkinter
import math


class ChessBoard:
    def __init__(self, canvas, boardlength, direction: str = "white"):
        self.canvas: tkinter.Canvas = canvas
        self.boardlength = boardlength
        self.routelength = self.boardlength / 10
        self.direction = direction

        self.coordinates = []
        self.routedict = {}
        if self.direction == "white":
            self.numbers = "87654321"
            self.letters = "abcdefgh"
        else:
            self.numbers = "12345678"
            self.letters = "hgfedcba"
        for row, number in enumerate(self.numbers):
            row += 1
            rad = []
            for column, letter in enumerate(self.letters):
                column += 1
                if (row + column) % 2 == 1:
                    color = "black"
                else:
                    color = "white"
                routecoords = (column * self.routelength + self.routelength / 2,
                               row * self.routelength + self.routelength / 2, color)
                rad.append(routecoords)
                self.routedict[f"{letter}{number}"] = tuple(routecoords)
            self.coordinates.append(tuple(rad))
        self.coordinates = tuple(self.coordinates)

        self.draw()

        self.colored_routes = []

    def draw(self):
        bokstaver = self.letters.upper()
        bokstavindex = 0
        tallindex = 0
        tall = self.numbers
        rl = self.routelength / 2
        for row in self.coordinates:
            for route in row:
                self.canvas.create_rectangle(route[0] - rl, route[1] - rl, route[0] + rl, route[1] + rl, fill=route[2])
                if route[1] == self.coordinates[0][0][1]:
                    self.canvas.create_text(route[0], route[1] - self.routelength + rl / 2,
                                            font=f"Algerian {int(self.routelength / 3)}",
                                            text=bokstaver[bokstavindex])
                    self.canvas.create_text(route[0], route[1] + 8 * self.routelength - rl / 2,
                                            font=f"Algerian {int(self.routelength / 3)}",
                                            text=bokstaver[bokstavindex])
                    bokstavindex += 1
                if route[0] == self.coordinates[0][0][0]:
                    self.canvas.create_text(route[0] - self.routelength + rl / 2, route[1],
                                            font=f"Algerian {int(self.routelength / 3)}", text=str(tall[tallindex]))
                    self.canvas.create_text(route[0] + 8 * self.routelength - rl / 2, route[1],
                                            font=f"Algerian {int(self.routelength / 3)}", text=str(tall[tallindex]))
                    tallindex += 1

    def route(self, place: str, withcolor: bool = False):
        bokstaver = self.letters.upper()
        tall = self.numbers
        try:
            if len(place) != 2:
                raise ValueError
            bokstav = place[0].upper()
            for index, gjeldenebokstav in enumerate(bokstaver):
                if gjeldenebokstav == bokstav:
                    bokstavtall = index
                    break
            tall = int(tall[int(place[1]) - 1]) - 1
        except ValueError:
            raise ValueError(f"{place} is not a valid route.")
        coordinate = self.coordinates[tall][bokstavtall]
        if withcolor:
            return coordinate
        else:
            return [coordinate[0], coordinate[1]]

    def closest_route(self, pos):
        closestroute = ""
        first = True
        for route in self.routedict:
            if first:
                closestroute = route
                first = False
                continue
            else:
                distance_click = math.sqrt((pos[0] - self.routedict[route][0]) ** 2 +
                                           (pos[1] - self.routedict[route][1]) ** 2)
                distance_closest = math.sqrt((pos[0] - self.routedict[closestroute][0]) ** 2 +
                                             (pos[1] - self.routedict[closestroute][1]) ** 2)
                if distance_click < distance_closest:
                    closestroute: str = route
        return closestroute

    def add_colored_route(self, route: str, color: str = "red"):
        coords = self.route(route)
        pos1 = (coords[0] - self.routelength/2, coords[1] - self.routelength/2)
        pos2 = (coords[0] + self.routelength/2, coords[1] + self.routelength/2)
        colored_route = self.canvas.create_rectangle(pos1[0], pos1[1], pos2[0], pos2[1], outline=color, width=4)
        self.colored_routes.append(colored_route)

    def clear_colored_routes(self):
        for colored_route in self.colored_routes:
            self.canvas.delete(colored_route)
        self.colored_routes = []


class ChessPiece:
    def __init__(self, system, piece: str, color: str, start_pos: str):
        self.system: Game = system
        self.canvas: tkinter.Canvas = system.canvas
        self.chessboard = system.chessboard

        self.piece = piece.lower()
        validpieces = ("king", "queen", "rook", "bishop", "knight", "pawn")
        if self.piece not in validpieces:
            raise ValueError(f"{self.piece} should be one of the following:\n\t> {validpieces}")

        self.color = color.lower()
        validcolors = ("white", "black")
        if self.color not in validcolors:
            raise ValueError(f"{self.color} should be one of the following:\n\t> {validcolors}")

        self.player = self.system.get_player(self.color)

        self.routepos = start_pos
        self.softpos = self.chessboard.route(self.routepos)
        self.size = self.chessboard.routelength * (3 / 7)
        self.system.routes_dict[self.routepos] = self

        self.available_moves = []
        self.routes_looking_at = []

        if self.piece == "king":
            self.value = 1000.0
        elif self.piece == "queen":
            self.value = 9.0
        elif self.piece == "rook":
            self.value = 5.0
        elif self.piece == "bishop":
            self.value = 3.5
        elif self.piece == "knight":
            self.value = 3.0
        elif self.piece == "pawn":
            self.value = 1.0
        else:
            raise ValueError(f"Couldn't set value to {self.piece}")

        self.routevalue_matrix = self.get_route_values()

        if self.piece == "knight":
            self.letter = "N"
        else:
            self.letter = self.piece[0].capitalize()

    def copy_all(self):
        piece = ChessPiece(self.system, self.piece, self.color, self.routepos)
        piece.available_moves = self.available_moves.copy()
        piece.routes_looking_at = self.routes_looking_at.copy()
        return piece

    def copy_routepos(self, piece):
        piece.routepos = self.routepos

    def get_route_values(self):
        if self.piece == "king":
            matrix = [[-3.0, -4.0, -4.0, -5.0, -5.0, -4.0, -4.0, -3.0],
                      [-3.0, -4.0, -4.0, -5.0, -5.0, -4.0, -4.0, -3.0],
                      [-3.0, -4.0, -4.0, -5.0, -5.0, -4.0, -4.0, -3.0],
                      [-3.0, -4.0, -4.0, -5.0, -5.0, -4.0, -4.0, -3.0],
                      [-2.0, -3.0, -3.0, -4.0, -4.0, -3.0, -3.0, -2.0],
                      [-1.0, -2.0, -2.0, -2.0, -2.0, -2.0, -2.0, -1.0],
                      [ 2.0,  2.0,  0.0,  0.0,  0.0,  0.0,  2.0,  2.0],
                      [ 2.0,  3.0,  1.0,  0.0,  0.0,  1.0,  3.0,  2.0]]
        elif self.piece == "queen":
            matrix = [[-2.0, -1.0, -1.0, -0.5, -0.5, -1.0, -1.0, -2.0],
                      [-1.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0, -1.0],
                      [-1.0,  0.0,  0.5,  0.5,  0.5,  0.5,  0.0, -1.0],
                      [-0.5,  0.0,  0.5,  0.5,  0.5,  0.5,  0.0, -0.5],
                      [ 0.0,  0.0,  0.5,  0.5,  0.5,  0.5,  0.0, -0.5],
                      [-1.0,  0.5,  0.5,  0.5,  0.5,  0.5,  0.0, -1.0],
                      [-1.0,  0.0,  0.5,  0.0,  0.0,  0.0,  0.0, -1.0],
                      [-2.0, -1.0, -1.0, -0.5, -0.5, -1.0, -1.0, -2.0]]
        elif self.piece == "rook":
            matrix = [[ 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,  0.0],
                      [ 0.5, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0,  0.5],
                      [-0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.5],
                      [-0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.5],
                      [-0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.5],
                      [-0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.5],
                      [-0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.5],
                      [ 0.0, 0.0, 0.0, 0.5, 0.5, 0.0, 0.0,  0.0]]
        elif self.piece == "bishop":
            matrix = [[-2.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -2.0],
                      [-1.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0, -1.0],
                      [-1.0,  0.0,  0.5,  1.0,  1.0,  0.5,  0.0, -1.0],
                      [-1.0,  0.5,  0.5,  1.0,  1.0,  0.5,  0.5, -1.0],
                      [-1.0,  0.0,  1.0,  1.0,  1.0,  1.0,  0.0, -1.0],
                      [-1.0,  1.0,  1.0,  1.0,  1.0,  1.0,  1.0, -1.0],
                      [-1.0,  0.5,  0.0,  0.0,  0.0,  0.0,  0.5, -1.0],
                      [-2.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -2.0]]
        elif self.piece == "knight":
            matrix = [[-5.0, -4.0, -3.0, -3.0, -3.0, -3.0, -4.0, -5.0],
                      [-4.0, -2.0,  0.0,  0.0,  0.0,  0.0, -2.0, -4.0],
                      [-3.0,  0.0,  1.0,  1.5,  1.5,  1.0,  0.0, -3.0],
                      [-3.0,  0.5,  1.5,  2.0,  2.0,  1.5,  0.5, -3.0],
                      [-3.0,  0.0,  1.5,  2.0,  2.0,  1.5,  0.0, -3.0],
                      [-3.0,  0.5,  1.0,  1.5,  1.5,  1.0,  0.5, -3.0],
                      [-4.0, -2.0,  0.0,  0.5,  0.5,  0.0, -2.0, -4.0],
                      [-5.0, -4.0, -3.0, -3.0, -3.0, -3.0, -4.0, -5.0]]
        elif self.piece == "pawn":
            matrix = [[16.0, 17.0,  18.0,  18.0,  18.0,  18.0,  17.0, 16.0],
                      [5.0,   5.0,   5.0,   5.0,   5.0,   5.0,   5.0,  5.0],
                      [1.0,   1.0,   2.0,   3.0,   3.0,   2.0,   1.0,  1.0],
                      [0.5,   0.5,   1.0,   2.5,   2.5,   1.0,   0.5,  0.5],
                      [0.0,   0.0,   0.0,   2.0,   2.0,   0.0,   0.0,  0.0],
                      [0.5,  -0.5,  -1.0,   0.0,   0.0,  -1.0,  -0.5,  0.5],
                      [0.5,   1.0,   1.0,  -2.0,  -2.0,   1.0,   1.0,  0.5],
                      [0.0,   0.0,   0.0,   0.0,   0.0,   0.0,   0.0,  0.0]]
        else:
            raise ValueError
        return matrix

    def route_value(self, route: str):
        letters = "abcdefgh"
        letter_index = letters.index(route[0])
        if self.color == "white":
            numbers = "87654321"
        else:
            numbers = "12345678"
        number_index = numbers.index(route[1])
        return self.routevalue_matrix[number_index][letter_index]

    def calculate_value(self):
        return self.route_value(self.routepos) + 3*self.value

    def draw_new(self, pos=None):
        if pos is not None:
            self.softpos = pos
        self.background = self.canvas.create_rectangle(self.softpos[0] - self.size * (3 / 5),
                                                       self.softpos[1] - self.size * (3 / 5),
                                                       self.softpos[0] + self.size * (3 / 5),
                                                       self.softpos[1] + self.size * (3 / 5), fill="gray")
        self.drawnpiece = self.canvas.create_text(self.softpos[0], self.softpos[1], text=self.letter, fill=self.color,
                                                  font=f"Algerian {int(self.size)} bold")

    def draw(self):
        self.canvas.coords(self.background, self.softpos[0] - self.size * (3 / 5),
                           self.softpos[1] - self.size * (3 / 5), self.softpos[0] + self.size * (3 / 5),
                           self.softpos[1] + self.size * (3 / 5))
        self.canvas.coords(self.drawnpiece, self.softpos[0], self.softpos[1])
        self.canvas.lift(self.background)
        self.canvas.lift(self.drawnpiece)

    def soft_move(self, pos: list):
        self.softpos = pos
        self.draw()

    def move(self, route: str):
        self.system.routes_dict[self.routepos] = None
        self.routepos = route
        self.system.routes_dict[self.routepos] = self
        self.soft_move(self.chessboard.route(self.routepos))
        if self.piece == "pawn":
            if (self.routepos[1] == "8" and self.color == "white") or \
                    (self.routepos[1] == "1" and self.color == "black"):
                self.replace_piece()
        self.system.switchturn()

    def remove(self):
        self.player.pieces.remove(self)
        if self.system.get_piece_at_route(self.routepos) == self.routepos:
            self.system.routes_dict[self.routepos] = None
        self.canvas.delete(self.background)
        self.canvas.delete(self.drawnpiece)

    def replace_piece(self, new_piece_name=None, close_popup=None):
        if new_piece_name is None:
            popup = tkinter.Tk()
            popup.title("Choose piece")
            button = tkinter.Button(popup, text="QUEEN", font="Arial 15", command=lambda: self.replace_piece("queen", popup))
            button.pack(fill=tkinter.X)
            button = tkinter.Button(popup, text="ROOK", font="Arial 15", command=lambda: self.replace_piece("rook", popup))
            button.pack(fill=tkinter.X)
            button = tkinter.Button(popup, text="BISHOP", font="Arial 15", command=lambda: self.replace_piece("bishop", popup))
            button.pack(fill=tkinter.X)
            button = tkinter.Button(popup, text="KNIGHT", font="Arial 15", command=lambda: self.replace_piece("knight", popup))
            button.pack(fill=tkinter.X)
            popup.geometry("+%d+%d" % (int(self.system.mainwindow.winfo_width()/2), int(self.system.mainwindow.winfo_height()/2)))
            popup.resizable(width=False, height=False)
        else:
            if close_popup is not None:
                close_popup.destroy()
            self.player.add_piece(ChessPiece(self.system, new_piece_name, self.color, self.routepos))
            self.remove()

    def update_available_moves(self):
        if self.player.checked and self.piece != "king":
            return
        self.available_moves = []
        self.routes_looking_at = []

        if self.piece in ("rook", "queen", "king"):
            for interval in [range(int(self.routepos[1])+1, 9), range(int(self.routepos[1])-1, 0, -1)]:
                for number in interval:
                    route = f"{self.routepos[0]}{number}"
                    if not self.system.is_piece_at_route(route):
                        self.add_avalable_move(route)
                        if self.piece == "king":
                            break
                    elif self.player.is_opponent_at_route(route):
                        self.add_avalable_move(route)
                        break
                    elif self.player.is_self_at_route(route):
                        self.routes_looking_at.append(route)
                        break
                    else:
                        break
            letters = self.system.chessboard.letters
            for interval in [range(letters.index(self.routepos[0])+1, 8), range(letters.index(self.routepos[0])-1, -1, -1)]:
                for letter in interval:
                    letter = letters[letter]
                    route = f"{letter}{self.routepos[1]}"
                    if not self.system.is_piece_at_route(route):
                        self.add_avalable_move(route)
                        if self.piece == "king":
                            break
                    elif self.player.is_opponent_at_route(route):
                        self.add_avalable_move(route)
                        break
                    elif self.player.is_self_at_route(route):
                        self.routes_looking_at.append(route)
                        break
                    else:
                        break
            if self.piece == "rook":
                return

        if self.piece in ("bishop", "queen", "king"):
            letters = self.system.chessboard.letters
            for interval in [range(letters.index(self.routepos[0])+1, 8), range(letters.index(self.routepos[0])-1, -1, -1)]:
                for ypos in [1, -1]:
                    for numberdiff, letter in enumerate(interval):
                        numberdiff += 1
                        letter = letters[letter]
                        number = int(self.routepos[1]) + numberdiff * ypos
                        if number not in tuple(range(1, 9)):
                            break
                        route = f"{letter}{number}"
                        if not self.system.is_piece_at_route(route):
                            self.add_avalable_move(route)
                            if self.piece == "king":
                                break
                        elif self.player.is_opponent_at_route(route):
                            self.add_avalable_move(route)
                            break
                        elif self.player.is_self_at_route(route):
                            self.routes_looking_at.append(route)
                            break
                        else:
                            break
            return

        if self.piece == "knight":
            intpos = (ord(self.routepos[0]), int(self.routepos[1]))
            negpos = (-1, 1)
            for twice in negpos:
                twice = 2*twice
                for side in negpos:
                    for route in ((chr(intpos[0] + twice), intpos[1] + side),
                                  (chr(intpos[0] + side), intpos[1] + twice)):
                        if route[0] not in "abcdefgh" or route[1] not in range(1, 9):
                            continue
                        else:
                            route = f"{route[0]}{route[1]}"
                            if not self.system.is_piece_at_route(route) or self.player.is_opponent_at_route(route):
                                self.add_avalable_move(route)
                                continue
                            elif self.player.is_self_at_route(route):
                                self.routes_looking_at.append(route)
                                continue

        elif self.piece == "pawn":
            if self.routepos[1] in "18":
                return
            number = int(self.routepos[1])
            if self.color == "white":
                route_infront = f"{self.routepos[0]}{number + 1}"
                if not self.system.is_piece_at_route(route_infront):
                    if number == 2:
                        self.add_avalable_move(f"{self.routepos[0]}{number + 2}")
                    self.add_avalable_move(route_infront)
            else:
                route_infront = f"{self.routepos[0]}{number - 1}"
                if not self.system.is_piece_at_route(route_infront):
                    if number == 7:
                        self.add_avalable_move(f"{self.routepos[0]}{number - 2}")
                    self.add_avalable_move(route_infront)
            for side in (-1, 1):
                letter = chr((ord(route_infront[0]) + side))
                diagonal_route = f"{letter}{route_infront[1]}"
                if letter not in "abcdefgh":
                    continue
                if self.player.is_opponent_at_route(diagonal_route):
                    self.add_avalable_move(diagonal_route)
                else:
                    self.routes_looking_at.append(diagonal_route)

        else:
            raise ValueError(f"Couldn't update available move to {self.piece}")

    def remove_kings_checkmoves(self):
        if self.piece == "king":
            for piece in self.player.get_other_player().pieces:
                for available_move in piece.available_moves:
                    if available_move in self.available_moves:
                        self.available_moves.remove(available_move)
                        self.routes_looking_at.append(available_move)
                for looking_at in piece.routes_looking_at:
                    if looking_at in self.available_moves:
                        if looking_at in self.available_moves:
                            self.available_moves.remove(looking_at)
                            self.routes_looking_at.append(looking_at)

    def add_avalable_move(self, route: str):
        self.available_moves.append(route)
        self.check_if_checking(route)

    def check_if_checking(self, route: str):
        piece = self.system.routes_dict[route]
        other_player = self.player.get_other_player()
        if piece == other_player.king:
            other_player.checked = True


class Player:
    def __init__(self, system, color: str, ai=False, online=False):
        self.system: Game = system
        self.AI = ai
        self.online = online
        self.color = color
        self.pieces = []
        self.king: ChessPiece = None
        self.checked = False
        self.checkmate = False

    def copy(self, force_ai=False):
        if force_ai:
            ai = True
        else:
            ai = self.AI
        player = Player(self.system, self.color, ai)
        for piece in self.pieces:
            player.pieces.append(piece.copy_all())
            if piece.piece == "king":
                player.king = piece
        player.checked = self.checked
        player.checkmate = self.checked
        return player

    def add_piece(self, piece: ChessPiece):
        self.pieces.append(piece)
        if piece.piece == "king":
            self.king: ChessPiece = piece
        piece.draw_new()

    def add_all_pieces(self):
        if self.system.chessboard.direction == self.color:
            pos = "87"
        else:
            pos = "12"
        numbers = f"{self.system.chessboard.numbers[int(pos[0])-1]}{self.system.chessboard.numbers[int(pos[1])-1]}"
        for letter in self.system.chessboard.letters:
            self.add_piece(ChessPiece(self.system, "pawn", self.color, f"{letter}{numbers[1]}"))
            if letter in "ah":
                piece = "rook"
            elif letter in "bg":
                piece = "knight"
            elif letter in "cf":
                piece = "bishop"
            elif letter == "d":
                piece = "queen"
            elif letter in "e":
                piece = "king"
            else:
                raise ValueError
            self.add_piece(ChessPiece(self.system, piece, self.color, f"{letter}{numbers[0]}"))

    def get_other_player(self):
        for player in self.system.players:
            if player != self:
                returned: Player = player
                return returned

    def is_opponent_at_route(self, route: str):
        if not self.system.is_piece_at_route(route):
            return False
        piece = self.system.routes_dict[route]
        if piece.color != self.color:
            return True
        else:
            return False

    def is_self_at_route(self, route: str):
        if not self.system.is_piece_at_route(route):
            return False
        piece = self.system.routes_dict[route]
        if piece.color == self.color:
            return True
        else:
            return False


class Game:
    def __init__(self, mainwindow: tkinter.Tk, canvas: tkinter.Canvas):
        self.mainwindow = mainwindow
        self.canvas = canvas
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()
        self.smaller_length = canvas_width if canvas_width < canvas_height else canvas_height
        self.chessboard = ChessBoard(self.canvas, self.smaller_length)

        self.players = []
        self.turn = 0

        self.routes_dict = {}
        for route in self.chessboard.routedict:
            self.routes_dict[route] = None

        self.setup()

        self.turnVar = tkinter.StringVar()
        self.turnVar.set(f"{self.players[self.turn].color.capitalize()}'s turn")
        turnLabel = tkinter.Label(self.mainwindow, textvariable=self.turnVar,
                                  font=f"Castellar {int(self.chessboard.routelength/3.5)} bold")
        turnLabel.grid(row=0, column=0)
        self.checkVar = tkinter.StringVar()
        self.checkVar.set("Check")
        self.checkLabel = tkinter.Label(self.mainwindow, textvariable=self.checkVar,
                                   font=f"Castellar {int(self.chessboard.routelength/3.5)*2} bold")
        self.checkLabel.grid(row=1, column=0)
        self.checkLabel.lower(self.canvas)

    def change_checklabel(self, lower: bool, checkmate=None):
        if lower:
            self.checkLabel.lower(self.canvas)
        else:
            self.checkLabel.lift(self.canvas)
        if checkmate is not None:
            self.checkVar.set(f"{checkmate}")

    def switchturn(self, turnboard=False):
        self.players[self.turn].checked = False
        if self.turn == 0:
            self.turn = 1
        elif self.turn == 1:
            self.turn = 0
        else:
            raise ValueError("Failed changing turn")
        self.turnVar.set(f"{self.players[self.turn].color.capitalize()}'s turn")
        self.update_available_moves_for_all_pieces()
        players_turn: Player = self.players[self.turn]
        if players_turn.checked:
            if len(players_turn.king.available_moves) == 0:
                self.change_checklabel(False, "Checkmate")
                players_turn.checkmate = True
            else:
                self.change_checklabel(False, "Check")
        if (not self.players[0].AI and not self.players[1].AI) or turnboard:
            self.turn_chessboard()
        if players_turn.AI:
            self.AI_move()
        elif players_turn.online:
            self.get_online_move()


    def turn_chessboard(self):
        tup = ("white", "black")
        current_color = self.chessboard.direction
        for color in tup:
            if color != current_color:
                other_color = color
                break
        self.canvas.delete("all")
        self.chessboard = ChessBoard(self.canvas, self.smaller_length, other_color)
        for player in self.players:
            for piece in player.pieces:
                piece.draw_new(self.chessboard.route(piece.routepos))

    def add_player(self, player: Player):
        if len(self.players) == 2:
            print("\t> Can't add more players")
        else:
            if player.color == "white":
                self.players.insert(0, player)
            else:
                self.players.append(player)

    def get_player(self, color: str):
        for player in self.players:
            if player.color == color:
                return player

    def get_piece_at_route(self, route: str):
        piece: ChessPiece = self.routes_dict.get(route)
        return piece

    def is_piece_at_route(self, route: str):
        piece = self.routes_dict[route]
        if piece is not None:
            return True
        else:
            return False

    def set_routevalue(self, route, piece: ChessPiece or None):
        self.routes_dict[route] = piece

    def update_available_moves_for_all_pieces(self):
        kings = []
        for player in self.players:
            for piece in player.pieces:
                if piece.piece == "king":
                    kings.append(piece)
                piece.update_available_moves()
        for king in kings:
            king.remove_kings_checkmoves()

    def setup(self):
        self.add_player(Player(self, "white"))
        self.add_player(Player(self, "black"))
        for player in self.players:
            player.add_all_pieces()

        self.update_available_moves_for_all_pieces()

    def get_online_move(self):
        HOST = "172.0.0.1"
        PORT = 12345

        with socket.socket() as s:
            s.settimeout(600)
            s.connect((HOST, PORT))

    def AI_move(self):
        ai = AI(self, self.players[self.turn])


class AI:
    def __init__(self, system: Game, player: Player):
        self.system = system
        self.player = player
        self.opponent = self.player.get_other_player()
        self.player_copy = player.copy()
        self.opponent_copy = self.opponent.copy()

    def best_move(self):
        pass


class Gui:
    def __init__(self):
        self.hovedvindu = tkinter.Tk()
        self.windowWidth = 600
        self.windowHeigth = 600
        self.canvas = tkinter.Canvas(self.hovedvindu, width=self.windowWidth, height=self.windowHeigth)
        self.canvas.grid(row=1, column=0)
        self.hovedvindu.update()

        self.system = Game(self.hovedvindu, self.canvas)
        self.hovedvindu.resizable(width=False, height=False)
        self.hovedvindu.title("Chess")

        self.piece_held = None
        self.mousepos = [10, 10]
        self.canvas.bind("<Button-1>", self.pick_up_piece)
        self.canvas.bind("<B1-Motion>", self.moving_mouse)
        self.canvas.bind("<ButtonRelease-1>", self.set_piece_down)

        tkinter.mainloop()

    def pick_up_piece(self, event):
        self.mousepos = [event.x, event.y]
        closestroute = self.system.chessboard.closest_route([event.x, event.y])
        piece = self.system.get_piece_at_route(closestroute)
        players_turn = self.system.players[self.system.turn]
        if players_turn.checked and not players_turn.checkmate:
            self.system.change_checklabel(True)
        if piece is None or players_turn.color != piece.color or players_turn.AI or players_turn.checkmate:
            return
        self.piece_held = piece
        for route in self.piece_held.available_moves:
            self.system.chessboard.add_colored_route(route, "red")
        self.canvas.after(15, self.moving_piece)

    def moving_piece(self):
        if self.piece_held is not None:
            self.piece_held.soft_move(self.mousepos)
            self.canvas.after(15, self.moving_piece)

    def moving_mouse(self, event):
        self.mousepos = [event.x, event.y]

    def set_piece_down(self, event):
        if self.piece_held is not None:
            route = self.system.chessboard.closest_route([event.x, event.y])
            piece = self.system.routes_dict[route]
            if route in self.piece_held.available_moves:
                self.piece_held.move(route)
                if piece is not None:
                    piece.remove()
            else:
                self.piece_held.soft_move(self.system.chessboard.route(self.piece_held.routepos))
            self.system.chessboard.clear_colored_routes()
            self.piece_held = None


if __name__ == '__main__':
    gui = Gui()
