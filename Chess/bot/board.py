from typing import Union, List
import piece


class ChessBoard:
    def __init__(self, board: Union[List[int], int]):
        if isinstance(board, int):
            self.__board: int = board
        elif isinstance(board, list):
            self.__board = self.list_to_int_format(board)
        else:
            raise TypeError(f"ChessBoard can't be initialized with a {type(board)} type")

    @property
    def int_board(self):
        return self.__board

    @int_board.setter
    def int_board(self, value):
        self.__board = value

    @property
    def list_board(self):
        return self.int_to_list_format(self.__board)

    @list_board.setter
    def list_board(self, value):
        self.__board = self.list_to_int_format(value)

    @staticmethod
    def list_to_int_format(list_board: List[int]):
        if len(list_board) != 64:
            raise ValueError(f"Board can't have {len(list_board)} fields")

        int_board: int = 0
        for index, route in enumerate(list_board):
            int_board += route << (piece.BITLENGTH * index)
        return int_board

    @staticmethod
    def int_to_list_format(int_board: int):
        list_board: [int] = []
        for i in range(64):
            list_board.append(int_board & pow(2, piece.BITLENGTH) - 1)
            int_board >>= piece.BITLENGTH

        if len(list_board) != 64:
            raise ValueError(f"Board can't have {len(list_board)} fields")
        return list_board

    def __iter__(self):
        return iter(_ChessBoardIter(self))


class _ChessBoardIter:
    def __init__(self, chessBoard: ChessBoard):
        self.board = chessBoard.int_board
        self.pos = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.pos >= 64:
            raise StopIteration
        route = self.board & (pow(2, piece.BITLENGTH) - 1)
        self.board >>= piece.BITLENGTH
        self.pos += 1
        return route
