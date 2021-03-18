import pygame
import chessApi
import board
import piece


class SelectedRoute:
    def __init__(self, chessboard, route_no):
        self.route_no = route_no
        self.available_moves = chessApi.getAvailableMoves(chessboard, route_no)


class Game:
    def __init__(self):
        board_list = chessApi.getStartBoard()
        # board_list = chessApi.getExampleBoard(piece.Color.white | piece.Pieces.king, 36)
        # board_list = [4, 2, 3, 5, 0, 3, 2, 4, 1, 1, 1, 1, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 6, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 9, 9, 9, 9, 9, 9, 9, 9, 12, 10, 11, 13, 14, 11, 10, 12]
        self.board = board.ChessBoard(board_list)

        self.selected_route: SelectedRoute = None

    def mouse_down(self, route_no):
        if self.selected_route is None or not self.selected_route.available_moves:
            self.selected_route = SelectedRoute(self.board, route_no)
        else:
            # chessApi.move_if_legal(from, to)
            self.board = chessApi.movePiece(self.board, self.selected_route.route_no, route_no)
            print(self.board)
            print(route_no)
            self.selected_route = None
