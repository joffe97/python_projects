from grafer.demograf import bygg_demograf


UNDER_BEHANDLING = 1
FERDIG = 2


class Tidsstempel:
    def __init__(self):
        self.tidsstempel = 0

def dybde_forst_sok(graf, startnode):
    graf = graf
    graf.fjern_kostnader()              # Theta(V)
    graf.fjern_kanttyper()              # Theta(E)
    tidsstempel = Tidsstempel()
    dfs_rekursiv(graf, startnode, tidsstempel)

# Kaller seg selv O(V) ganger.
# Kjøretid O(V + E)
def dfs_rekursiv(graf, node, tidsstempel):
    tidsstempel.tidsstempel += 1
    print(f"Starter behandling av node {graf.get_nodedata(node)} på tid {tidsstempel.tidsstempel}")
    graf.set_kostnad(node, UNDER_BEHANDLING)
    graf.set_starttidspunkt(node, tidsstempel.tidsstempel)
    naboer = graf.get_naboer(node)      # Theta(antall naboer)
    for nabo in naboer:
        if graf.get_kostnad(nabo) is None:
            graf.set_kant_type(node, nabo, "Tree-edge")
            dfs_rekursiv(graf, nabo, tidsstempel)
        elif graf.get_kostnad(nabo) == UNDER_BEHANDLING:
            graf.set_kant_type(node, nabo, "Back-edge")
            print(f"Har funnet en sykel, siste kant fra {graf.get_nodedata(node)} til {graf.get_nodedata(nabo)}")
        elif graf.get_kostnad(nabo) == FERDIG:
            graf.set_kant_type(node, nabo, "Cross-edge")
            print(f"Har funnet en cross-edge fra {graf.get_nodedata(node)} til {graf.get_nodedata(nabo)}")
    tidsstempel.tidsstempel += 1
    graf.set_kostnad(node, FERDIG)
    graf.set_sluttidspunkt(node, tidsstempel.tidsstempel)
    print(f"Avslutter behandling av node {graf.get_nodedata(node)} på tid {tidsstempel.tidsstempel}")


if __name__ == "__main__":
    grafen = bygg_demograf()
    dybde_forst_sok(grafen, 0)
