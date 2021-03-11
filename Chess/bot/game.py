import pygame
import chessApi
import board


class Game:
    def __init__(self):
        board_list = chessApi.getStartBoard()
        self.board = board.ChessBoard(board_list)

        self.selected_route = None

    def mouse_down(self, route_pos):
        if self.selected_route is None:
            self.selected_route = route_pos
            moves = chessApi.getAvailableMoves(self.board.list_board, route_pos)
            print(moves)
            # display_legal_moves()
        else:
            # chessApi.move_if_legal(from, to)
            self.selected_route = None

