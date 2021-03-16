//
// Created by Joachim on 15.03.2021.
//

#include <stdio.h>
#include <stdlib.h>

#include "pieces.h"
#include "board.h"

int main(int argc, char *argv[]) {
    int board[64], availableMoves[32], route_no;

    initStartBoard(board);
    route_no = 14;

    getAvailableMoves(availableMoves, board, route_no);
    return 0;
}

