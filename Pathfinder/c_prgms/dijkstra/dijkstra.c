#define PY_SSIZE_T_CLEAN
#include <Python.h>

#define MAX_NEIGHBOURS 10
#define NELEMS(x) (sizeof(x) / sizeof(x)[0])


typedef struct priority_element {
    int *data;
    int priority;
} priorityElement;

void pe_init(priorityElement *element, int *data, int priority) {
    element->data = data;
    element->priority = priority;
}




typedef struct priority_queue {
    priorityElement **data;
    size_t data_len;
    size_t next_index;
} priorityQueue;

void pq_init(priorityQueue *queue) {
    queue->data_len = 64;
    queue->data = (priorityElement**) malloc(queue->data_len * sizeof(priorityElement*));
    queue->next_index = 1;
}

void pq_free(priorityQueue *queue) {
    for (int i=1; i < queue->next_index; i++) {
        free(queue->data[i]);
    }
    free(queue->data);
    queue->data_len = 0;
    queue->next_index = 1;
}

size_t pq_parent_index(size_t index) {
    return index / 2;
}

size_t pq_left_child(size_t index) {
    return index * 2;
}

size_t pq_right_child(size_t index) {
    return index * 2 + 1;
}

int pq_is_lower(priorityQueue *queue, size_t index1, size_t index2) {
    if (index1 >= queue->next_index || queue->data[index1]->priority > queue->data[index2]->priority)
        return 1;
    return 0;
}

void pq_switch_elements(priorityQueue *queue, size_t index1, size_t index2) {
    priorityElement *pe1 = queue->data[index1];
    queue->data[index1] = queue->data[index2];
    queue->data[index2] = pe1;
}

void pq_buble_up(priorityQueue *queue, size_t index) {
    while (index > 1 && queue->data[index]->priority < queue->data[pq_parent_index(index)]->priority) {
        pq_switch_elements(queue, index, pq_parent_index(index));
        index = pq_parent_index(index);
    }
}

void pq_buble_down(priorityQueue *queue, size_t index) {
    while (!(pq_is_lower(queue, pq_left_child(index), index) && pq_is_lower(queue, pq_right_child(index), index))) {
        if (pq_right_child(index) >= queue->next_index) {
            pq_switch_elements(queue, index, pq_left_child(index));
            return;
        }
        if (queue->data[pq_left_child(index)]->priority < queue->data[pq_right_child(index)]->priority) {
            pq_switch_elements(queue, index, pq_left_child(index));
            index = pq_left_child(index);
        } else {
            pq_switch_elements(queue, index, pq_right_child(index));
            index = pq_right_child(index);
        }
    }
}

int pq_extend(priorityQueue *queue) {
    size_t new_len = queue->data_len * 2;
    priorityElement **tmp = realloc(queue->data, new_len * sizeof(priorityElement*));
    if (!tmp) {
        pq_free(queue);
        return 1;
    }
    queue->data = tmp;
    queue->data_len = new_len;
    return 0;
}

int pq_update_priority(priorityQueue *queue, int element, int new_priority) {
    for (int i=1; i<queue->next_index; i++) {
        if (*queue->data[i]->data == element) {
            queue->data[i]->priority = new_priority;
            return 0;
        }
    }
    return 1;
}

int pq_add(priorityQueue *queue, int *element, int priority) {
    if (queue->next_index >= queue->data_len) {
        if (pq_extend(queue)) return 1;
    }
    priorityElement *pe = (priorityElement*) malloc(sizeof(priorityElement));
    pe_init(pe, element, priority);

    size_t index = queue->next_index++;
    queue->data[index] = pe;

    pq_buble_up(queue, index);
    return 0;
}

int *pq_remove(priorityQueue *queue) {
    if (queue->next_index - 1 < 1) return NULL;

    int *ret_data = queue->data[1]->data;
    queue->data[1]->data = queue->data[--queue->next_index]->data;
    queue->data[1]->priority = queue->data[queue->next_index]->priority;
    free(queue->data[queue->next_index]);
    queue->data[queue->next_index] = NULL;

    if (queue->next_index > 1) {
        pq_buble_down(queue, 1);
    }
    return ret_data;
}

/*void pq_print(priorityQueue *queue) {
    PyObject_CallMethodObjArgs(obj2, Py_BuildValue("s", "printa"), Py_BuildValue("s", " "), NULL);
    for (int i=1; i<queue->next_index; i++) {
        PyObject_CallMethodObjArgs(obj2, Py_BuildValue("s", "printa"), Py_BuildValue("i", queue->data[i]->priority), NULL);
    }
}*/




