//
// Created by Joach on 06.03.2021.
//

#ifndef CHESSAPI_BOARD_H
#define CHESSAPI_BOARD_H

void initBoard(int *board);
void initStartBoard(int *board);
int getColumn(int route_no);
int getRow(int route_no);
int getRouteNo(int column, int row);

#endif //CHESSAPI_BOARD_H
