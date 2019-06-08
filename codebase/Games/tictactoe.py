import numpy as np
import time


class Board:
    state = [[]]
    X = 1
    O = 0
    Null = -1
    draw = {-1: ' ', 1: 'X', 0: 'O'}

    def __init__(self):
        self.state = -1*np.ones((3, 3)).astype(np.int)

    def show_board(self):
        toe = '\t'+self.draw[self.state[0, 0]] + '|' + self.draw[self.state[0, 1]] + '|'+self.draw[self.state[0, 2]]
        toe += '\n\t------\n\t'+self.draw[self.state[1, 0]]+'|'+self.draw[self.state[1, 1]]+'|'+self.draw[self.state[1, 2]]
        toe += '\n\t------\n\t'+self.draw[self.state[2, 0]]+'|'+self.draw[self.state[2, 1]]+'|'+self.draw[self.state[2, 2]]
        print toe

    def blank_squares(self):
        blank = 0
        xs = 0
        os = 0
        for cell in np.array(self.state).flatten():
            if cell == -1:
                blank += 1
            elif cell == 1:
                xs += 1
            elif cell == -1:
                os += 1
        return blank, xs, os

    def set_state(self, pos, mov):
        moves = [0, 1]
        if mov in moves and self.state[pos[0], pos[1]] == -1:
            self.state[pos[0], pos[1]] = mov
            return True
        else:
           return False

    def isComplete(self):
        finished = False
        row1 = self.state[0, :]
        row2 = self.state[1, :]
        row3 = self.state[2, :]

        col1 = self.state[:,0]
        col2 = self.state[:,1]
        col3 = self.state[:,2]

        dag1 = [self.state[0,0], self.state[1,1], self.state[2,2]]
        dag2 = [self.state[0,2], self.state[1,1], self.state[2,0]]

        # BOOLEANS
        r1 = len(np.unique(row1)) == 1 and -1 not in row1
        r2 = len(np.unique(row2)) == 1 and -1 not in row2
        r3 = len(np.unique(row3)) == 1 and -1 not in row3

        c1 = len(np.unique(col1)) == 1 and -1 not in col1
        c2 = len(np.unique(col2)) == 1 and -1 not in col2
        c3 = len(np.unique(col3)) == 1 and -1 not in col3

        d1 = len(np.unique(dag1)) == 1 and -1 not in dag1
        d2 = len(np.unique(dag2)) == 1 and -1 not in dag2
        # Check IF ANY conditions for completion were met
        if r1 or r2 or r3 or c1 or c2 or c3 or d1 or d2:
            finished = True
        return finished


class Player:
    board = Board
    winner = False
    loser = False
    states = {'X': 1, 'O': 0, 'x': 1, 'o': 0}

    def __init__(self, state):
        self.board = state

    def random_move(self, board):
        moved = False
        while not moved:
            x = np.random.random_integers(0, 2, 1)[0]
            y = np.random.random_integers(0, 2, 1)[0]
            val = np.random.random_integers(0, 1, 1)[0]
            moved = board.set_state([x, y], val)
            self.board = board.state

        return board

    def interactive_move(self, board):
        x = int(input('Enter x pos: '))
        y = int(input('Enter y pos: '))
        val = str(raw_input('Enter Val [X,O]: '))
        if val not in self.states.keys():
            print 'Illegal Value!'
            exit(0)
        board.set_state([x, y], self.states[val])
        self.board = board.state
        return board



board = Board()
player1 = Player(board)
robot = Player(board)

blank, Xs, Os = board.blank_squares()

while board.blank_squares()[0] > 0:
    t0 = time.time()
    board = robot.random_move(board)
    if board.isComplete():
        print 'Robot Wins!'
        board.show_board()
        exit(0)

    board.show_board()
    board = player1.interactive_move(board)
    if board.isComplete():
        print 'Player 1 Wins!'
        board.show_board()
        exit(0)
    print '-------------------------------------'

