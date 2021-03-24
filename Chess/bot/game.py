import pygame
import chessApi
import board
from piece import Color, get_piece_color, getPiece


class SelectedRoute:
    def __init__(self, chessboard, route_no):
        self.route_no = route_no
        self.available_moves = chessApi.getAvailableMoves(chessboard, route_no)


class Game:
    def __init__(self):
        # board_list = chessApi.getStartBoard()
        # board_list = chessApi.getExampleBoard(piece.Color.white | piece.Pieces.king, 36)
        board_list = [4, 0, 0, 0, 6, 0, 0, 4, 1, 3, 1, 1, 5, 1, 1, 1, 0, 1, 2, 3, 1, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 11, 0, 9, 0, 0, 0, 10, 13, 9, 9, 0, 10, 0, 0, 9, 9, 0, 11, 0, 9, 9, 9, 12, 0, 0, 0, 14, 0, 0, 12]
        # board_list = 934518772647114197112938351362149484002244967819837885914675392910601678180483530194841010962432
        self.board = board.ChessBoard(board_list)
        self.selected_route: SelectedRoute = None
        self.turn = Color.white
        self.bots = []
        self.bot_depth = 4

    def next_turn(self):
        self.turn = Color.black - self.turn

    def mouse_down(self, route_no):
        if self.selected_route is None or not self.selected_route.available_moves:
            if get_piece_color(getPiece(route_no, self.board)) == self.turn or True:
                self.selected_route = SelectedRoute(self.board, route_no)
        else:
            tmpboard = self.board.int_board
            self.board.list_board = chessApi.movePiece(self.board, self.selected_route.route_no, route_no)
            print(self.board.list_board)
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
