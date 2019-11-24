import matplotlib.pyplot as plt
import scipy.ndimage as ndi
import numpy as np
import imutils
import time
import sys
import os

tic = time.time()
'''     DEFAULT GLOBALS '''
w = 350; h = 350
state = np.zeros((w, h))
cx, cy = [int(w/2), int(h/2)]
n_points = 4*(w+h)
shapes = {1: [[1,0],
              [1,1]],
          2: [[0,1],
              [1,1]],
          3: [[1,1],
              [0,1]],
          4: [[1,1],
              [1,0]],
          5: [[1,1],
              [0,0]],
          6: [[0,0],
              [1,1]],
          7: [[1,0],
              [1,0]],
          8: [[0,1],
              [0,1]],
          9: [[1,0],
              [0,1]],
          10: [[0,1],
               [1,0]]}


def seed_maze():
    added = []
    while len(added) < n_points:
        try:
            [x, y] = imutils.spawn_random_point(state)
            added.append([x, y])
            element_id = np.random.random_integers(1, 10, 1)[0]
            state[x - 1:x + 1, y - 1:y + 1] = shapes[element_id]
        except:
            pass
    return state


def organic_maze_1(state):
    ind2sub = imutils.flat_map_creator(state)
    k = [[1, 1, 1, 1, 1, 1],
         [1, 1, 2, 2, 1, 1],
         [1, 1, 0, 0, 1, 1],
         [1, 1, 0, 0, 1, 1],
         [1, 1, 2, 2, 1, 1],
         [1, 1, 1, 1, 1, 1]]
    landscape = ndi.convolve(state, k, origin=0)
    for ii in range(state.shape[0] * state.shape[1]):
        [px, py] = ind2sub[ii]
        # if landscape[px,py] > 28 or (landscape[px,py] and landscape[px,py] % 23):
        #     state[px,py] = 1
        if landscape[px, py] == 8 and not state[px, py]:
            state[px, py] = 1
        if landscape[px, py] % 23 == 1:
            state[px, py] = 1
    return state




