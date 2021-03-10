import board
import piece
import chessApi
a = chessApi.getStartBoard()
print(a)
b = board.ChessBoard(a)
print(piece.Pieces.get_piece_letter(1))
