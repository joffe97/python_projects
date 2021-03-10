from collections import deque
from grafer.demograf import bygg_demograf


# Returnerer resultatet som modifikasjon av "kostnad" attributtet til nodene
# Total kjøretid O(V + E) for nabolistegraf, O(v**2) for matrisegraf
def bredde_forst_sok(graf, start_node):
    graf.fjern_kostnader()                  # Theta(V)
    nodekoe = deque()                       # Theta(1)
    graf.set_kostnad(start_node, 0)         # Theta(1)
    nodekoe.append(start_node)              # Theta(1)
    while len(nodekoe) > 0:                 # O(V)
        nv_node = nodekoe.popleft()                 # O(1)
        naboliste = graf.get_naboer(nv_node)        # For naboliste graf totalt O(E), for matrisegraf totalt O(V**2)
        for nabo_indeks in naboliste:               # Total O(E)
            if graf.get_kostnad(nabo_indeks) is None:           # Innhold kjører maks 1 gang pr. node O(V)
                print(f"Besøker node: {graf.get_nodedata(nabo_indeks)}")
                graf.set_kostnad(nabo_indeks, graf.get_kostnad(nv_node) + 1)
                nodekoe.append(nabo_indeks)


if __name__ == "__main__":
    grafen = bygg_demograf()
    bredde_forst_sok(grafen, 0)
    print()
    for i in range(grafen.get_antall_noder()):
        print(f"Node: {grafen.get_nodedata(i)} har avstand {grafen.get_kostnad(i)}")
