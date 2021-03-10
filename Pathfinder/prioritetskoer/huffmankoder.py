from prioritetskoer.binaerhaug import Prioritetsko
from trestrukturer.binaertre import Binaertre


def lag_frekvenstabell(filnavn):
    frekvenstabell = {}
    with open(filnavn, encoding="utf8") as fila:
        for linje in fila:
            for tegn in linje:
                if tegn in frekvenstabell:
                    frekvenstabell[tegn] = frekvenstabell[tegn] + 1
                else:
                    frekvenstabell[tegn] = 1
    return frekvenstabell


def bygg_kodetre(frekvenstabell):
    nodekoe = Prioritetsko()
    for tegn in frekvenstabell:
        node = Binaertre((tegn, frekvenstabell[tegn]))
        nodekoe.add(node, frekvenstabell[tegn])
    while len(nodekoe) > 1:
#        print(f"Lengde på kø: {len(nodekoe)}, innhold {nodekoe.liste}")
        node1 = nodekoe.remove()
        node2 = nodekoe.remove()
        prioritet = node1.data[1] + node2.data[1]
        forelder = Binaertre((None, prioritet))
        forelder.venstre_barn = node1
        forelder.hoyre_barn = node2
        nodekoe.add(forelder, prioritet)
    return nodekoe.remove()


def bygg_kodetabell(kodetre, kodetabell, kode=""):
    if kodetre.er_bladnode():
        kodetabell[kodetre.data[0]] = kode
    else:
        if kodetre.venstre_barn is not None:
            bygg_kodetabell(kodetre.venstre_barn, kodetabell, kode+"0")
        if kodetre.hoyre_barn is not None:
            bygg_kodetabell(kodetre.hoyre_barn, kodetabell, kode+"1")


def kod_fil(filnavn, kodetabell):
    with open(filnavn, encoding="utf8") as fila:
        with open(filnavn+".hcode", "w") as kodefil:
            for linje in fila:
                for tegn in linje:
                    kode = kodetabell[tegn]
                    kodefil.write(kode+"\n")


def les_kodet_fil(filnavn, kodetre):
    with open(filnavn+".hcode") as kodefil:
        nv_node = kodetre
        for linje in kodefil:
            for tegn in linje:
                if nv_node.er_bladnode():
                    print(nv_node.data[0], end="")
                    nv_node = kodetre
                if tegn == "0":
                    nv_node = nv_node.venstre_barn
                elif tegn == "1":
                    nv_node = nv_node.hoyre_barn


if __name__ == "__main__":
    frekvenstabell = lag_frekvenstabell("test.txt")
    print(frekvenstabell)
    kodetre = bygg_kodetre(frekvenstabell)
    kodetre.rekursiv_preorder_utskrift()
    kodetabell = {}
    bygg_kodetabell(kodetre, kodetabell)
    for nokkel in kodetabell:
        print(f"{nokkel} : {kodetabell[nokkel]}")
    kod_fil("test.txt", kodetabell)
    les_kodet_fil("test.txt", kodetre)
