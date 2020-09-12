import time


class Hanoi:
    def __init__(self):
        self.one = [4, 3, 2, 1]
        self.two = []
        self.three = []
        self.stackList = (self.one, self.two, self.three)
        self.movedTo = None

    def run(self):
        print(self)
        i = ""
        while i != "q":
            i = input("Move: ")
            if len(i) == 2 and i[0] in "123" and i[1] in "123":
                self.move(int(i[0]), int(i[1]))
            else:
                self.move("a", "a")

    def cantMove(self, stacknr):
        curStack = self.stackList[stacknr-1]
        for index, stack in enumerate(self.stackList):
            if index == stacknr-1:
                continue
            if len(curStack) == 0 or len(stack) == 0 or curStack[-1] < stack[-1]:
                return False
        return True

    def findFrom(self):
        highest = None
        for nr, stack in enumerate(self.stackList, 1):
            if len(stack) == 0 or self.movedTo == nr or self.cantMove(nr):
                continue
            elif highest is None or self.stackList[highest][0] < stack[0]:
                highest = nr
        return highest

    def findTo(self, _from, goal=3):
        to = None
        sList = list(self.stackList).copy()
        sList.pop(_from-1)
        movePiece = self.stackList[_from-1][-1]
        for j in sList:
            if len(j) == 0:
                continue
            else:
                if not (j[-1] + movePiece % 2 == 0):  # Partall på oddetall, eller oddetall på partall
                    if to:
                        if j[-1] < self.stackList[to-1][-1]:
                            to = self.stackList.index(j)
                    else:
                        to = self.stackList.index(j)
        if to:
            print(0)
            return to
        # print(sList)
        sListGoalIndex = None
        if self.stackList[goal-1] in sList:
            sListGoalIndex = sList.index(self.stackList[goal-1])
        if movePiece % 2 == 1:
            sList.remove(sList[sListGoalIndex])
            # print(1)
            return self.stackList.index(sList[0])+1
        else:
            # print(2)
            print(sList)
            print(sListGoalIndex)
            return self.stackList.index(sList[sListGoalIndex])+1

    def solve(self, wait_ms=0, goal=3):
        _from = self.findFrom()
        to = self.findTo(_from, goal)
        print(f"{_from} -> {to}")
        self.move(_from, to)
        time.sleep(wait_ms/1000)
        self.solve(wait_ms, goal)

    def move(self, _from, to):
        a = []
        for i in [_from, to]:
            if i == 1:
                a.append(self.one)
            elif i == 2:
                a.append(self.two)
            elif i == 3:
                a.append(self.three)
            else:
                print(f"{_from} -> {to}")
                print("\nUnavailable move\n")
                return -1
        _fromStack = a[0]
        toStack = a[1]
        if len(_fromStack) == 0:
            # print("\nCan't move from empty stack\n")
            return -1
        elif len(_fromStack) == 0 or (len(toStack) != 0 and _fromStack[-1] > toStack[-1]):
            # print("\nUnavailable move\n")
            return -1
        else:
            toStack.append(_fromStack.pop())
            self.movedTo = to
            print(f":{self.movedTo}")
            print(self)
            print()
            return 1

    def printpiece(self, size, start=0):
        if size == 1:
            string = "="
            if start:
                while len(string) < 9:
                    string = f" {string} "
            return string
        string = ""
        if start:
            string += "==" + self.printpiece(size-1)
            while len(string) < 9:
                string = f" {string} "
        else:
            string += "==" + self.printpiece(size-1)
        return string

    def __str__(self):
        string = ""
        for line in range(3, -1, -1):
            for nr, stack in enumerate([self.one, self.two, self.three]):
                if nr == 0:
                    string += " | "
                if line < len(stack):
                    string += self.printpiece(stack[line], 1)
                else:
                    string += " "*9
                string += " | "
            string += "\n"
        string += "\n"
        return string


if __name__ == '__main__':
    h = Hanoi()
    h.solve(1000)
