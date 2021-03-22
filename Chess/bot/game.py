import pygame
import chessApi
import board
from piece import Color


class SelectedRoute:
    def __init__(self, chessboard, route_no):
        self.route_no = route_no
        self.available_moves = chessApi.getAvailableMoves(chessboard, route_no)


class Game:
    def __init__(self):
        board_list = chessApi.getStartBoard()
        # board_list = chessApi.getExampleBoard(piece.Color.white | piece.Pieces.king, 36)
        # board_list = [4, 2, 3, 5, 6, 0, 0, 4, 1, 1, 1, 1, 0, 1, 1, 1, 0, 0, 0, 3, 1, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 9, 9, 9, 9, 9, 9,     9, 9, 12, 10, 11, 13, 14, 11, 10, 12]
        self.board = board.ChessBoard(board_list)
        self.selected_route: SelectedRoute = None
        self.turn = Color.white
        self.bots = [Color.black]
        self.bot_depth = 4

    def next_turn(self):
        self.turn = Color.black - self.turn

    def mouse_down(self, route_no):
        if self.selected_route is None or not self.selected_route.available_moves:
            self.selected_route = SelectedRoute(self.board, route_no)
        else:
            tmpboard = self.board.int_board
            self.board.list_board = chessApi.movePiece(self.board, self.selected_route.route_no, route_no)
            # move = chessApi.getBestMove(self.board.list_board, 3, Color.black)
            # print(move)
            #self.board.list_board = chessApi.movePiece(self.board.list_board, move[0], move[1])
            self.selected_route = None
            if tmpboard != self.board.int_board:
                self.next_turn()

    def bot_move(self):
        if self.turn not in self.bots:
            return
        move = chessApi.getBestMove(self.board.list_board, self.bot_depth, self.turn)
        self.board.list_board = chessApi.movePiece(self.board.list_board, move[0], move[1])
        self.next_turn()
