# Lag ei liste (standard Python array-liste)

# Sett inn (verdi, prioritet) tupler i lista, sett inn på sluttem

# For peek og remove, leit gjennom lista etter det minste elementet og returner det.
class Prioritetsko:
    def __init__(self):
        self.liste = []

    # Legg inn et element med oppgitt prioritet. Kjøretid O(1) amortized
    def add(self, verdi, prioritet):
        verdi_tuppel = (verdi, prioritet)
        self.liste.append(verdi_tuppel)

    # Finner indeksen i lista til det laveste elementet. Kjøretid Theta(n)
    def finn_laveste(self):
        forelopig_laveste_prioritet = self.liste[0][1]
        forelopig_laveste_index = 0
        for i in range(len(self.liste)):
            if forelopig_laveste_prioritet > self.liste[i][1]:
                forelopig_laveste_prioritet = self.liste[i][1]
                forelopig_laveste_index = i
        return forelopig_laveste_index

    # Tar ut og returnerer verdien med lavest verdi i "prioritet" variabelen
    # Kjøretid Theta(n)
    def remove(self):
        if len(self.liste) == 0:
            raise ValueError("Prioritetskøen er tom")
        index_laveste = self.finn_laveste()                 # Theta(n)
        element_laveste = self.liste[index_laveste][0]      # Theta(1)
        del self.liste[index_laveste]                       # O(n)
        return element_laveste

    # Finner verdien med laveste verdi i "prioritet" variabelen og returnerer den, men fjerner den ikke
    # Kjøretid Theta(n)
    def peek(self):
        if len(self.liste) == 0:
            raise ValueError("Prioritetskøen er tom")
        index_laveste = self.finn_laveste()
        return self.liste[index_laveste][0]

    # Setter prioriteten til en ny verdi
    # Kjøretid O(n) for å gå gjennom lista
    def senk_prioritet(self, verdi, ny_prioritet):
        for element in self.liste:
            if element[0] == verdi:
                element[1] = ny_prioritet
                return

    # Kjøretid Theta(1)
    def __len__(self):
        return len(self.liste)


if __name__ == "__main__":
    testkoe = Prioritetsko()
    testkoe.add(5, 5)
    testkoe.add(15, 15)
    testkoe.add(2, 2)
    testkoe.add(10, 10)
    testkoe.add(7, 7)
    print(testkoe.peek())
    print(testkoe.remove())
    print(testkoe.remove())
    testkoe.add(4, 4)
    testkoe.add(12, 12)
    print(testkoe.remove())
    print(testkoe.remove())
