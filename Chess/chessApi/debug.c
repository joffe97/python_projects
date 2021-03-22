//
// Created by Joachim on 15.03.2021.
//

#include <stdio.h>
#include <stdlib.h>

#include "pieces.h"
#include "board.h"
#include "botBrain.h"

int main(int argc, char *argv[]) {
    int board[64], /*move[2], */dest[32];

    initStartBoard(board);
    // int board2[64] = {4, 2, 3, 5, 6, 3, 2, 4, 1, 1, 1, 1, 0, 1, 1, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 9, 9, 9, 9, 9, 9, 9, 9, 12, 10, 11, 13, 14, 11, 10, 12};

    getAvailableMoves(dest, board, 60);

    // int scoreDifference = getScore(board2) - getScore(board);
    // getBestMove(&move[0], &move[1], board, 5, BLACK);
    return 0;
}

