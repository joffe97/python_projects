import pygame
import math
import piece
import game
from pieceImages import PieceImages


COLOR_WHITE = pygame.Color(232, 235, 239)
COLOR_BLACK = pygame.Color(125, 135, 150)
COLOR_RED = pygame.Color(255, 0, 0)


class Graphics:
    def __init__(self):
        self.board_size = 800
        self.fps = 10

        pygame.init()
        pygame.display.set_caption("Chess")
        self.screen = pygame.display.set_mode([self.board_size, self.board_size])

        self.game = game.Game()
        self.piece_images = PieceImages(self.route_size)

    @property
    def route_size(self):
        return self.board_size // 8

    def game_loop(self):
        run = True
        clock = pygame.time.Clock()

        while run:
            clock.tick(self.fps)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.game.mouse_down(self.get_clicked_route())

            self.redraw_window()

    def redraw_window(self):
        self.draw_chessboard()
        self.draw_chesspieces()
        self.draw_available_moves()
        pygame.display.update()

    def draw_chessboard(self):
        for y in range(8):
            for x in range(8):
                color = COLOR_WHITE if (x + y) % 2 == 0 else COLOR_BLACK
                pygame.draw.rect(self.screen, color, self.get_route_rect_coords(x, y))

    def draw_chesspieces(self):
        for index, route in enumerate(self.game.board):
            _, is_black, piece_type = piece.get_piece_data(route)
            if piece_type == 0:
                continue
            x, y = self.get_routeno_coords(index)
            img = self.piece_images.get_img(is_black, piece_type)
            self.screen.blit(img, self.get_route_topleft(x, y))

    def draw_available_moves(self):
        selected = self.game.selected_route
        if selected is None:
            return
        # print()
        for move in selected.available_moves:
            x, y = self.get_routeno_coords(move)
            # print(f"{x}, {y}")
            a, b, c, d = self.get_route_rect_coords(x, y)
            # print(f"{a},{b},{c},{d}")
            pygame.draw.rect(self.screen, COLOR_RED, self.get_route_rect_coords(x, y), 3)

    def blit_middle(self, img: pygame.surface.Surface, middle_pos: tuple[int, int]):
        topleft_pos = middle_pos[0] - self.route_size // 2, middle_pos[1] - self.route_size // 2
        self.screen.blit(img, topleft_pos)

    def get_route_rect_coords(self, x: int, y: int):
        return (x * self.route_size,
                y * self.route_size,
                self.route_size,
                self.route_size)

    @staticmethod
    def get_routeno_coords(route_no: int):
        return route_no % 8, 7 - (route_no // 8)

    def get_route_topleft(self, x: int, y: int):
        return (x * self.route_size,
                y * self.route_size)

    def get_clicked_route_coords(self):
        pos = pygame.mouse.get_pos()
        relpos = []
        for d in range(2):
            route_d = math.floor(pos[d] / self.route_size)
            if route_d < 0:
                route_d = 0
            elif route_d > 7:
                route_d = 7
            relpos.append(route_d)
        return relpos[0], 7 - relpos[1]

    def get_clicked_route(self):
        x, y = self.get_clicked_route_coords()
        return x + y * 8


if __name__ == '__main__':
    Graphics().game_loop()

