import scipy.ndimage as ndi
import numpy as np
import sys
import os


def ind2sub(index, shape):
    ii = 0
    for y in range(shape[0]):
        for x in range(shape[1]):
            if index == ii:
                return [x, y]
            ii += 1


def generate_random_soduku_board(difficulty):
    n_super = 9
    dims = [3, 3]
    cells = {}
    for i in range(1, n_super + 1):
        cell = np.zeros(dims)
        fill = np.array(np.arange(0, difficulty))
        np.random.shuffle(fill)
        ii = 0
        for c in cell.flatten():
            [x, y] = ind2sub(ii, dims)
            try:
                cell[x, y] = fill[ii]
            except IndexError:
                cell[x, y] = 0
                pass
            ii += 1
        cells[i] = cell.reshape(dims)
    ''' Now combine into one board
      _____ _____ _____
     |cell1|cell2|cell3|
     |cell4|cell5|cell6|
     |cell7|cell8|cell9|
      -----------------                                                                             '''
    row1 = np.concatenate((cells[1], cells[2], cells[3]), 1)
    row2 = np.concatenate((cells[4], cells[5], cells[6]), 1)
    row3 = np.concatenate((cells[7], cells[8], cells[9]), 1)
    board = np.concatenate((row1, row2, row3), 0)
    # TODO: Make a check to confirm board is legal!!
    return board


# Generate random soduku board
difficulty = 6
board = generate_random_soduku_board(difficulty)

print board