int contains(int element, const int *array, size_t array_size) {
    for (size_t i=0; i<array_size; i++) {
        if (array[i] == element)
            return 1;
    }
    return 0;
}

int cfy_py_list(PyObject *src, int *dest) {
    PyObject *iter, *item;
    int counter = 0, cur_int;

    if (!(iter = PyObject_GetIter(src))) return -1;
    while ((item = PyIter_Next(iter))) {
        if ((cur_int = PyLong_AsLong(item)) == -1) return -1;
        dest[counter++] = cur_int;
        Py_DECREF(item);
    }
    return counter - 1;
}

int cfy_py_method_return_double(PyObject *obj, char *method_name, PyObject *arg1, PyObject *arg2, PyObject *arg3, double *dest) {
    //PyObject_CallMethodObjArgs(obj, Py_BuildValue("s", "printb"), arg1, Py_BuildValue("s", "><arg>"), NULL);
    PyObject *py_return_value;
    double return_value;
    if (arg3 != NULL) {
        py_return_value = PyObject_CallMethodObjArgs(obj, Py_BuildValue("s", method_name), arg1, arg2, arg3, NULL);
    } else if (arg2 != NULL) {
        //PyObject_CallMethodObjArgs(obj, Py_BuildValue("s", "printc"), arg1, arg2, Py_BuildValue("s", "><args>"), NULL);
        py_return_value = PyObject_CallMethodObjArgs(obj, Py_BuildValue("s", method_name), arg1, arg2, NULL);
    } else if (arg1 != NULL) {
        //PyObject_CallMethodObjArgs(obj, Py_BuildValue("s", "printb"), arg1, Py_BuildValue("s", "><arg>"), NULL);
        py_return_value = PyObject_CallMethodObjArgs(obj, Py_BuildValue("s", method_name), arg1, NULL);
    } else {
        return 1;
    }
    if (py_return_value == Py_None) {
        return 1;
    }
    //PyObject_CallMethodObjArgs(obj, Py_BuildValue("s", "printb"), py_return_value, Py_BuildValue("s", "><py>"), NULL);
    return_value = PyFloat_AsDouble(py_return_value);
    //if (!strcmp(method_name, "get_weight"))
        //PyObject_CallMethodObjArgs(obj, Py_BuildValue("s", "printb"), Py_BuildValue("f", return_value), Py_BuildValue("s", "><c>"), NULL);
    //PyObject_CallMethodObjArgs(obj, Py_BuildValue("s", "printb"), Py_BuildValue("f", return_value), Py_BuildValue("s", "><c>"), NULL);
    *dest = return_value;
    return 0;
}

