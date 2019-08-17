import numpy as np
import time
import sys

subsquares = {1: [(0, 0), (1, 0), (2, 0),
                      (0, 1), (1, 1), (2, 1),
                      (0, 2), (1, 2), (2, 2)],
                  2: [(3, 0), (4, 0), (5, 0),
                      (3, 1), (4, 1), (5, 1),
                      (3, 2), (4, 2), (5, 2)],
                  3: [(6, 0), (7, 0), (8, 0),
                      (6, 1), (7, 1), (8, 1),
                      (6, 2), (7, 2), (8, 2)],
                  4: [(0, 3), (1, 3), (2, 3),
                      (0, 4), (1, 4), (2, 4),
                      (0, 5), (1, 5), (2, 5)],
                  5: [(3, 3), (4, 3), (5, 3),
                      (3, 4), (4, 4), (5, 4),
                      (3, 5), (4, 5), (5, 5)],
                  6: [(6, 3), (7, 3), (8, 3),
                      (6, 4), (7, 4), (8, 4),
                      (6, 5), (7, 5), (8, 5)],
                  7: [(0, 6), (1, 6), (2, 6),
                      (0, 7), (1, 7), (2, 7),
                      (0, 8), (1, 8), (2, 8)],
                  8: [(3, 6), (4, 6), (5, 6),
                      (3, 7), (4, 7), (5, 7),
                      (3, 8), (4, 8), (5, 8)],
                  9: [(6, 6), (7, 6), (8, 6),
                      (6, 7), (7, 7), (8, 7),
                      (6, 8), (7, 8), (8, 8)]}


def split_board(board):
    subsquares = {1: board[0:3, 0:3],
                  2: board[0:3, 3:6],
                  3: board[0:3, 6:9],
                  4: board[3:6, 0:3],
                  5: board[3:6, 3:6],
                  6: board[3:6, 6:9],
                  7: board[6:9, 0:3],
                  8: board[6:9, 3:6],
                  9: board[6:9, 6:9]}
    return subsquares


def check_board(board):
    solved_rows = {}
    solved_cols = {}
    # Do a board check!
    correct = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    dims = np.array(board).shape
    state = np.array(board)
    rows = {}
    nr_fin = 0
    for row in range(dims[0]):
        rows[row] = np.unique(state[row, :])
        if np.unique(state[row, :]).all() == np.array(correct).all():
            solved_rows[row] = True
            nr_fin += 1
        else:
            missing_row = []
            for num in correct:
                if num not in np.unique(state[row,:]):
                    missing_row.append(num)
            solved_rows[row] = missing_row

    cols = {}
    nc_fin = 0
    for col in range(dims[1]):
        cols[col] = np.unique(state[:, col])
        if np.unique(state[:, col]).all() == np.array(correct).all():
            solved_cols[col] = True
            nc_fin += 1
        else:
            missing_col = []
            for n in correct:
                if n not in np.unique(state[:, col]):
                    missing_col.append(n)
            solved_cols[col] = missing_col
    solved = False
    if nr_fin == dims[0] and nc_fin == dims[1]:
        solved = True
    # TODO: Also check 3x3 sub squares to contain correct list?
    return solved_cols, solved_rows, solved


def check_missing(subset):
    check = [1,2,3,4,5,6,7,8,9]
    missing = []
    for n in check:
        if n not in subset:
            missing.append(n)
    return missing


def educated_guess(board, zerod):
    """
    Algorithm for solving:
    [1] Pick number 1-9
    [2] Find num in each sub square, and cancel all adjacent
    rows/cols, hoping to swap num with zeros in sub squares
    not containing selected num.
    [3] Scan adjacent rows and columns to complete their 1-9
     ^ (Only useful when there are rows and columns with one
    or two zeros.
    :param board:
    :return:
    """
    squares = split_board(board)
    start = np.random.random_integers(1, 9, 1)[0]
    # start = 5
    print 'starting with  %s' % start
    locations = []
    subcontain = list()
    empty_subsquares = []
    for sq in squares.keys():
        if start in np.array(squares[sq]).flatten():
            subcontain.append(sq)
        else:
            empty_subsquares.append(sq)

    for square in subcontain:
        ii = 0
        for row in squares[square]:
            for element in row:
                pos = subsquares[square][ii]
                if element == start:
                    locations.append(pos)
                ii += 1

    print '%d is in %s ' % (start, subcontain)
    print '(Missing from %s)' % (empty_subsquares)
    return board


def locate_zeros(squares):
    zed = []
    for sq in squares.keys():
        ii = 0
        for row in squares[sq]:
            for element in row:
                if element == 0:
                    zed.append(subsquares[sq][ii])
                ii += 1
    n_zed = len(zed)
    pempty = float(n_zed)/81*100
    print '%d Zeros Found [%s Percent Empty]' % (n_zed,str(pempty))
    return zed, pempty


def main():
    debug = True
    if 'test' in sys.argv and len(sys.argv) == 3:
        t0 = time.time()
        board = []
        test = open(sys.argv[2], 'r').read().split('\n')
        for row in test:
            r = []
            for e in row.split(' '):
                if e == '_':
                    r.append(0)
                else:
                    r.append(int(e))
            board.append(r)
        board = np.array(board)
        if debug:
            print '\033[1m=====================================\033[0m'
            print '\033[1m\033[31mTest Board Loaded: \033[0m\033[1m'
            print board
            print '=====================================\033[0m'
        rnd = 0
        solved = False
        while not solved:
            cols, rows, solved = check_board(board)
            zeros, unsolved_ratio = locate_zeros(split_board(board))
            board = educated_guess(board, zeros)
            print board
            if solved:
                print '\033[1m\033[31mFINISHED! \033[0m\033[1m[%s]\033[0m' % str(time.time() - t0)

            if debug and rnd >=1:
                break
            rnd += 1

if __name__ == '__main__':
    main()
