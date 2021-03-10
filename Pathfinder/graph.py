from prioritetskoer.binaerhaug import Prioritetsko


class Edge:
    def __init__(self, to_node, weight):
        self.to_node = to_node
        self.weight = weight
        self.type = None


class Node:
    def __init__(self, data: object, cost=None):
        self.data = data
        self.cost = cost
        self.start_time = 0
        self.end_time = 0
        self.neighbours = {}  # Nodeindex -> Edgeobject
        self.prev_node = None


class Graph:
    def __init__(self):
        self.nodes: [Node] = []

    def add_node(self, data: object):
        node = Node(data)
        self.nodes.append(node)
        return len(self.nodes) - 1

    def add_edge(self, from_node: int, to_node: int, weight):
        node: Node = self.nodes[from_node]
        node.neighbours[to_node] = Edge(to_node, weight)

    def get_nodedata(self, node_index: int):
        return self.nodes[node_index].data

    def get_weight(self, from_node: int, to_node: int):
        node: Node = self.nodes[from_node]
        try:
            return node.neighbours[to_node].weight
        except KeyError:
            return None

    def set_cost(self, node_index: int, cost: int):
        self.nodes[node_index].cost = cost

    def get_cost(self, node_index: int):
        return self.nodes[node_index].cost

    def remove_all_costs(self):
        for node in self.nodes:
            node: Node
            node.cost = None
            node.start_time = None
            node.end_time = None
            node.prev_node = None

    def remove_edgetypes(self):
        for node in self.nodes:
            for to_node in node.neighbours:
                edge = node.neighbours[to_node]
                edge.type = None

    def get_number_of_nodes(self):
        return len(self.nodes)

    def get_neighbours(self, node_index):
        neighbours = []
        for i in self.nodes[node_index].neighbours:
            neighbours.append(i)
        return neighbours

    def get_starttime(self, node_index: int):
        return self.nodes[node_index].start_time

    def get_endtime(self, node_index: int):
        return self.nodes[node_index].end_time

    def set_starttime(self, node_index: int, time):
        self.nodes[node_index].start_time = time

    def set_endtime(self, node_index: int, time):
        self.nodes[node_index].end_time = time

    def get_prevnode(self, node_index: int):
        return self.nodes[node_index].prev_node

    def set_prevnode(self, node_index: int, prev: int):
        self.nodes[node_index].prev_node = prev

    def dijkstra(self, start_node: int, end_nodes: list, func=None, time_diff=50):
        nodes_found = 0
        end_nodes_found = []
        queue = Prioritetsko()
        self.remove_all_costs()
        self.set_cost(start_node, 0)
        queue.add(start_node, 0)
        while len(queue) > 0:
            cur_node = queue.remove()
            if cur_node in end_nodes and cur_node not in end_nodes_found:
                end_nodes_found.append(cur_node)
            if len(end_nodes_found) == len(end_nodes):
                return nodes_found
            if func:
                func(cur_node, nodes_found * time_diff)
                nodes_found += 1
            neighbours = self.get_neighbours(cur_node)
            for neighbour in neighbours:
                cost_to_neighbour = self.get_cost(cur_node) + self.get_weight(cur_node, neighbour)
                if self.get_cost(neighbour) is None:
                    self.set_cost(neighbour, cost_to_neighbour)
                    self.set_prevnode(neighbour, cur_node)
                    queue.add(neighbour, cost_to_neighbour)
                elif self.get_cost(neighbour) > cost_to_neighbour:
                    self.set_cost(neighbour, cost_to_neighbour)
                    self.set_prevnode(neighbour, cur_node)
                    queue.senk_prioritet(neighbour, cost_to_neighbour)

    def printa(self, item):
        print(item)

    def printb(self, item, pre):
        print(f"{pre}{item}")

    def printc(self, item, item2, pre):
        print(f"{pre} {item} {item2}")