int Cdijkstra(PyObject *graph, int start_node, int *end_nodes, int end_nodes_len) {
    //PyObject_CallMethodObjArgs(graph, Py_BuildValue("s", "printa"), Py_BuildValue("s", "new"), NULL);

    priorityQueue queue;
    pq_init(&queue);
    PyObject *py_neighbours, *py_cur_node, *py_neighbour, *py_cost_to_neighbour;
    int cur_node, neighbour_count, nodes_found, nok;
    int end_nodes_found[end_nodes_len], neighbours[MAX_NEIGHBOURS];
    double cur_cost, neighbour_cost, weight, cost_to_neighbour;

    nodes_found = 0;

    PyObject_CallMethodObjArgs(graph, Py_BuildValue("s", "remove_all_costs"), NULL);
    PyObject_CallMethodObjArgs(graph, Py_BuildValue("s", "set_cost"), Py_BuildValue("i", start_node), Py_BuildValue("i", 0), NULL);
    pq_add(&queue, &start_node, 0);
    //PyObject_CallMethodObjArgs(graph, Py_BuildValue("s", "printa"), Py_BuildValue("i", start_node), NULL);

    while (queue.next_index > 1) {
        cur_node = *pq_remove(&queue);
        py_cur_node = Py_BuildValue("i", cur_node);

        if (contains(cur_node, end_nodes, end_nodes_len) && !contains(cur_node, end_nodes_found, nodes_found))
            end_nodes_found[nodes_found++] = cur_node;
        if (nodes_found == end_nodes_len) {
            break;
        }

        py_neighbours = PyObject_CallMethodObjArgs(graph, Py_BuildValue("s", "get_neighbours"), py_cur_node, NULL);
        for (int i=0; i<MAX_NEIGHBOURS; i++) {
            neighbours[i] = -1;
        }
        neighbour_count = cfy_py_list(py_neighbours, neighbours);
        if (neighbour_count == -1) {
            break;
        }

        for (int i=0; i<neighbour_count; i++) {
            py_neighbour = Py_BuildValue("i", neighbours[i]);
            //PyObject_CallMethodObjArgs(graph, Py_BuildValue("s", "printa"), Py_BuildValue("s", ""), NULL);
            //PyObject_CallMethodObjArgs(graph, Py_BuildValue("s", "printb"), py_neighbour, Py_BuildValue("s", ">"), NULL);
            cfy_py_method_return_double(graph, "get_cost", py_cur_node, NULL, NULL, &cur_cost);
            cfy_py_method_return_double(graph, "get_weight", py_cur_node, py_neighbour, NULL, &weight);
            //PyObject_CallMethodObjArgs(graph, Py_BuildValue("s", "printb"), Py_BuildValue("f", cur_cost), Py_BuildValue("s", "!cost!"), NULL);
            //PyObject_CallMethodObjArgs(graph, Py_BuildValue("s", "printb"), Py_BuildValue("f", weight), Py_BuildValue("s", "!weight!"), NULL);
            cost_to_neighbour = cur_cost + weight;
            py_cost_to_neighbour = Py_BuildValue("f", cost_to_neighbour);
            //PyObject_CallMethodObjArgs(graph, Py_BuildValue("s", "printb"), py_cost_to_neighbour, Py_BuildValue("s", "!cost_to_n! "), NULL);
            //PyObject_CallMethodObjArgs(graph, Py_BuildValue("s", "printa"), Py_BuildValue("s", "a"), NULL);
            nok = cfy_py_method_return_double(graph, "get_cost", py_neighbour, NULL, NULL, &neighbour_cost);
            //PyObject_CallMethodObjArgs(graph, Py_BuildValue("s", "printa"), Py_BuildValue("s", "b"), NULL);
            if (nok) {
                PyObject_CallMethodObjArgs(graph, Py_BuildValue("s", "set_cost"), py_neighbour, py_cost_to_neighbour, NULL);
                PyObject_CallMethodObjArgs(graph, Py_BuildValue("s", "set_prevnode"), py_neighbour, py_cur_node, NULL);
                pq_add(&queue, &neighbours[i], (int) cost_to_neighbour);
            } else if (neighbour_cost > cost_to_neighbour) {
                PyObject_CallMethodObjArgs(graph, Py_BuildValue("s", "set_cost"), py_neighbour, py_cost_to_neighbour, NULL);
                PyObject_CallMethodObjArgs(graph, Py_BuildValue("s", "set_prevnode"), py_neighbour, py_cur_node, NULL);
                pq_update_priority(&queue, neighbours[i], (int) cost_to_neighbour);
            }
        }
    }
    pq_free(&queue);
    return nodes_found;
}

static PyObject *dijkstra(PyObject *self, PyObject *args) {
    PyObject *graph, *py_end_nodes, *py_end_nodes_len;
    int start_node, nodes_found;
    long end_nodes_len;

    if (!PyArg_ParseTuple(args, "OiO", &graph, &start_node, &py_end_nodes))
        return NULL;

    py_end_nodes_len = PyObject_CallMethodObjArgs(py_end_nodes, Py_BuildValue("s", "__len__"), NULL);
    if ((end_nodes_len = PyLong_AsLong(py_end_nodes_len)) == -1) return NULL;
    if (end_nodes_len == 0) return Py_BuildValue("i", 0);
    int end_nodes[end_nodes_len];

    if (cfy_py_list(py_end_nodes, end_nodes) == -1) return NULL;


    nodes_found = Cdijkstra(graph, start_node, end_nodes, end_nodes_len);

    return Py_BuildValue("i", nodes_found);
}

static PyObject *version(PyObject *self) {
    return Py_BuildValue("s", "Version 1.0");
}

static PyMethodDef myMethods[] = {
        {"dijkstra", dijkstra, METH_VARARGS, "Uses dijkstra algorithm on a graph."},
        {"version", (PyCFunction)version, METH_NOARGS, "Returns the version."},
        {NULL, NULL, 0, NULL}
};

static struct PyModuleDef myModule = {
        PyModuleDef_HEAD_INIT,
        "dijkstra",
        "Dijkstra Module",
        -1,
        myMethods
};

PyMODINIT_FUNC PyInit_dijkstra(void) {
    return PyModule_Create(&myModule);
}
