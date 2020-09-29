import numpy as np
import random

class Game:
    def __init__(self, times = 2, pb = 0.2):
        self.table = np.zeros((4, 4), dtype=int)
        self.num = 0
        self.produce(times = times, pb = pb)
        self.score = 0

    def printTable(self): #print the whole table
        for i in range(4):
            for j in range(4):
                print(str(1 << self.table[i, j]).center(5) if self.table[i, j] != 0 else '.'.center(5), end='')
            print('\n')

    def produce(self, pb = 0.2, times = 1): #produce a number 2 or 4 in a random tile
        for nums in range(times):
            if self.num == 16: return
            self.num += 1
            valid = []
            for i in range(4):
                for j in range(4):
                    if self.table[i, j] == 0: valid.append((i, j))
            self.table[random.choice(valid)] = np.random.choice((1, 2), 1, p=(1.0-pb,pb))[0]

    def act(self, dir = 'w'): #slide in one direction
        table = self.table.copy()
        score = 0
        if dir == 's': #when dealing with other directions, just rotate the matrix
            table = np.rot90(table, 2)
        elif dir == 'a':
            table = np.rot90(table, -1)
        elif dir == 'd':
            table = np.rot90(table, 1)
        for j in range(4):
            arr = table[table[:, j] > 0, j]
            for i in range(1, len(arr)):
                if arr[i] == arr[i - 1]:
                    arr[i], arr[i - 1] = 0, arr[i - 1] + 1
                    score += (1 << (arr[i - 1] + 1))
            table[:, j] = np.pad(arr[arr > 0], (0, 4 - len(arr[arr > 0])), 'constant')
        if dir == 's':
            table = np.rot90(table, 2)
        elif dir == 'a':
            table = np.rot90(table, 1)
        elif dir == 'd':
            table = np.rot90(table, -1)
        if (table == self.table).all(): score = -999
        return (table, score)

    def move(self, dir): #if nothing happened, block the action
        table, score = self.act(dir)
        if score == -999: return False

        self.table = table
        self.num = np.sum(self.table > 0)
        self.score += score
        return True

    def over(self):
        return self.num == 16

def start(): #start a normal game
    g = Game()
    while not g.over():
        g.printTable()
        change = False
        while not change:
            s = input().lower()
            if s in ('w', 'a', 's', 'd'):
                change = g.move(s)
        g.produce()
    print('Game Over!')
    print('Score: ', g.score)

def auto(): #watch the solution of a stupid AI, which fails to reach 512
    g = Game()
    while not g.over():
        g.printTable()
        change = False
        while not change:
            #input()
            select = [g.act(dir) + (dir,) for dir in ('w', 'a', 's', 'd')]
            select.sort(key = lambda x: -x[1])
            print(select[0][2])
            change = g.move(select[0][2])

        g.produce()
    print('Game Over!')
    print('Score: ', g.score)

if __name__ == '__main__':
    auto()