cmake_minimum_required(VERSION 3.17)
project(chessApi C)

set(CMAKE_C_STANDARD 11)

add_executable(chessApi
        pymodule.c
        pieces.c
        board.c
        rules.c)

find_package(PythonLibs REQUIRED)
include_directories(${PYTHON_INCLUDE_DIRS})
link_libraries(C:/Users/Joach/AppData/Local/Programs/Python/Python38-32/libs/python38.lib ${PYTHON_LIBRARIES})