//
// Created by Joachim on 18.02.2021.
//

#define PY_SSIZE_T_CLEAN

#include <Python.h>
#include <stdio.h>
#include <stdlib.h>

#include "pieces.h"
#include "board.h"


int main(int argc, char *argv[]) {
    int board[64];
    initStartBoard(board);
    return 0;
}


void Py_BuildBoardList(PyObject *py_list, int *board) {
    for (int i = 0; i < 64; i++) {
        PyList_Append(py_list, Py_BuildValue("i", board[i]));
    }
}

static PyObject *Py_getStartBoard(PyObject *self, PyObject *args) {
    int board[64];
    initStartBoard(board);
    PyObject *py_list = PyList_New(0);
    Py_BuildBoardList(py_list, board);
    return py_list;
}

static PyObject *Py_getAvailableMoves(PyObject *self, PyObject *args) {
    int route_no, *board, availableMoves[28];
    if (!PyArg_ParseTuple(args, "OiO", &route_no, &board))
        return NULL;

    getAvailableMoves(availableMoves, board, route_no);
}

static PyObject *version(PyObject *self) {
    return Py_BuildValue("s", "Version 1.0");
}

static PyMethodDef myMethods[] = {
        {"getStartBoard", Py_getStartBoard, METH_VARARGS, "Returns list with start board"},
        {"getAvailableMoves", Py_getStartBoard, METH_VARARGS, "Returns available moves for given piece"},
        {"version", (PyCFunction)version, METH_NOARGS, "Returns the version."},
        {NULL, NULL, 0, NULL}
};

static struct PyModuleDef myModule = {
        PyModuleDef_HEAD_INIT,
        "chessApi",
        "Chess API",
        -1,
        myMethods
};

PyMODINIT_FUNC PyInit_chessApi(void) {
    return PyModule_Create(&myModule);
}

