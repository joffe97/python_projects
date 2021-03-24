//
// Created by Joach on 06.03.2021.
//

#include "board.h"
#include "pieces.h"

void initBoard(int *board) {
    for (int i = 0; i < 64; i++) {
        board[i] = 0;
    }
}

void initStartBoard(int *board) {
    initBoard(board);
    for (int i = 8; i < 16; i++) {
        board[i] = PAWN;
        board[63 - i] = PAWN;
    }
    board[0] = board[7] = board[56] = board[63] = ROOK;
    board[1] = board[6] = board[57] = board[62] = KNIGHT;
    board[2] = board[5] = board[58] = board[61] = BISHOP;
    board[3] = board[59] = QUEEN;
    board[4] = board[60] = KING;

    for (int i = 0; i < 16; i++) {
        board[i] |= WHITE;
        board[63 - i] |= BLACK;
    }
}

void initExampleBoard(int *board, int piece, int route_no) {
    initBoard(board);
    board[route_no] = piece;
}

int getColumn(int route_no) {
    return route_no % 8;
}

int getRow(int route_no) {
    return route_no / 8;
}

int getRouteNo(int column, int row) {
    return row * 8 + column;
}

int getKingRouteNo(int *board, int color) {
    int tmpPiece;
    for (int i = 0; i < 64; i++) {
        tmpPiece = getPiece(board, i);
        if (tmpPiece && getPieceType(tmpPiece) == KING && getPieceColor(tmpPiece) == color) {
            return i;
        }
    }
    return -1;
}

void copyBoard(int *from_board, int *to_board) {
    for (int i = 0; i < 64; i++) {
        to_board[i] = from_board[i];
    }
}
