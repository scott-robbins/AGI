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


def generate_world(width, height, n_food, show):
    world = np.zeros((width, height, 3))
    bits = []
    while len(bits) < n_food:
        [x, y] = spawn_random_point(world)
        try:
            if (world[x, y, 1] and world[x, y, 0] and world[x, y, 2]) == 0:
                world[x, y, :] = [0, 1, 0]
                bits.append([x, y])
        except IndexError:
            pass
    if show:
        plt.imshow(world)
        plt.show()
    return world, bits


def check_steps(moves, world):
    score = 0
    for step in moves:
        try:
            x = int(step[0])
            y = int(step[1])
            if world[x, y, 1] == 1 and (world[x, y, 0] and world[x, y, 2]) == 0:
                score += 1
        except TypeError:
            pass
    return score


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