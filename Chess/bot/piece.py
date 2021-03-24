from enum import IntEnum
BITLENGTH = 5


class Pieces(IntEnum):
    pawn = 1    # 001
    knight = 2  # 010
    bishop = 3  # 011
    rook = 4    # 100
    queen = 5   # 101
    king = 6    # 110

    @staticmethod
    def get_piece_name(piece: int):
        return Pieces(piece).name

    @staticmethod
    def get_piece_letter(piece: int):
        if piece == Pieces.knight:
            return "N"
        name = Pieces(piece).name
        return name[0].upper()


class Color(IntEnum):
    white = 0       # 0000
    black = 1 << 3  # 1000


def get_piece_data(piece: int):
    special = (piece & (1 << 4)) // 0x10
    color = (piece & (1 << 3)) // 0x08
    piece_type = piece & 7
    return special, color, piece_type


def get_piece_color(piece: int):
    return piece & (1 << 3)


def getRouteBit(field_no, piece):
    return piece << (BITLENGTH * field_no)


def getPiece(field_no, board):
    board = board.int_board
    return (((pow(2, BITLENGTH) - 1) << field_no * BITLENGTH) & board) >> field_no * BITLENGTH    # (11111 << (0 * 5)) & 0111001001

