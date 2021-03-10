import dijkstra


class A:
    def __init__(self):
        self.num = 2

    def inc(self, n):
        self.num += n
        print(n)

    def printa(self, item):
        print(item)

    def printb(self, item):
        print(f">{item}")

    def printc(self, item):
        print(f"<{item}>")

    def printd(self, item):
        print(f":{item}")


if __name__ == '__main__':
    a = A()
    print(a.num)
    print()
    b = dijkstra.dijkstra(a)
    print()
    print(a)
    print(b)
    print(a.num)
