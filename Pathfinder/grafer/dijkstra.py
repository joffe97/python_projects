from prioritetskoer.binaerhaug import Prioritetsko
from grafer.demograf import bygg_demograf


# Kjøretid:
#  O(V) remove-operasjoner fra prioritetskøen
#  O(V) add operasjoner til prioritetskøen
#  O(E) senk_prioritet operasjoner på prioritetskøen
#
# Med array-basert prioritetskø: O(V**2 + E)
#
# Med binærhaug: O(V*log(V) + E*log(V))
#
# Glissen graf: array-basert O(V**2), binærhaug O(V*log(V))  <- Binærhaug best
#
# Tett graf: array-basert O(V**2), binærhaug O(V**2 * log(V)) <- Array-basert haug best
def dijkstra(graf, startnode, sluttnode):
    nodekoe = Prioritetsko()                # Theta(1)
    graf.fjern_kostnader()                  # Theta(V)
    graf.set_kostnad(startnode, 0)          # Theta(1)
    nodekoe.add(startnode, 0)               # Theta(1)
    while len(nodekoe) > 0:                 # Kjører O(V) ganger
        nv_node = nodekoe.remove()          # O(log(V)) med binærhaug, O(V) med array-basert
        if nv_node == sluttnode:            # O(1)
            return
        naboer = graf.get_naboer(nv_node)   # Totalt O(E)
        for nabo in naboer:                 # Totalt O(E)
            kostnad_til_nabo = graf.get_kostnad(nv_node) + graf.get_vekt(nv_node, nabo)     # Theta(1)
            if graf.get_kostnad(nabo) is None:
                graf.set_kostnad(nabo, kostnad_til_nabo)
                graf.set_forrige_node(nabo, nv_node)
                nodekoe.add(nabo, kostnad_til_nabo)                 # O(log(V)) med binærhaug, O(1) array-basert
            elif graf.get_kostnad(nabo) > kostnad_til_nabo:
                graf.set_kostnad(nabo, kostnad_til_nabo)
                graf.set_forrige_node(nabo, nv_node)
                nodekoe.senk_prioritet(nabo, kostnad_til_nabo)      # O(log(V)) med binærhaug, O(1) array-basert


def skriv_korteste_vei(grafen, startnode):
    nv_node = startnode
    while nv_node is not None:
        print(f"Node: {grafen.get_nodedata(nv_node)}")
        nv_node = grafen.get_forrige_node(nv_node)


if __name__ == "__main__":
    grafen = bygg_demograf()
    dijkstra(grafen, 0, 7)
    print(f"Korteste vei fra A til H: {grafen.get_kostnad(7)}")
    skriv_korteste_vei(grafen, 7)
