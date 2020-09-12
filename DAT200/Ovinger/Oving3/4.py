import numpy as np


def mostValuableBag(items, maxWeight):
    bag = np.zeros(len(items), np.zeros(maxWeight))
    print(bag)


def mostValuableBag_helper(items, maxWeight, bag):
    pass


if __name__ == '__main__':
    items = [[6, 368], [7, 292], [4, 65], [8, 187], [2, 300], [10, 394], [9, 442], [6, 473], [5, 266], [4, 68]]
    mostValuableBag(items, 30)

    # items = []
    # for k in range(10):
    #     items.append([random.randint(1, 10), random.randint(10, 500)])
    # print(items)
