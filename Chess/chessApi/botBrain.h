//
// Created by Joach on 19.03.2021.
//

#ifndef CHESSAPI_BOTBRAIN_H
#define CHESSAPI_BOTBRAIN_H

#define VALUE_PAWN 100
#define VALUE_KNIGHT 310
#define VALUE_BISHOP 320
#define VALUE_ROOK 500
#define VALUE_QUEEN 900
#define VALUE_KING 30000

#define INFINITY 999999

struct moveData {
    int isSet;
    int from;
    int to;
    int score;
};

int getScore(int *board);
void getBestMove(int *from_dest, int *to_dest, int *board, int depth, int colorsTurn);

#endif //CHESSAPI_BOTBRAIN_H

