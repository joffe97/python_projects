//
// Created by Joach on 06.03.2021.
//

#ifndef CHESSAPI_PIECES_H
#define CHESSAPI_PIECES_H

#define B(x) S_to_binary_(#x)

#define PAWN 1
#define KNIGHT 2
#define BISHOP 3
#define ROOK 4
#define QUEEN 5
#define KING 6

#define WHITE 0
#define BLACK 1 << 3

void movePiece(int *board, int from_route, int to_route);
void getAvailableMoves(int *dest, int *board, int route_no);

int getPiece(int *board, int route);
int getPieceType(int piece);
int getPieceColor(int piece);

#endif //CHESSAPI_PIECES_H
