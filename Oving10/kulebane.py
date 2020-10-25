import numpy as np
import matplotlib.pyplot as plt
import math


class BasisKulebane:
    def __init__(self, tyngdekraft):
        self.tyngdekraft = tyngdekraft

    def evaluate(self, tidspunkt, tilstandsvektor):
        x_acc = 0
        y_acc = self.tyngdekraft
        x_fart = tilstandsvektor[2]
        y_fart = tilstandsvektor[3]

        endringsvektor = np.array([x_fart, y_fart, x_acc, y_acc]) * tidspunkt
        return endringsvektor


class AvaKulebane:
    def __init__(self, tyngdekraft, luftmotstand):
        self.tyngdekraft = tyngdekraft
        self.c = luftmotstand

    def evaluate(self, tidspunkt, tilstandsvektor):
        x_fart = tilstandsvektor[2]
        y_fart = tilstandsvektor[3]

        fart = math.sqrt(x_fart**2 + y_fart**2)

        x_acc = -(self.c * x_fart * fart)
        y_acc = self.tyngdekraft - (self.c * y_fart * fart)

        endringsvektor = np.array([x_fart, y_fart, x_acc, y_acc]) * tidspunkt
        return endringsvektor


class SuperAvaKulebane:
    def __init__(self, tyngdekraft, luftmotstand, vind_vektor):
        self.tyngdekraft = tyngdekraft
        self.c = luftmotstand
        self.x_vind = vind_vektor[0]
        self.y_vind = vind_vektor[1]

    def evaluate(self, tidspunkt, tilstandsvektor):
        x_fart = tilstandsvektor[2]
        y_fart = tilstandsvektor[3]

        fart = math.sqrt(x_fart**2 + y_fart**2)

        x_acc = -(self.c * x_fart * fart) + self.x_vind
        y_acc = self.tyngdekraft - (self.c * y_fart * fart) + self.y_vind

        endringsvektor = np.array([x_fart, y_fart, x_acc, y_acc]) * tidspunkt
        return endringsvektor


class Integrasjon:
    def __init__(self, tidssteg, sluttid):
        self.tidssteg = tidssteg
        self.sluttid = sluttid
        self.tid = 0
        self.tilstandsvektor = []
        self.matrise = np.array([[]])
        self.nextvector = []
        self.k = 0

    def integrer(self, funksjonsobjekt: (BasisKulebane, AvaKulebane), starttilstand):
        self.k = 0
        self.tid = 0
        self.tilstandsvektor = np.array(starttilstand.copy())

        while self.tid <= self.sluttid:
            endringsvektor = funksjonsobjekt.evaluate(self.tidssteg, self.tilstandsvektor)

            self.tilstandsvektor = self.tilstandsvektor + endringsvektor
            self.tilstandsvektor = list(self.tilstandsvektor)

            vektor = self.tilstandsvektor.copy()
            vektor.insert(0, self.tid)

            if self.tid == 0:
                self.matrise = np.array([vektor])
            else:
                self.matrise = np.append(self.matrise, [vektor], axis=0)

            self.tid += self.tidssteg
        return self.matrise

    def __next__(self):
        if self.k >= len(self.matrise):
            self.k = 0
        vector = self.matrise[self.k]
        self.k += 1
        return vector


class MatriseIterator:
    def __init__(self, matrise):
        self.matrise = matrise
        self.k = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.k >= len(self.matrise):
            raise StopIteration
        vector = self.matrise[self.k]
        self.k += 1
        return vector


if __name__ == '__main__':
    GRAVITASJON = 9.81
    LUFTMOTSTAND = 0.5
    VIND = [-2, 0]
    STARTTILSTAND = [17, 720, 10, -10]
    tid = 0.45

    integrator = Integrasjon(0.01, tid)
    kule_A = BasisKulebane(GRAVITASJON)
    kule_B = AvaKulebane(GRAVITASJON, LUFTMOTSTAND)
    kule_C = SuperAvaKulebane(GRAVITASJON, LUFTMOTSTAND, VIND)

    a = integrator.integrer(kule_A, STARTTILSTAND)
    b = integrator.integrer(kule_B, STARTTILSTAND)
    c = integrator.integrer(kule_C, STARTTILSTAND)

    plt.plot(a[:, 1], a[:, 2])
    plt.plot(b[:, 1], b[:, 2])
    plt.plot(c[:, 1], c[:, 2])

    plt.title("Kulebaner")
    plt.xlabel("Tid")

    plt.show()

    for k in range(45):
        print(next(integrator))
