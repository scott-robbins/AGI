import numpy as np
import time
import sys


def ind2sub(index,dims):
    """
    Given an index and array dimensions,
    convert an index to [x,y] subscript pair.
    :param index:
    :param dims:
    :return tuple - subscripts :
    """
    subs = []
    ii = 0
    for y in range(dims[0]):
        for x in range(dims[1]):
            if index == ii:
                subs = [y, x]
            ii +=1
    return subs


def mat2board(matrix):
    elements = Board.draw
    board = [[]]
    for col in range(matrix.shape[0]):
        R = ''
        for row in range(matrix.shape[1]):
            R+= elements[int(matrix[row, col])] + ' '
        R += '\n'
        board.append(R)
    return board


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
            elif cell == 0:
                os += 1
        return blank, xs, os

    def set_state(self, pos, mov):
        moves = [0, 1]
        if mov in moves and self.state[pos[0], pos[1]] == -1:
            self.state[pos[0], pos[1]] = mov
            return True
        else:
            return False

    def is_complete(self):
        finished = False
        row1 = self.state[0, :]
        row2 = self.state[1, :]
        row3 = self.state[2, :]

        col1 = self.state[:, 0]
        col2 = self.state[:, 1]
        col3 = self.state[:, 2]

        dag1 = [self.state[0, 0], self.state[1, 1], self.state[2, 2]]
        dag2 = [self.state[0, 2], self.state[1, 1], self.state[2, 0]]

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
    hold_center = False
    game_tree = {1: [], -1: [], 0: []}
    oppt_tree = {1: [], -1: [], 0: []}
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
        elif not board.set_state([y, x], self.states[val]):
            print 'False Move?!'
            exit(0)
        board.set_state([y, x], self.states[val])
        self.board = board.state
        return board

    def adversarial_move(self, board, is_opponent):

        blanks, xs, os = self.survey_board(board)
        if [1, 1] in blanks:
            board.set_state([1, 1], 1)
            self.hold_center = True
            return
        else:
            possible_moves = blanks

            choice_loc = possible_moves.pop()
            choice_mov = np.random.random_integers(0,1,1)[0]
            board.set_state(choice_loc, choice_mov)
            return

    def survey_board(self, board):
        blank = []
        xs = []
        os = []
        ii = 0
        for cell in np.array(board.state).flatten():
            if cell == -1:
                blank.append(ind2sub(ii,[3,3]))
            elif cell == 1:
                xs.append(ind2sub(ii,[3,3]))
            elif cell == 0:
                os.append(ind2sub(ii,[3,3]))
            ii += 1
        return blank, xs, os


def main():
    t0 = time.time()
    board = Board()
    player1 = Player(board)
    robot = Player(board)
    blank, Xs, Os = board.blank_squares()
    if '-easy' in sys.argv:
        while board.blank_squares()[0] > 0:
            t0 = time.time()
            board = robot.random_move(board)
            if board.is_complete():
                print 'Robot Wins!'
                board.show_board()
                dt = time.time() - t0
                break

            board.show_board()
            board = player1.interactive_move(board)
            if board.is_complete():
                print 'Player 1 Wins!'
                board.show_board()
                dt = time.time() - t0
                break

            print '-------------------------------------'
        print '\033[1m%ds Elapsed]\033[0m' % dt

    if 'ai_train' in sys.argv:
        # TODO: Medium/Hard
        t0 = time.time()

        n_round = 10
        '''
        Planning Agent w/ Goals:
        ===========================
        * Stopping Opponent Success
        * Achieving goal conditions 
        '''
        history = np.zeros((n_round,3,3))

        base_line = {'random_wins': 0,
                     'smarty_wins': 0}
        i = 0
        while i < n_round:
            ii = 0
            while board.blank_squares()[0] > 0:
                robot2 = Player(board)
                board = robot2.random_move(board)
                if board.is_complete():
                    #board.show_board()
                    history[ii, :, :] = board.state
                    dt = time.time() - t0
                    base_line['random_wins'] += 1
                    break
                robot.adversarial_move(board, True)
                if board.is_complete():
                    #board.show_board()
                    history[ii, :, :] = board.state
                    dt = time.time() - t0
                    base_line['smarty_wins'] += 1
                    break
                history[ii, :, :] = board.state
                ii += 1
            dt = time.time() - t0
            i += 1
        print base_line
        dt = time.time() - t0
        print '\033[1m%ds Elapsed]\033[0m' % dt

        for line in mat2board(history[0]):
            print line

if __name__ == '__main__':
    main()
