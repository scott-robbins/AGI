from matplotlib.animation import FFMpegWriter
import matplotlib.animation as animation
import matplotlib.pyplot as plt
import scipy.ndimage as ndi
import numpy as np
import utils
import time
import sys
import os


class Cell:
    x = 0
    y = 0
    value = 0
    state = [[]]
    pos = [x, y]

    def __init__(self, position, world, weight):
        self.state = world
        self.initialize(position, weight)

    def initialize(self, start, val):
        self.x = start[0]
        self.y = start[1]
        self.value = val
        self.pos = [self.x, self.y]

    def draw_self(self):
        self.state[self.x, self.y, :] = [1, 0, 0]

    def set_pos(self, new_position):
        self.state[self.x, self.y, :] = 0
        self.x = new_position[0]
        self.y = new_position[1]
        self.pos = [self.x, self.y]
        self.draw_self()

    def steps(self, depth):
        film = []
        film.append([plt.imshow(state)])
        moves = [self.x, self.y]
        for step in range(depth):
            directions = {1:[self.x-1, self.y-1], 2:[self.x, self.y-1], 3:[self.x+1, self.y-1],
                          4:[self.x-1, self.y], 5: [self.x, self.y],  6: [self.x+1, self.y],
                          7:[self.x-1, self.y+1], 8:[self.x, self.y+1], 9:[self.x+1, self.y+1]}
            for n in directions.keys():
                move = directions[n]
                opt = self.state[move[0], move[1]]
                if (opt[0] and opt[1])==0 and opt[2] == 1:
                    self.state[self.x, self.y, :] = 0
                    moves.append(move)
                    self.set_pos(move)
                    film.append([plt.imshow(state)])
                    break
        return moves, film


def build_reel(frames, states):
    return [frames.append(frame) for frame in states]


D = 150
WIDTH = 250
HEIGHT = 250
state = np.zeros((WIDTH, HEIGHT, 3))
state[:, :, 2] += np.random.random_integers(0, 1, WIDTH*HEIGHT).reshape((WIDTH, HEIGHT))
start = [int(WIDTH/2), int(HEIGHT/2)]
print 'Starting at [%d, %d]' % (int(WIDTH/2), int(HEIGHT/2))


f = plt.figure()
film = []
completed = []
LIMIT = int(D*0.6)
print 'Running Simulation. Limit is %d' % LIMIT
time.sleep(3)

while len(completed) < LIMIT:
    crawler = Cell(start, state, 1)
    crawler.draw_self()
    completed, reel = crawler.steps(depth=D)
    print '%d Viable Steps Found' % len(reel)

    film = build_reel(film, reel)
    state = np.zeros((WIDTH, HEIGHT, 3))
    state[:, :, 2] += np.random.random_integers(0, 1, WIDTH * HEIGHT).reshape((WIDTH, HEIGHT))

a = animation.ArtistAnimation(f,reel,interval=25,blit=True,repeat_delay=900)
plt.show()
