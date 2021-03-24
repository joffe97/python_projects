//
// Created by Joach on 19.03.2021.
//

#ifndef CHESSAPI_BOTBRAIN_H
#define CHESSAPI_BOTBRAIN_H

struct moveData {
    int isSet;
    int from;
    int to;
    int score;
};

int getScore(int *board);
void getBestMove(int *from_dest, int *to_dest, int *board, int depth, int colorsTurn);

#endif //CHESSAPI_BOTBRAIN_H

