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
    int board[64], availableMoves[32], route_no;

    initStartBoard(board);
    route_no = 12;
    
    getAvailableMoves(availableMoves, board, route_no);
    return 0;
}


void print_array(int *cArray, int size) {
    printf("cArray[");
    for (int i = 0; i < size; i++) {
        if (i != 0) {
            printf(", ");
        }
        printf("%d", cArray[i]);
    }
    printf("]");
}

void PyListToCArray(PyObject *pyList, int *cArray) {
    PyObject *iter, *next;
    int listPos = 0;

    if (!(iter = PyObject_GetIter(pyList))) {
        PyErr_SetString(PyExc_TypeError, "Can't convert a non iterable object");
    }
    while (next = PyIter_Next(iter)) {
        if (!PyLong_Check(next)) {
            PyErr_SetString(PyExc_TypeError, "Can't convert list entry into int");
        }
        cArray[listPos++] = PyLong_AsLong(next);
    }
}

void CArrayToPyList(PyObject *pyList, int *cArray, int size) {
    for (int i = 0; i < size; i++) {
        if (cArray[i] != -1) {
            PyList_Append(pyList, Py_BuildValue("i", cArray[i]));
        }
    }
}

static PyObject *Py_getStartBoard(PyObject *self, PyObject *args) {
    int board[64];
    initStartBoard(board);
    PyObject *py_list = PyList_New(0);
    CArrayToPyList(py_list, board, 64);
    return py_list;
}

static PyObject *Py_getAvailableMoves(PyObject *self, PyObject *args) {
    int route_no, board[64], availableMoves[32];
    PyObject *py_board, *py_moves;
    if (!PyArg_ParseTuple(args, "Oi", &py_board, &route_no))
        return NULL;

    PyListToCArray(py_board, board);
    getAvailableMoves(availableMoves, board, route_no);

    CArrayToPyList(py_moves, availableMoves, 32);
    return py_moves;
}

static PyObject *version(PyObject *self) {
    return Py_BuildValue("s", "Version 1.0");
}

static PyMethodDef myMethods[] = {
        {"getStartBoard", Py_getStartBoard, METH_VARARGS, "Returns list with start board"},
        {"getAvailableMoves", Py_getAvailableMoves, METH_VARARGS, "Returns available moves for given piece"},
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

