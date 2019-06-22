import numpy as np
import time
import sys


def split_board(board):
    s1 = board[0:3, 0:3]
    s2 = board[0:3, 3:6]
    s3 = board[0:3, 6:9]
    s4 = board[3:6, 0:3]
    s5 = board[3:6, 3:6]
    s6 = board[3:6, 6:9]
    s7 = board[6:9, 0:3]
    s8 = board[6:9, 3:6]
    s9 = board[6:9, 6:9]
    subsquares = [[s1, s2, s3],
                  [s4, s5, s6],
                  [s7, s8, s9]]
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
    print '====================================='
    print 'Test Board Loaded: '
    print board
    print '====================================='

    squares = split_board(board)
    solved = False
    # while not solved:
    #     cols, rows, solved = check_board(board)
    #     if solved:
    #         print '\033[1m\033[31mFINISHED! \033[0m\033[1m[%s]\033[0m' % str(time.time()-t0)
    #     # Swap out the zeros
    #     for col in cols:
    #         if not col:
    cols, rows, solved = check_board(board)
    # Swap out the zeros
    for col in cols:
        if type(cols[col]) == list:
            print np.array(cols[col]).nonzero()
    for row in rows:
        if type(rows[row]) == list:
            print np.array(rows[row]).nonzero()


