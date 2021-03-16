//
// Created by Joach on 06.03.2021.
//

#include "pieces.h"
#include "board.h"

static inline int S_to_binary_(const char *s)
{
    int i = 0;
    while (*s) {
        i <<= 1;
        i += *s++ - '0';
    }
    return i;
}

void movePiece(int *board, int from_route, int to_route) {
    board[to_route] = board[from_route];
    board[from_route] = 0;
}

int getPiece(int *board, int route_no) {
    return board[route_no];
}

int isEmptyRoute(int *board, int route_no) {
    return !getPiece(board, route_no);
}

int getPieceType(int piece) {
    return piece & B(00111);
}

int getPieceColor(int piece) {
    return piece & B(01000);
}

int pieceIsBlack(int piece) {
    return piece & BLACK;
}

int pieceIsWhite(int piece) {
    return !pieceIsBlack(piece);
}

int pieceIsSpecial(int piece) {
    return piece & B(10000) ? 1 : 0;
}


int addPosIfEmpty(int *dest, int *destsize, int *board, int route_no) {
    if (isEmptyRoute(board, route_no)) {
        dest[(*destsize)++] = route_no;
        return 1;
    } else {
        return 0;
    }
}

int addPosIfNotOwnColor(int *dest, int *destsize, int *board, int route_no, int color) {
    int piece = getPiece(board, route_no);

    if (piece && getPieceColor(piece) != color) {
        dest[(*destsize)++] = route_no;
        return 1;
    } else {
        return 0;
    }
}

int addPosIfEmptyOrNotOwnColor(int *dest, int *destsize, int *board, int route_no, int color, int *isOpponent) {
    int piece = getPiece(board, route_no);
    *isOpponent = 0;

    if (piece) {
        if (getPieceColor(piece) == color) {
            return 0;
        } else {
            *isOpponent = 1;
        }
    }
    dest[(*destsize)++] = route_no;
    return 1;
}

void getAvailableMovesPawn(int *dest, int *board, int route_no) {
    int piece = getPiece(board, route_no);
    int color = getPieceColor(piece);
    int direction = (color == WHITE) * 2 - 1;
    int row = getRow(route_no);
    int column = getColumn(route_no);
    int destsize = 0;
    int targetRoute;

    targetRoute = getRouteNo(column, row + direction);
    if (addPosIfEmpty(dest, &destsize, board, targetRoute)) {
        if (row == ((color == WHITE) ? 1 : 6)) {
            targetRoute = getRouteNo(column, row + (2 * direction));
            addPosIfEmpty(dest, &destsize, board, targetRoute);
        }
    }

    for (int attackDir = -1; attackDir <= 1; attackDir += 2) {
        int targetCol = column + attackDir;
        int targetRow = row + direction;
        if (targetCol < 0 || targetCol > 7) {
            continue;
        }
        targetRoute = getRouteNo(targetCol, row);  // Passant
        int passantPiece = getPiece(board, targetRoute);
        if (getPieceType(passantPiece) == PAWN && pieceIsSpecial(passantPiece)) {
            addPosIfNotOwnColor(dest, &destsize, board, targetRoute, getPieceColor(piece));
        }

        if (targetRow < 0 || targetRow > 7) {
            continue;
        }
        targetRoute = getRouteNo(targetCol, targetRow);
        addPosIfNotOwnColor(dest, &destsize, board, targetRoute, getPieceColor(piece));
    }
    dest[destsize] = -1;
}

void getAvailableMovesKnight(int *dest, int *board, int route_no) {
    int piece = getPiece(board, route_no);
}

void getAvailableMovesBishop(int *dest, int *board, int route_no) {
    int piece = getPiece(board, route_no);
}

void getAvailableMovesRook(int *dest, int *board, int route_no) {
    int piece = getPiece(board, route_no);
}

void getAvailableMovesQueen(int *dest, int *board, int route_no) {
    int piece = getPiece(board, route_no);
}

void getAvailableMovesKing(int *dest, int *board, int route_no) {
    int piece = getPiece(board, route_no);
}

void getAvailableMoves(int *dest, int *board, int route_no) {
    int piece = getPiece(board, route_no);
    switch (getPieceType(piece)) {
        case PAWN:
            getAvailableMovesPawn(dest, board, route_no);
            break;
        case KNIGHT:
            getAvailableMovesKnight(dest, board, route_no);
            break;
        case BISHOP:
            getAvailableMovesBishop(dest, board, route_no);
            break;
        case ROOK:
            getAvailableMovesRook(dest, board, route_no);
            break;
        case QUEEN:
            getAvailableMovesQueen(dest, board, route_no);
            break;
        case KING:
            getAvailableMovesKing(dest, board, route_no);
            break;
    }
}

