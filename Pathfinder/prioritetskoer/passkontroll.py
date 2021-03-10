from prioritetskoer.binaerhaug import Prioritetsko
from collections import deque
import random

HENDELSE_ANKOMMET = 1
HENDELSE_BEHANDLET = 2

PASSASJERKOE_TOM = -1
MAKS_TID = 10000

class Hendelse:
    def __init__(self, type, tidsstempel):
        self.type = type
        self.tidsstempel = tidsstempel


def haandter_ankomst(passasjerer, hendelseskoe, systemtid):
    print(f"Passasjer ankommer på tid: {systemtid}. Passasjerkølengde {len(passasjerer)}")
    passasjerer.append(systemtid)
    ny_tid = systemtid + random.randint(5, 90)
    hendelsen = Hendelse(HENDELSE_ANKOMMET, ny_tid)
    hendelseskoe.add(hendelsen, ny_tid)


def haandter_behandlet(passasjerer, hendelseskoe, systemtid):
    if len(passasjerer) == 0:
        print(f"Skulle behandle passasjer men køen er tom. Tid {systemtid}")
        ventetid = PASSASJERKOE_TOM
        ny_tid = systemtid + 360
    else:
        print(f"Behandlet passasjer på tid: {systemtid}. Passasjerkølengde {len(passasjerer)}")
        passasjer_ankonsttid = passasjerer.popleft()
        ventetid = systemtid - passasjer_ankonsttid
        ny_tid = systemtid + 60
    hendelsen = Hendelse(HENDELSE_BEHANDLET, ny_tid)
    hendelseskoe.add(hendelsen, ny_tid)
    return ventetid


def kjor_simulering():
    hendelseskoe = Prioritetsko()
    passasjerer = deque()
    systemtid = 0

    maks_koelengde = 0
    maks_ventetid = 0

    antall_behandlet = 0
    antall_ledige_ganger = 0

    hendelseskoe.add(Hendelse(HENDELSE_ANKOMMET, 0), 0)
    hendelseskoe.add(Hendelse(HENDELSE_BEHANDLET, 60), 60)
    hendelseskoe.add(Hendelse(HENDELSE_BEHANDLET, 90), 90)

    while systemtid < MAKS_TID:
        hendelse = hendelseskoe.remove()
        systemtid = hendelse.tidsstempel
        if hendelse.type == HENDELSE_ANKOMMET:
            haandter_ankomst(passasjerer, hendelseskoe, systemtid)
            if len(passasjerer) > maks_koelengde:
                maks_koelengde = len(passasjerer)
        if hendelse.type == HENDELSE_BEHANDLET:
            ventetid = haandter_behandlet(passasjerer, hendelseskoe, systemtid)
            if ventetid == PASSASJERKOE_TOM:
                antall_ledige_ganger += 1
            else:
                antall_behandlet += 1
            if ventetid > maks_ventetid:
                maks_ventetid = ventetid

    print("Simulering ferdig")
    print(f"Maksimal kølengde: {maks_koelengde}")
    print(f"Maksimal ventetid: {maks_ventetid}")
    print(f"Behandlet antall passasjerer: {antall_behandlet}")
    print(f"Antall ganger kontrollør ledig: {antall_ledige_ganger}")


if __name__ == "__main__":
    kjor_simulering()
