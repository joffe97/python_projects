//
// Created by Joach on 06.03.2021.
//

#include <stdlib.h>

#include "pieces.h"
#include "board.h"

extern inline int S_to_binary_(const char *s)
{
    int i = 0;
    while (*s) {
        i <<= 1;
        i += *s++ - '0';
    }
    return i;
}

int myPow(int x, int n) {
    int number = 1;
    for (int i = 0; i < n; i++) {
        number *= x;
    }
    return(number);
}

extern inline int getPiece(int *board, int route_no) {
    return board[route_no];
}

extern inline int isEmptyRoute(int *board, int route_no) {
    return !getPiece(board, route_no);
}

extern inline int getPieceType(int piece) {
    return piece & B(00111);
}

extern inline int getPieceColor(int piece) {
    return piece & B(01000);
}

extern inline int pieceIsSpecial(int piece) {
    return piece & B(10000);
}

void setPieceToSpecial(int *board, int route_no) {
    board[route_no] = (board[route_no] & B(01111)) + B(10000);
}

void setPieceToUnspecial(int *board, int route_no) {
    board[route_no] = (board[route_no] & B(01111));
}

extern inline int isLegalRoute(int route_no) {
    return (route_no <= 0 && route_no < 64);
}

extern inline int isLegalRouteCoords(int x, int y) {
    return (x >= 0 && x < 8 && y >= 0 && y < 8);
}


int isLegalMove(int *board, int from_route, int to_route) {
    int legalMoves[32], move;
    getAvailableMoves(legalMoves, board, from_route);
    for (int i = 0; i < 32; i++) {
        move = legalMoves[i];
        if (move == -1) break;
        else if (move == to_route) return 1;
    }
    return 0;
}

void handlePawnMove(int *board, int from_route, int to_route) {
    int x1, x2, y1, y2, yDelta, route;
    x1 = getColumn(from_route);
    x2 = getColumn(to_route);
    y1 = getRow(from_route);
    y2 = getRow(to_route);

    if (y2 == 0 || y2 == 7) {
        board[from_route] = (B(01000) & board[from_route]) + QUEEN;
        return;
    }

    yDelta = (y1-y2) >= 0 ? (y1-y2) : -(y1-y2);
    if (yDelta >= 2) {
        setPieceToSpecial(board, from_route);
    } else if (x1 != x2 && isEmptyRoute(board, to_route)) {
        route = getRouteNo(x2, y1);
        board[route] = 0;
    }
}

void handleKingMove(int *board, int from_route, int to_route) {
    int piece = getPiece(board, from_route);

    if (!pieceIsSpecial(piece)) {
        setPieceToSpecial(board, from_route);

        int y, x1, x2, xDelta, isKingside, rook_route, old_rook_route, rook;
        y = getRow(from_route);
        x1 = getColumn(from_route);
        x2 = getColumn(to_route);
        isKingside = (x2-x1) > 0;
        xDelta = (x1-x2) >= 0 ? (x1-x2) : -(x1-x2);
        if (xDelta > 1) {
            rook_route = getRouteNo(x2 + (isKingside ? -1 : 1), y);
            old_rook_route = getRouteNo(isKingside ? 7 : 0, y);
            rook = getPiece(board, old_rook_route);
            board[rook_route] = rook;
            board[old_rook_route] = 0;
        }
    }
}

void removeAllPassantPawns(int *board) {
    for (int row = 3; row <= 4; row++) {
        for (int col = 0; col <= 7; col++) {
            int route = getRouteNo(col, row);
            int piece = getPiece(board, route);
            if (getPieceType(piece) == PAWN) {
                setPieceToUnspecial(board, route);
            }
        }
    }
}

void movePiece(int *board, int from_route, int to_route) {
    if (!isLegalMove(board, from_route, to_route)) return;

    removeAllPassantPawns(board);

    int piece, type;
    piece = getPiece(board, from_route);
    type = getPieceType(piece);
    switch (type) {
        case PAWN:
            handlePawnMove(board, from_route, to_route);
            break;
        case KING:
            handleKingMove(board, from_route, to_route);
            break;
        case ROOK:
            setPieceToSpecial(board, from_route);
    }
    board[to_route] = board[from_route];
    board[from_route] = 0;
}


