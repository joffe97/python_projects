//
// Created by Joachim on 15.03.2021.
//

#include <stdio.h>
#include <stdlib.h>

#include "pieces.h"
#include "board.h"

int main(int argc, char *argv[]) {
    int /*board[64], */availableMoves[32], route_no;

    route_no = 37;
    //initExampleBoard(board, WHITE | KING, route_no);
    int board[64] = {4, 2, 3, 5, 0, 3, 2, 4, 1, 1, 1, 1, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 6, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 9, 9, 9, 9, 9, 9, 9, 9, 12, 10, 11, 13, 14, 11, 10, 12};

    getAvailableMoves(availableMoves, board, route_no);
    return 0;
}

