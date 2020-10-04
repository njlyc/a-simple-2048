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

    def produce(self, pb = 0.1, times = 1): #produce a number 2 or 4 in a random tile
        for nums in range(times):
            if self.num == 16: return
            self.num += 1
            valid = []
            for i in range(4):
                for j in range(4):
                    if self.table[i, j] == 0: valid.append((i, j))
            self.table[random.choice(valid)] = np.random.choice((1, 2), 1, p=(1.0-pb,pb))[0]

    def evaluate(self, table0, dir ='w'): #slide in one direction
        table = table0.copy()
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
                    score += 1
            table[:, j] = np.pad(arr[arr > 0], (0, 4 - len(arr[arr > 0])), 'constant')
        if dir == 's':
            table = np.rot90(table, 2)
        elif dir == 'a':
            table = np.rot90(table, 1)
        elif dir == 'd':
            table = np.rot90(table, -1)
        if (table == table0).all(): score = -999 #this means no changes are made
        return (table, score)

    def move(self, dir): #if nothing happened, block the action
        table, score = self.evaluate(self.table, dir)
        if score == -999: return False

        self.table = table
        self.num = np.sum(self.table > 0)
        self.score += score
        return True

    def over(self):
        return self.num == 16 and all(map(lambda x: self.evaluate(self.table, x)[1] == -999, ('w', 'a', 's', 'd')))

def start(): #start a normal game
    g = Game()
    while not g.over():
        g.printTable()
        change = False
        while not change:
            s = input().lower()
            if s in ('w', 'a', 's', 'd'):
                change = g.move(s)
            if not change: print("This move is forbidden. Make some difference!")
        g.produce()
    print('Game Over!')
    print('Score: ', g.score)

def auto(): #watch the solution of a greedy AI, which fails to reach 512
    g = Game()
    while not g.over():
        g.printTable()
        #input()
        select = [g.evaluate(g.table, dir) + (dir,) for dir in ('w', 'a', 's', 'd')]
        select.sort(key = lambda x: -x[1])
        print(select[0][2])
        g.move(select[0][2])

        g.produce()
    print('Game Over!')
    print('Score: ', g.score)

def auto2():
    # calculate the possible situations in future 3 steps
    # still using greedy algorithms
    # sometimes it reaches 1024
    g = Game()
    step = 0
    while not g.over():
        #g.printTable()
        step += 1
        solution = []
        for i in ('w', 'a', 's', 'd'):
            table1, s1 = g.evaluate(g.table, i)
            if s1 < 0: continue
            for j in ('w', 'a', 's', 'd'):
                table2, s2 = g.evaluate(table1, j)
                if s2 < 0: continue
                for k in ('w', 'a', 's', 'd'):
                    table3, s3 = g.evaluate(table2, k)
                    if s3 < 0: continue
                    solution.append((s1, s2, s3, i))
        solution.sort(key = lambda x: (x[0] + x[1] + x[2], x[0] + x[1], x[0], x[1], x[2]), reverse = True)
        g.move(solution[0][3])
        #print(solution[0][3])
        g.produce()
    g.printTable()
    print('Game Over!')
    print('Score: ', g.score, 'Steps:', step)

def debug():
    g = Game()
    g.table = np.ones((4, 4), dtype=int)
    g.num = 16
    g.printTable()
    print(g.over())

if __name__ == '__main__':
    auto2()