int addPosIfEmpty(int *dest, int *destsize, int *board, int route_no) {
    if (isEmptyRoute(board, route_no)) {
        dest[*destsize] = route_no;
        (*destsize)++;
        return 1;
    } else {
        return 0;
    }
}

int addPosIfNotOwnColor(int *dest, int *destsize, int *board, int route_no, int color) {
    int piece = getPiece(board, route_no);

    if (piece && getPieceColor(piece) != color) {
        dest[*destsize] = route_no;
        (*destsize)++;
        return 1;
    } else {
        return 0;
    }
}

int addPosIfEmptyOrNotOwnColor(int *dest, int *destsize, int *board, int route_no, int color, int *isOpponent) {
    int piece = getPiece(board, route_no);
    if (isOpponent) *isOpponent = 0;

    if (piece) {
        if (getPieceColor(piece) == color) {
            return 0;
        } else if (isOpponent) {
            *isOpponent = 1;
        }
    }
    dest[*destsize] = route_no;
    (*destsize)++;
    return 1;
}

void getDiagonalMoves(int *dest, int *destsize, int *board, int route_no, int includeOwnColor) {
    int piece = getPiece(board, route_no);
    int color = getPieceColor(piece);
    int row = getRow(route_no);
    int column = getColumn(route_no);
    int targetRoute, radius, x, y, isOpponent, added;
    isOpponent = 0;

    for (int xrel = -1; xrel <= 1; xrel += 2) {
        for (int yrel = -1; yrel <= 1; yrel += 2) {
            for (radius = 1; radius < 8; radius++) {
                x = column + (radius * xrel);
                y = row + (radius * yrel);
                if (!isLegalRouteCoords(x, y)) break;
                targetRoute = getRouteNo(x, y);
                added = addPosIfEmptyOrNotOwnColor(dest, destsize, board, targetRoute, color, &isOpponent);
                if (!added) {
                    if (includeOwnColor) {
                        dest[*destsize] = targetRoute;
                        (*destsize)++;
                    }
                    break;
                }
                if (isOpponent) break;
            }
        }
    }
    dest[*destsize] = -1;
}

void getStraightMoves(int *dest, int *destsize, int *board, int route_no, int includeOwnColor) {
    int piece = getPiece(board, route_no);
    int color = getPieceColor(piece);
    int row = getRow(route_no);
    int column = getColumn(route_no);
    int targetRoute, radius, x, y, isOpponent, added;
    isOpponent = 0;

    for (int isX = 0; isX <= 1; isX++) {
        for (int rel = -1; rel <= 1; rel += 2) {
            for (radius = 1; radius < 8; radius++) {
                x = column + (radius * isX * rel);
                y = row + (radius * !isX * rel);
                if (!isLegalRouteCoords(x, y)) break;
                targetRoute = getRouteNo(x, y);
                added = addPosIfEmptyOrNotOwnColor(dest, destsize, board, targetRoute, color, &isOpponent);
                if (!added) {
                    if (includeOwnColor) {
                        dest[*destsize] = targetRoute;
                        (*destsize)++;
                    }
                    break;
                }
                if (isOpponent) break;
            }
        }
    }
    dest[*destsize] = -1;
}

void getAvailableMovesPawn(int *dest, int *board, int route_no, int includeOwnColor) {
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

        targetRoute = getRouteNo(targetCol, targetRow);  // Passant
        if (targetRow < 0 || targetRow > 7) {
            continue;
        }

        int passantPiece = getPiece(board, getRouteNo(targetCol, row));
        if (getPieceType(passantPiece) == PAWN && pieceIsSpecial(passantPiece)) {
            addPosIfEmpty(dest, &destsize, board, targetRoute);
        }

        addPosIfNotOwnColor(dest, &destsize, board, targetRoute, color);
    }
    dest[destsize] = -1;
}

