cmake_minimum_required(VERSION 3.17)
project(c_project C)

set(CMAKE_C_STANDARD 11)

add_library(dijkstra SHARED dijkstra/dijkstra.c dijkstra/tmp.c)

find_package(PythonLibs REQUIRED)
include_directories(${PYTHON_INCLUDE_DIRS})
link_libraries(C:/Users/Joach/AppData/Local/Programs/Python/Python38-32/libs/python38.lib ${PYTHON_LIBRARIES})