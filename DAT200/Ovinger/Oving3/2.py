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

    def move(n, source, target, auxiliary, wait_ms):
        if n > 0:
            # Move n - 1 disks from source to auxiliary, so they are out of the way
            move(n - 1, source, auxiliary, target, wait_ms)

            # Move the nth disk from source to target
            target.append(source.pop())

            # Display our progress
            time.sleep(wait_ms / 1000)
            print(1)

            # Move the n - 1 disks that we left on auxiliary onto target
            move(n - 1, auxiliary, target, source, wait_ms)

    move(4, h.one, h.three, h.two, 1000)
