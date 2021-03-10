from prioritetskoer.binaerhaug import Prioritetsko
from grafer.graf_naboliste import GrafNaboliste
from grafer.demograf_ikke_rettet import bygg_demograf

def prim(graf, startnode):
    nodekoe = Prioritetsko()                # Theta(1)
    graf.fjern_kostnader()                  # Theta(V)
    graf.set_kostnad(startnode, 0)          # Theta(1)
    nodekoe.add(startnode, 0)               # Theta(1)
    while len(nodekoe) > 0:                 # Kjører O(V) ganger
        nv_node = nodekoe.remove()          # O(log(V)) med binærhaug, O(V) med array-basert
        graf.set_starttidspunkt(nv_node, 1)
        naboer = graf.get_naboer(nv_node)   # Totalt O(E)
        for nabo in naboer:                 # Totalt O(E)
            if graf.get_starttidspunkt(nabo) != 0:
                continue
            kostnad_til_nabo = graf.get_vekt(nv_node, nabo)     # Theta(1)
            if graf.get_kostnad(nabo) is None:
                graf.set_kostnad(nabo, kostnad_til_nabo)
                graf.set_forrige_node(nabo, nv_node)
                nodekoe.add(nabo, kostnad_til_nabo)                 # O(log(V)) med binærhaug, O(1) array-basert
            elif graf.get_kostnad(nabo) > kostnad_til_nabo:
                graf.set_kostnad(nabo, kostnad_til_nabo)
                graf.set_forrige_node(nabo, nv_node)
                nodekoe.senk_prioritet(nabo, kostnad_til_nabo)      # O(log(V)) med binærhaug, O(1) array-basert


def bygg_minimalt_spenntre(graf, startnode):
    prim(graf, startnode)
    ny_graf = GrafNaboliste()
    for node in range(graf.get_antall_noder()):
        ny_graf.add_node(graf.get_nodedata(node))
    for node in range(graf.get_antall_noder()):
        if graf.get_forrige_node(node) is not None:
            ny_graf.add_edge(node, graf.get_forrige_node(node), graf.get_vekt(node, graf.get_forrige_node(node)))
            ny_graf.add_edge(graf.get_forrige_node(node), node, graf.get_vekt(graf.get_forrige_node(node), node))
    return ny_graf


if __name__ == "__main__":
    graf = bygg_demograf()
    minimalt_spenntre = bygg_minimalt_spenntre(graf, 0)
    for node in range(minimalt_spenntre.get_antall_noder()):
        print(minimalt_spenntre.get_nodedata(node))
        naboer = minimalt_spenntre.get_naboer(node)
        for element in naboer:
            print(f"    {minimalt_spenntre.get_nodedata(element)} : {minimalt_spenntre.get_vekt(node, element)}")