void getAvailableMovesKnight(int *dest, int *board, int route_no, int includeOwnColor) {
    int piece = getPiece(board, route_no);
    int color = getPieceColor(piece);
    int row = getRow(route_no);
    int column = getColumn(route_no);
    int destsize = 0;
    int targetRoute, xlen, ylen, x, y, isOpponent, added;

    /*  x | y
     * -1, -2
     * -1, +2
     * +1, -2
     * +1, +2
     * -2, -1
     * -2, +1
     * +2, -1
     * +2, +1
     */

    for (xlen = 1; xlen <= 2; xlen++) {
        ylen = 3 - xlen;
        for (int i = 1; i <= 4; i++) {
            x = column + xlen * ((2 * (i > 2)) - 1);
            y = row + ylen * (myPow(-1, i));
            if (!isLegalRouteCoords(x, y)) continue;
            targetRoute = getRouteNo(x, y);
            added = addPosIfEmptyOrNotOwnColor(dest, &destsize, board, targetRoute, color, &isOpponent);
            if (!added && includeOwnColor) {
                dest[destsize] = targetRoute;
                (destsize)++;
            }
        }
    }
    dest[destsize] = -1;
}

void getAvailableMovesBishop(int *dest, int *board, int route_no, int includeOwnColor) {
    int destsize = 0;
    getDiagonalMoves(dest, &destsize, board, route_no, includeOwnColor);
}

void getAvailableMovesRook(int *dest, int *board, int route_no, int includeOwnColor) {
    int destsize = 0;
    getStraightMoves(dest, &destsize, board, route_no, includeOwnColor);
}

void getAvailableMovesQueen(int *dest, int *board, int route_no, int includeOwnColor) {
    int destsize = 0;
    getDiagonalMoves(dest, &destsize, board, route_no, includeOwnColor);
    getStraightMoves(dest, &destsize, board, route_no, includeOwnColor);
}

int isAttackedBy(int *moves, int *board, int *attackedByType, int color) {
    int route, piece, pieceType, type;
    for (int i = 0; i < 32; i++) {
        route = moves[i];
        if (isLegalRoute(route)) break;
        else if (isEmptyRoute(board, route)) continue;
        piece = getPiece(board, route);
        if (getPieceColor(piece) == color) continue;
        pieceType = getPieceType(piece);
        for (int j = 0; j < 7; j++) {
            type = attackedByType[j];
            if (type == -1) break;
            else if (pieceType == type) return 1;
        }
    }
    return 0;
}

int isLegalKingRoute(int *boardWithKing, int targetRoute, int includeOwnColor, int kingRoute) {
    int board[64];
    copyBoard(boardWithKing, board);
    board[kingRoute] = 0;

    int kingColor = getPieceColor(getPiece(boardWithKing, kingRoute));

    if (!includeOwnColor && !isEmptyRoute(board, targetRoute)) {
        int piece = getPiece(board, targetRoute);
        if (getPieceColor(piece) == kingColor) {
            return 0;
        }
    }

    int dest[32];

    getAvailableMovesRook(dest, board, targetRoute, 1);
    int pieceTypes[3] = {QUEEN, ROOK, -1};
    if (isAttackedBy(dest, board, pieceTypes, kingColor)) return 0;

    getAvailableMovesBishop(dest, board, targetRoute, 1);
    pieceTypes[1] = BISHOP;
    if (isAttackedBy(dest, board, pieceTypes, kingColor)) return 0;

    pieceTypes[1] = -1;

    getAvailableMovesKnight(dest, board, targetRoute, 1);
    pieceTypes[0] = KNIGHT;
    if (isAttackedBy(dest, board, pieceTypes, kingColor)) return 0;

    int row, column, destsize, route, x, y;
    destsize = 0;
    row = getRow(targetRoute);
    column = getColumn(targetRoute);

    for (int xrel = -1; xrel <= 1; xrel++) {
        for (int yrel = -1; yrel <= 1; yrel++) {
            if (!(xrel || yrel)) continue;
            x = column + xrel;
            y = row + yrel;
            if (!isLegalRouteCoords(x, y)) continue;
            route = getRouteNo(x, y);
            dest[destsize] = route;
            destsize++;
        }
    }
    dest[destsize] = -1;

    pieceTypes[0] = KING;
    if (isAttackedBy(dest, board, pieceTypes, kingColor)) return 0;
 
    int direction;
    destsize = 0;
    direction = (kingColor == WHITE) * 2 - 1;

    for (int i = -1; i <= 1; i += 2) {
        x = column + i;
        y = row + direction;
        if (!isLegalRouteCoords(x, y)) continue;
        route = getRouteNo(x, y);
        dest[destsize] = route;
        destsize++;
    }
    dest[destsize] = -1;
    pieceTypes[0] = PAWN;
    if (isAttackedBy(dest, board, pieceTypes, kingColor)) return 0;

    return 1;
}

