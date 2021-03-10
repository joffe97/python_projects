from grafer.graf_matrise import GrafMatrise
from grafer.graf_naboliste import GrafNaboliste

def bygg_demograf():
    grafen = GrafNaboliste()
    a = grafen.add_node("A")        # Indeks 0
    b = grafen.add_node("B")        # Indeks 1
    c = grafen.add_node("C")        # Indeks 2
    d = grafen.add_node("D")        # Indeks 3
    e = grafen.add_node("E")        # Indeks 4
    f = grafen.add_node("F")        # Indeks 5
    g = grafen.add_node("G")        # Indeks 6
    h = grafen.add_node("H")        # Indeks 7
    grafen.add_edge(a, b, 5)
    grafen.add_edge(b, a, 5)
    grafen.add_edge(a, c, 2)
    grafen.add_edge(c, a, 2)
    grafen.add_edge(a, d, 2)
    grafen.add_edge(d, a, 2)
    grafen.add_edge(b, c, 4)
    grafen.add_edge(c, b, 4)
    grafen.add_edge(b, e, 5)
    grafen.add_edge(e, b, 5)
    grafen.add_edge(c, g, 3)
    grafen.add_edge(g, c, 3)
    grafen.add_edge(d, g, 3)
    grafen.add_edge(g, d, 3)
    grafen.add_edge(d, h, 5)
    grafen.add_edge(h, d, 5)
    grafen.add_edge(e, f, 3)
    grafen.add_edge(f, e, 3)
    grafen.add_edge(e, g, 3)
    grafen.add_edge(g, e, 3)
    grafen.add_edge(f, g, 5)
    grafen.add_edge(g, f, 5)
    grafen.add_edge(g, h, 2)
    grafen.add_edge(h, g, 2)
    return grafen


if __name__ == "__main__":
    grafen = bygg_demograf()
    print(grafen.get_nodedata(2))
    print(grafen.get_nodedata(0))
    print(grafen.get_nodedata(3))
    print(grafen.get_vekt(4, 5))
    print(grafen.get_vekt(2, 6))
    print(grafen.get_vekt(0, 7))
