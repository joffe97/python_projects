import numpy as np


class ArrayListe:
    def __init__(self, startkapasitet=20):
        self.array = np.zeros(startkapasitet, dtype=object)
        self.lengde = 0
        self.first = 0

    #gir resultatet av len funksjonen
    def __len__(self):
        return self.lengde

    # Kjøretid Theta(n)
    def utvid(self, ny_storrelse=None):
        if ny_storrelse is None:
            ny_storrelse = len(self.array)*2
        ny_array = np.zeros(ny_storrelse, dtype=object)
        for index in range(len(self.array)):
            ny_array[index] = self.array[index]
        self.array = ny_array

    # Theta(n)
    def utvidleft(self, ny_storrelse=None):
        if ny_storrelse is None:
            ny_storrelse = len(self.array)*2
        if ny_storrelse < len(self.array):
            raise ValueError(f"Can't expand to a smaller array.")
        ny_array = np.zeros(ny_storrelse, dtype=object)
        ny_first = self.first + ny_storrelse - len(self.array)
        for index in range(len(self.array)):
            ny_array[index+ny_first] = self.array[index]
        self.first = ny_first
        self.array = ny_array

    # Legger til element på slutten av lista
    # Kjøretid: Worst case Theta(n) hvis jeg må lage en ny array
    #           Ellers Theta(1)
    # Kjøretid O(1) amortized, O(n) worst case
    def append(self, element):
        if self.lengde + self.first >= len(self.array):
            self.utvid()
        self.array[self.lengde + self.first] = element
        self.lengde += 1

    # Kjøretid O(1) amortized, O(n) worst case
    def appendleft(self, element):
        if self.first == 0:
            self.utvidleft()
        self.array[self.first-1] = element
        self.lengde += 1
        self.first -= 1

    # Legger inn det oppgitte elementet på oppgitt indeks, og forskyver alle elementer som ligger
    # etterpå ett hakk bak
    # Best case på slutten O(1)
    # Worst case starten O(n)
    # Gjennomsnitt: Forventningsverdi n/2, O(n)
    def insert(self, indeks, element):
        indeks = self.getandverify_index(indeks)
        if indeks > self.lengde // 2:
            if self.lengde + self.first >= len(self.array):
                self.utvid()
            for index in range(self.lengde-1, indeks-1, -1):
                self.array[index+self.first+1] = self.array[index+self.first]
            self.array[indeks + self.first] = element
        else:
            if self.first <= 0:
                self.utvidleft()
            for index in range(self.first, self.first+indeks+1):
                self.array[index-1] = self.array[index]
            self.first -= 1
            self.array[indeks+self.first] = element
        self.lengde += 1

    # Overskriver det som ligger på oppgitt indeks med det oppgitte elementet.
    # Tilsvarer Python liste[indeks] = element
    # Kjøretid Theta(1)
    def put(self, indeks, element):
        if indeks < 0:
            indeks = self.lengde + indeks
        if not (0 <= indeks < self.lengde):
            raise IndexError("Out of range")
        self.array[indeks+self.first] = element

    # Fjerner første forekomst av oppgitt element
    # Kjøretid Theta(n)
    def remove(self, element):
        index = self.search(element)
        self.delete(index)

    # Fjerner elementet på oppgitt indeks
    # Tilsvarer Python del liste[indeks]
    # Kjøretid er antall elementer som må flyttes
    # Best case siste element O(1)
    # Worst case første element O(n)
    # Gjennomsnitt O(n)
    def delete(self, indeks):
        for i in range(indeks + self.first, self.lengde + self.first - 1):
            self.array[i] = self.array[i+1]
        self.array[self.lengde + self.first - 1] = 0
        self.lengde -= 1

    # Legger alle elementete i oppgitt samling til i lista
    # Kjøretid O(m) best case
    # Kjøretid O(n + m) worst case
    def append_all(self, samling):
        if self.lengde + len(samling) >= len(self.array):
            self.utvid((self.lengde + len(samling))*2)
        for element in samling:
            self.append(element)

    # Setter inn den oppgitte samlingen på oppgitt indeks, og forskyver alt som ligger bak
    # Kjøretid som en flytting + lengden til den nye lista
    def insert_all(self, indeks, samling):
        if self.lengde + len(samling) >= len(self.array):
            self.utvid((self.lengde + len(samling))*2)
        for i in range(self.lengde-1, indeks-1, -1):
            self.array[i+len(samling)] = self.array[i]
        for i in range(len(samling)):
            self.array[indeks+i] = samling[i]

    # O(1)
    def pop(self):
        if self.lengde <= 0:
            raise ValueError("Can't pop a empty list")
        item = self.array[self.first + self.lengde - 1]
        self.array[self.first + self.lengde - 1] = 0
        self.lengde -= 1
        return item

    # O(1)
    def popleft(self):
        if self.lengde <= 0:
            raise ValueError("Can't pop a empty list")
        item = self[0]
        self.array[self.first] = 0
        self.lengde -= 1
        self.first += 1
        movenum = int(len(self.array) * 0.55)
        if self.first > movenum:
            ny_first = int(movenum * 0.3)
            for ny_index, index in enumerate(range(self.first, self.first+self.lengde+1)):
                self.array[ny_first + ny_index] = self.array[index]
                self.array[index] = 0
            self.first = ny_first
        return item

    # Returnerer elementet på oppgitt indeks.
    # Tilsvarer Python variabel = liste[indeks]
    # Kjøretid Theta(1)
    def get(self, indeks):
        if indeks < 0:
            indeks = self.lengde + indeks
        if not (0 <= indeks < self.lengde):
            raise IndexError("Out of range")
        return self.array[indeks+self.first]

    # Finner første indeks hvor dette elementet forekommer
    # Kjøretid som sekvensielt søk
    def search(self, element):
        for index in range(self.lengde):  # Kjører maks n ganger
            if element == self.array[index]:  # Kjører maks n ganger
                return index  # Kjører maks 1 gang
        return -1  # Kjører maks 1 gang

    def reverse(self):
        ny_array = np.zeros(len(self.array), object)
        last = self.first + self.lengde - 1
        for index in range(self.first, last+1):
            ny_array[last-index+self.first] = self.array[index]
        self.array = ny_array

    def getandverify_index(self, indeks):
        if indeks < 0:
            indeks = self.lengde + indeks
        if not (0 <= indeks < self.lengde):
            raise IndexError("Out of range")
        return indeks

    def verify_range(self, start, end, step):
        if step == 0 or (start < end and step < 0) or (start > end and step > 0):
            raise ValueError(f"Can't generate numbers from {start} to {end} by stepping {step}")

    # Gå gjennom lista, element for element
    def __iter__(self):
        return ArrayListIterator(self)

    # Python spesialmetoder slik at array-lista kan brukes som en Python liste. Ikke forelest siden
    # det ikke er en sentral del av faget DAT200.
    def __getitem__(self, item):
        if type(item) == slice:
            ny_liste = []
            step = (item.step if item.step else 1)
            start = self.getandverify_index(item.start)
            stop = self.getandverify_index(item.stop)
            stop += step//abs(step)
            self.verify_range(start, stop, step)
            print(f"Range {start} {stop} {step}")
            for i in range(start, stop, step):
                ny_liste.append(self.get(i))
            return ny_liste
        return self.get(item)

    def __setitem__(self, key, value):
        if type(key) == slice:
            for k in value:
                break
            if len(value) != (key.stop - key.start + 1):
                raise IndexError(f"Expected iterable with length {key.stop - key.start + 1}; not {len(value)}")
            start = self.getandverify_index(key.start)
            stop = self.getandverify_index(key.stop)
            for index in range(start, stop+1):
                self.put(index, value[index-start])
            return
        self.put(key, value)

    def __contains__(self, item):
        if self.search(item) != -1:
            return True
        return False

    def __delitem__(self, key):
        self.delete(key)

    # O(n)
    def __str__(self):
        string = "["
        first = True
        for index in range(self.lengde):
            item = self.get(index)
            if not first:
                string += ", "
            else:
                first = False
            string += f"{item}"
        string += "]"
        return string


class ArrayListIterator:
    def __init__(self, lista):
        self.lista = lista
        self.nv_element = 0

    def __next__(self):
        if self.nv_element >= len(self.lista):
            raise StopIteration
        resultat = self.lista.get(self.nv_element)
        self.nv_element += 1
        return resultat


if __name__ == "__main__":
    liste = ArrayListe(5)
    liste.append(6)
    liste.append(9)
    liste.append(-2)
    liste.append(5)
    liste.append(7)
    liste.delete(1)
    liste.utvidleft(12)
    liste.appendleft(2)
    liste.appendleft(3)
    liste.appendleft(4)

    print(liste.array)
    print(liste)
    print()

    # import random
    import time
    while True:
        time.sleep(0.2)
        # k = random.randint(1, 9)
        liste.append(liste.popleft())
        print(liste.array)