int isLegalCastle(int *board, int isKingside, int color) {
    int firstLine = (color == BLACK) * 7;
    int kingCol = 4;
    int xrel_dir = isKingside ? 1 : -1;
    int targetRoute, rook;

    targetRoute = getRouteNo(isKingside ? 7 : 0, firstLine);
    rook = getPiece(board, targetRoute);

    if (!getPieceType(rook) == ROOK || pieceIsSpecial(rook) || (!isKingside && !isEmptyRoute(board, getRouteNo(1, firstLine)))) return 0;

    for (int i = 1; i <= 2; i++) {
        targetRoute = getRouteNo(kingCol + (i * xrel_dir), firstLine);
        if (!isEmptyRoute(board, targetRoute) || !isLegalKingRoute(board, targetRoute, 0, getRouteNo(kingCol, firstLine))) return 0;
    }

    return 1;
}

void getAvailableMovesKing(int *dest, int *board, int route_no, int includeOwnColor) {
    int piece = getPiece(board, route_no);
    int color = getPieceColor(piece);
    int row = getRow(route_no);
    int column = getColumn(route_no);
    int destsize = 0;
    int targetRoute, x, y;

    for (int xrel = -1; xrel <= 1; xrel++) {
        for (int yrel = -1; yrel <= 1; yrel++) {
            if (!(xrel || yrel)) continue;
            x = column + xrel;
            y = row + yrel;
            if (!isLegalRouteCoords(x, y)) continue;
            targetRoute = getRouteNo(x, y);
            if (!isLegalKingRoute(board, targetRoute, includeOwnColor, route_no)) continue;
            dest[destsize] = targetRoute;
            destsize++;
        }
    }

    if (!pieceIsSpecial(piece) && isLegalKingRoute(board, route_no, 1, route_no)) {
        if (isLegalCastle(board, 1, color)) {
            dest[destsize] = getRouteNo(column + 2, row);
            destsize++;
        }
        if (isLegalCastle(board, 0, color)) {
            dest[destsize] = getRouteNo(column - 2, row);
            destsize++;
        }
    }

    dest[destsize] = -1;
}

void getAvailableMoves(int *dest, int *board, int route_no) {
    int piece = getPiece(board, route_no);
    switch (getPieceType(piece)) {
        case PAWN:
            getAvailableMovesPawn(dest, board, route_no, 0);
            break;
        case KNIGHT:
            getAvailableMovesKnight(dest, board, route_no, 0);
            break;
        case BISHOP:
            getAvailableMovesBishop(dest, board, route_no, 0);
            break;
        case ROOK:
            getAvailableMovesRook(dest, board, route_no, 0);
            break;
        case QUEEN:
            getAvailableMovesQueen(dest, board, route_no, 0);
            break;
        case KING:
            getAvailableMovesKing(dest, board, route_no, 0);
            break;
        default:
            dest[0] = -1;
    }
}

void getAvailableMovesNoCheck(int *dest, int *board, int route_no) {
    // TODO: Not tested!
    int piece, color, kingRoute, availableMoves[32], toRoute, toPiece, isLegal, destsize;

    destsize = 0;
    piece = getPiece(board, route_no);
    color = getPieceColor(piece);
    kingRoute = getKingRouteNo(board, color);

    getAvailableMoves(availableMoves, board, route_no);
    
    for (int i = 0; i < 32; i++) {
        toRoute = availableMoves[i];
        if (toRoute == -1) break;
        
        toPiece = getPiece(board, toRoute);
        board[toRoute] = board[route_no];
        board[route_no] = 0;
        isLegal = isLegalKingRoute(board, kingRoute, 1, kingRoute);
        board[route_no] = board[toRoute];
        board[toRoute] = toPiece;
        
        if (isLegal) {
            dest[destsize] = toRoute;
            destsize++;
        }
    }
}

