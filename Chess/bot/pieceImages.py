import pygame
import piece


class PieceImages(list):
    def __init__(self, img_size):
        super().__init__()
        for is_black in range(2):
            for route in range(1, 7):
                img_name = f"images/pieces/{'b' if is_black else 'w'}{piece.Pieces.get_piece_letter(route)}.png"
                img = pygame.image.load(img_name)
                self.append(pygame.transform.scale(img, (img_size, img_size)))

    def get_img(self, is_black: int, piece_type: int):
        return self[is_black * 6 + piece_type - 1]
