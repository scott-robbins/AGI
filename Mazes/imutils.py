import matplotlib.animation as animation
import matplotlib.pyplot as plt
import numpy as np
import time
import os


def swap(file_name, destroy):
    data = []
    for line in open(file_name,'r').readlines():
        data.append(line.replace('\n', ''))
    if destroy:
        os.remove(file_name)
    return data


def spawn_random_point(state):
    x_max = np.array(state).shape[0]
    y_max = np.array(state).shape[1]
    x = np.random.random_integers(0, x_max, 1)[0]
    y = np.random.random_integers(0, y_max, 1)[0]
    return [x, y]


def generate_random_steps(start, steps):
    moves = [start]
    choices = []
    x = start[0]
    y = start[0]
    for step in range(steps):
        directions = {1: [x-1, y-1], 2: [x, y-1], 3: [x+1, y-1],
                      4: [x-1, y],   5: [x, y],   6: [x+1, y],
                      7: [x-1, y+1], 8: [x, y+1], 9: [x+1, y+1]}
        opt = np.random.random_integers(1,9,1)[0]
        choice = directions[opt]
        moves.append(choice)
        choices.append(opt)
        x = choice[0]
        y = choice[1]
    return moves, choices


def flat_map_creator(state):
    """
    LoopInvariantHoisting to preallocate a map, that
    pairs a flattened index of a corresponding state to
    an x-y position.
    :param state:
    :return:
    """
    index_map = {}
    ii = 0
    for x in range(state.shape[0]):
        for y in range(state.shape[1]):
            index_map[ii] = [x, y]
            ii += 1
    return index_map


def sub2ind(subs, dims):
    """
    Given a 2D Array's subscripts, return it's
    flattened index
    :param subs:
    :param dims:
    :return:
    """
    ii = 0
    for y in range(dims[1]):
        for x in range(dims[0]):
            if subs[0] == x and subs[1] == y:
                return ii
            ii += 1
    return -1


def ind2sub(index, dims):
    """
    Given an index and array dimensions,
    convert an index to [x,y] subscript pair.
    :param index:
    :param dims:
    :return tuple - subscripts :
    """
    subs = []
    ii = 0
    for x in range(dims[0]):
        for y in range(dims[1]):
            if index==ii:
                subs = [x, y]
                return subs
            ii +=1
    return subs


def load_image(file_name, show):
    matrix = np.array(plt.imread(file_name))
    if show:
        plt.imshow(matrix)
        plt.show()
    return matrix

def animate_steps(moves, world):
    f = plt.figure()
    reel = []
    for i in range(len(moves)):
        if i>0:
            [x, y] = moves[i-1]
            world[x, y, :] = 0
        [x, y] = moves[i]
        world[x,y,:] = [1,0,0]
        reel.append([plt.imshow(world)])
    a = animation.ArtistAnimation(f,reel,interval=100,blit=True,repeat_delay=900)
    plt.show()
