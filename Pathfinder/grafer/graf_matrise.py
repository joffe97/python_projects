import numpy as np

class Node:
    def __init__(self, dataobjekt, kostnad=None):
        self.dataobjekt = dataobjekt
        self.kostnad = kostnad

# Plassbruk: Theta(V**2)
# Kjøretid for konstruktør: Theta(V**2)
class GrafMatrise:
    def __init__(self, kapasitet):
        self.noder = np.zeros(kapasitet, dtype=object)
        self.kantmatrise = np.zeros((kapasitet, kapasitet))
        for i in range(kapasitet):
            for j in range(kapasitet):
                self.kantmatrise[i, j] = -1
        self.antall_noder = 0

    # Returnerer en referanse
    # Kjøretid: Theta(1)
    def add_node(self, dataobjekt):
        ny_node = Node(dataobjekt)
        self.noder[self.antall_noder] = ny_node
        node_index = self.antall_noder
        self.antall_noder += 1
        return node_index

    # Kjøretid: Theta(1)
    def add_edge(self, fra_node, til_node, vekt):
        self.kantmatrise[fra_node, til_node] = vekt

    # Kjøretid: Theta(1)
    def get_nodedata(self, node_referanse):
        return self.noder[node_referanse].dataobjekt

    # Kjøretid: Theta(1)
    def get_vekt(self, fra_node, til_node):
        return self.kantmatrise[fra_node, til_node]

    # Kjøretid: Theta(1)
    def set_kostnad(self, node_referanse, kostnad):
        self.noder[node_referanse].kostnad = kostnad

    # Kjøretid: Theta(1)
    def get_kostnad(self, node_referanse):
        return self.noder[node_referanse]

    # Kjøretid: Theta(n)
    def fjern_kostnader(self):
        for i in range(self.antall_noder):
            self.noder[i].kostnad = None

    # Antall noder i grafen
    # Kjøretid: Theta(1)
    def get_antall_noder(self):
        self.antall_noder

    # Kjøretid Theta(V)
    def get_naboliste(self, node_indeks):
        naboliste = []
        for til_node in range(self.antall_noder):
            if self.get_vekt(node_indeks, til_node) != -1:
                naboliste.append(til_node)
        return til_node

if __name__ == "__main__":
    graf = GrafMatrise(10)
