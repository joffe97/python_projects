from grafer.graf_naboliste import GrafNaboliste
from grafer.topologisk_sortering import topologisk_sortering


def bygg_aktivitetsgraf():
    grafen = GrafNaboliste()
    grafen.add_node("Start")    # 0
    grafen.add_node("Ae")       # 1
    grafen.add_node("Be")       # 2
    grafen.add_node("Ce")       # 3
    grafen.add_node("Ds")       # 4
    grafen.add_node("De")       # 5
    grafen.add_node("Ee")       # 6
    grafen.add_node("Fs")       # 7
    grafen.add_node("Fe")       # 8
    grafen.add_node("Gs")       # 9
    grafen.add_node("Ge")       # 10
    grafen.add_node("Ke")       # 11
    grafen.add_node("Hs")       # 12
    grafen.add_node("He")       # 13
    grafen.add_node("Slutt")    # 14
    grafen.add_edge(0, 1, 3)
    grafen.add_edge(0, 2, 2)
    grafen.add_edge(1, 3, 3)
    grafen.add_edge(1, 4, 0)
    grafen.add_edge(2, 4, 0)
    grafen.add_edge(4, 5, 2)
    grafen.add_edge(2, 6, 1)
    grafen.add_edge(3, 7, 0)
    grafen.add_edge(5, 7, 0)
    grafen.add_edge(7, 8, 3)
    grafen.add_edge(5, 9, 0)
    grafen.add_edge(6, 9, 0)
    grafen.add_edge(9, 10, 2)
    grafen.add_edge(6, 11, 4)
    grafen.add_edge(8, 12, 0)
    grafen.add_edge(10, 12, 0)
    grafen.add_edge(11, 12, 0)
    grafen.add_edge(12, 13, 1)
    grafen.add_edge(13, 14, 0)
    return grafen


def kritisk_sti_aktivitetsgraf(graf):
    sortert_nodeliste = topologisk_sortering(graf)
    graf.fjern_kostnader()
    graf.set_kostnad(sortert_nodeliste[0], 0)
    for node in sortert_nodeliste:
        node_kostnad = graf.get_kostnad(node)
        naboer = graf.get_naboer(node)
        for nabo in naboer:
            if graf.get_kostnad(nabo) is None:
                graf.set_kostnad(nabo, node_kostnad + graf.get_vekt(node, nabo))
                graf.set_forrige_node(nabo, node)
            elif graf.get_kostnad(nabo) < node_kostnad + graf.get_vekt(node, nabo):
                graf.set_kostnad(nabo, node_kostnad + graf.get_vekt(node, nabo))
                graf.set_forrige_node(nabo, node)
    maks_kostnad = graf.get_kostnad(sortert_nodeliste[-1])
    kritisk_vei = []
    nv_node = sortert_nodeliste[-1]
    while nv_node is not None:
        kritisk_vei.append(nv_node)
        nv_node = graf.get_forrige_node(nv_node)
    kritisk_vei.reverse()
    return maks_kostnad, kritisk_vei


if __name__ == "__main__":
    grafen = bygg_aktivitetsgraf()
    print("Kritisk vei for aktivitetsgraf")
    maks_kostnad, kritisk_vei = kritisk_sti_aktivitetsgraf(grafen)
    print(f"Kostnad for prosjektet: {maks_kostnad}")
    print("Kritisk sti:")
    for i in kritisk_vei:
        print(grafen.get_nodedata(i))
