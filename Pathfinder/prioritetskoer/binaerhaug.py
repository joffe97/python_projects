class Prioritetsko:
    # Kjøretid Theta(1)
    def __init__(self, liste=None):
        self.liste = []
        self.liste.append("Dummy")
        self.elementfinner = {}
        if liste is not None:
            for element in liste:
                self.liste.append(element)
            for index in range(self.forelder(len(self.liste)-1), 0, -1):
                self.boble_ned(index)

    # Kjøretid Theta(1)
    def forelder(self, index):
        return index//2

    # Kjøretid Theta(1)
    def venstre_barn(self, index):
        return index*2

    # Kjøretid Theta(1)
    def hoyre_barn(self, index):
        return index*2 + 1

    def bytt_elementer(self, index1, index2):
        temp = self.liste[index1]
        self.liste[index1] = self.liste[index2]
        self.liste[index2] = temp
        self.elementfinner[self.liste[index1][0]] = index1
        self.elementfinner[self.liste[index2][0]] = index2

    # Kjøretid
    # Best case O(1) hvis det du setter inn er større enn forelder
    # Worst case O(høyden til treet) = O(log(n))
    def boble_opp(self, index):
        while index > 1 and self.liste[index][1] < self.liste[self.forelder(index)][1]:
            forelder = self.forelder(index)
            self.bytt_elementer(index, forelder)
            index = forelder

    # Kjøretid Theta(1)
    def er_mindre(self, index, prioritet):
        if index >= len(self.liste):
            return True
        if self.liste[index][1] > prioritet:
            return True
        return False

    # Kjøretid:
    # Teoretisk O(1) best case som aldri skjer i praksis med mindre haugen er svært liten
    # O(log(n)) worst og average case
    def boble_ned(self, index):
        while not(self.er_mindre(self.venstre_barn(index), self.liste[index][1]) and
                  self.er_mindre(self.hoyre_barn(index), self.liste[index][1])):
            if self.hoyre_barn(index) >= len(self.liste):
                self.bytt_elementer(index, self.venstre_barn(index))
                return
            if self.liste[self.venstre_barn(index)][1] < self.liste[self.hoyre_barn(index)][1]:
                self.bytt_elementer(index, self.venstre_barn(index))
                index = self.venstre_barn(index)
            else:
                self.bytt_elementer(index, self.hoyre_barn(index))
                index = self.hoyre_barn(index)


    # Legg inn et element med oppgitt prioritet
    # Kjøretid O(1) best case, O(log(n)) worst case
    def add(self, verdi, prioritet):
        verdi_tuppel = (verdi, prioritet)       # Theta(1)
        self.liste.append(verdi_tuppel)         # O(1) amortized
        self.elementfinner[verdi] = len(self.liste) - 1
        self.boble_opp(len(self.liste) - 1)     # O(1) best case, O(log(n)) worst case

    # Tar ut og returnerer verdien med lavest verdi i "prioritet" variabelen
    # Kjøretid O(log(n)) i nesten alle tilfeller
    def remove(self):
        if len(self) < 1:                   # Theta(1)
            raise ValueError("Har ingen elementer!")
        returverdi = self.liste[1][0]       # Theta(1)
        self.liste[1] = self.liste[-1]      # Theta(1)
        del self.liste[-1]                  # Å slette det siste elementet i en array-liste Theta(1)
        if len(self.liste) > 1:
            self.boble_ned(1)
        del self.elementfinner[returverdi]
        return returverdi

    # Finner verdien med laveste verdi i "prioritet" variabelen og returnerer den, men fjerner den ikke
    # Kjøretid Theta(1)
    def peek(self):
        if len(self) < 1:
            raise ValueError("Har ingen elementer!")
        return self.liste[1][0]

    # Setter prioriteten til en ny verdi
    # Kjøretid O(log(n)) for boble_opp
    def senk_prioritet(self, verdi, ny_prioritet):
        index = self.elementfinner[verdi]
        self.liste[index] = (verdi, ny_prioritet)
        self.boble_opp(index)

    def __len__(self):
        return len(self.liste)-1

    def __str__(self):
        resultat = "Haug:\n"
        for i in range(1, len(self.liste)):
            resultat += f"{i}: Prioritet {self.liste[i][1]}  Verdi: {self.liste[i][0]} \n"
        return resultat


if __name__ == "__main__":
    testkoe = Prioritetsko()
    testkoe.add(5, 5)
    testkoe.add(15, 15)
    testkoe.add(2, 2)
    testkoe.add(10, 10)
    testkoe.add(7, 7)
    print(testkoe)
    print(testkoe.peek())
    print(testkoe.remove())
    print(testkoe.remove())
    testkoe.add(4, 4)
    testkoe.add(12, 12)
    print(testkoe.remove())
    print(testkoe.remove())
    print(testkoe)
    print()
    testkoe = Prioritetsko()
    testkoe.add(10, 10)
    testkoe.add(11, 11)
    testkoe.add(15, 15)
    testkoe.add(16, 16)
    testkoe.add(12, 12)
    testkoe.add(18, 18)
    testkoe.add(22, 22)
    testkoe.add(21, 21)
    testkoe.add(24, 24)
    testkoe.add(23, 23)
    print(testkoe)
    testkoe.add(7, 7)
    print(testkoe)
    print()
    print(testkoe.remove())
    print(testkoe.remove())
    print(testkoe)
    print()
    liste = [12, 0, -20, 17, 7, 12, 13, -13, -11, 15, 19, 8, -17, 2]
    tuppel_liste = []
    for element in liste:
        tuppel_liste.append((element, element))
    print(tuppel_liste)
    koe2 = Prioritetsko(tuppel_liste)
    print(koe2)
    print()
    testkoe.senk_prioritet(23, 8)
    print(testkoe)
    print(testkoe.remove())
    print(testkoe.remove())
    print(testkoe)
