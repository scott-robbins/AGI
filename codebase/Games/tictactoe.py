import numpy as np
import sys


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
        if mov >=0 and pos[0] <= 2 and pos[1] <= 2:
            self.state[pos[0], pos[1]] = mov


class Player:
    board = Board
    winner = False
    loser = False
    states = {'X': 1, 'O': 0, 'x': 1, 'o': 0}

    def __init__(self, state):
        self.board = state

    def random_move(self, board):
        x = np.random.random_integers(0, 2, 1)[0]
        y = np.random.random_integers(0, 2, 1)[0]
        val = np.random.random_integers(0, 1, 1)[0]
        board.set_state([x, y], val)
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
    board = robot.random_move(board)
    board.show_board()
    board = player1.interactive_move(board)
    print '-------------------------------------'

