from grafer.emnegraf import bygg_emnegraf


UNDER_BEHANDLING = 1
FERDIG = 2


class Tidsstempel:
    def __init__(self):
        self.tidsstempel = 0


def topologisk_sortering(graf):
    liste = []
    graf.fjern_kostnader()              # Theta(V)
    graf.fjern_kanttyper()              # Theta(E)
    noder_prosessert = set()
    noder_gjenstaaende = set()
    for i in range(graf.get_antall_noder()):
        noder_gjenstaaende.add(i)
    tidsstempel = Tidsstempel()
    while len(noder_gjenstaaende) > 0:  # Totalt Theta(V + E)
        dfs_rekursiv(graf, noder_gjenstaaende.pop(), tidsstempel, liste, noder_prosessert, noder_gjenstaaende)
    liste.reverse()                     # Theta(V)
    return liste


# Kaller seg selv O(V) ganger.
# Kjøretid O(V + E)
def dfs_rekursiv(graf, node, tidsstempel, liste, noder_prosessert, noder_gjenstaaende):
    tidsstempel.tidsstempel += 1
    print(f"Starter behandling av node {graf.get_nodedata(node)} på tid {tidsstempel.tidsstempel}")
    graf.set_kostnad(node, UNDER_BEHANDLING)
    noder_gjenstaaende.discard(node)            # Theta(1) remove fra hashset
    graf.set_starttidspunkt(node, tidsstempel.tidsstempel)
    naboer = graf.get_naboer(node)      # Theta(antall naboer)
    for nabo in naboer:
        if graf.get_kostnad(nabo) is None:
            graf.set_kant_type(node, nabo, "Tree-edge")
            dfs_rekursiv(graf, nabo, tidsstempel, liste, noder_prosessert, noder_gjenstaaende)
        elif graf.get_kostnad(nabo) == UNDER_BEHANDLING:
            graf.set_kant_type(node, nabo, "Back-edge")
            print(f"Har funnet en sykel, siste kant fra {graf.get_nodedata(node)} til {graf.get_nodedata(nabo)}")
        elif graf.get_kostnad(nabo) == FERDIG:
            graf.set_kant_type(node, nabo, "Cross-edge")
            print(f"Har funnet en cross-edge fra {graf.get_nodedata(node)} til {graf.get_nodedata(nabo)}")
    tidsstempel.tidsstempel += 1
    graf.set_kostnad(node, FERDIG)
    noder_prosessert.add(node)          # Theta(1) add på hashset
    liste.append(node)                  # O(1) for add på array-liste
    graf.set_sluttidspunkt(node, tidsstempel.tidsstempel)
    print(f"Avslutter behandling av node {graf.get_nodedata(node)} på tid {tidsstempel.tidsstempel}")


if __name__ == "__main__":
    grafen = bygg_emnegraf()
    liste = topologisk_sortering(grafen)
    for i in liste:
        print(grafen.get_nodedata(i))
