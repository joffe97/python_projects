//
// Created by Joachim on 15.03.2021.
//

#include <stdio.h>
#include <stdlib.h>

#include "pieces.h"
#include "board.h"
#include "botBrain.h"

int main(int argc, char *argv[]) {
    int /*board[64], move[2], */dest[32];

    //initStartBoard(board);
    int board[64] = {4, 0, 0, 0, 6, 0, 0, 4, 1, 3, 1, 1, 5, 1, 1, 1, 0, 1, 2, 3, 1, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 11, 0, 9, 0, 0, 0, 10, 13, 9, 9, 0, 10, 0, 0, 9, 9, 0, 11, 0, 9, 9, 9, 12, 0, 0, 0, 14, 0, 0, 12};
    // int board2[64] = {4, 2, 3, 5, 6, 3, 2, 4, 1, 1, 1, 1, 0, 1, 1, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 9, 9, 9, 9, 9, 9, 9, 9, 12, 10, 11, 13, 14, 11, 10, 12};

    getAvailableMoves(dest, board, 60);

    // int scoreDifference = getScore(board2) - getScore(board);
    // getBestMove(&move[0], &move[1], board, 5, BLACK);
    return 0;
}

