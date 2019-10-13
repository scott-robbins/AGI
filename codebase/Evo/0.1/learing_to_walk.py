import matplotlib.animation as animation
import matplotlib.pyplot as plt
import scipy.ndimage as ndi
import numpy as np
import utility
import time
import sys
import os

tic = time.time()


class Agent:
    xpos = 0
    ypos = 0
    position = [xpos, ypos]
    movements = []
    start = []

    def __init__(self, initial_position):
        self.xpos = initial_position[0]
        self.ypos = initial_position[1]
        self.position = [initial_position[0], initial_position[1]]
        self.start = self.position

    def update(self, x, y,):
        self.xpos = x
        self.ypos = y
        self.position = [x, y]
        self.movements.append([self.xpos, self.ypos])

    def evaluate_path(self, steps, world):
        internal = 0
        for step in steps:
            internal -= 1
            directions = {1: [self.xpos-1, self.ypos-1],
                          2: [self.xpos, self.ypos-1],
                          3: [self.xpos+1, self.ypos-1],

                          4: [self.xpos-1, self.ypos],
                          5: [self.xpos, self.ypos],
                          6: [self.xpos+1, self.ypos],
                          7: [self.xpos-1, self.ypos+1],
                          8: [self.xpos, self.ypos+1],
                          9: [self.xpos+1, self.ypos+1]}
            try:
                state = world[self.xpos, self.ypos]
                disp = utility.get_displacement(self.start, step)
                [self.xpos, self.ypos] = step
                internal += state
                # internal += disp
            except IndexError:
                pass
        print 'Score: %d' % internal
        return internal


if __name__ == '__main__':
    width = 50
    height = 50
    # world = np.random.random_integers(0, 2, width * height).reshape((width, height))
    world = utility.draw_centered_circle(np.zeros((width, height)),20,False)
    start = utility.spawn_random_point(world)
    start = [10,10]
    # test_walk = utility.spawn_random_walk(crawler.position, 100)
    # crawler.evaluate_path(test_walk, world)

    TARGET = -1
    trials = []
    experiment = True
    try:
        while experiment:
            crawler = Agent(start)
            candidate = utility.spawn_random_walk(crawler.position, 150)
            fitness = crawler.evaluate_path(candidate, world)
            trials.append(fitness)
            if fitness >= TARGET:
                experiment = False
                break
    except KeyboardInterrupt:
        print 'Killed! Best Score: %d' % np.max(np.array(trials))
        exit(0)
        pass
    print 'FINISHED <Score: %s> [%ss Elapsed]' % (fitness, str(time.time()-tic))
    utility.render_random_walk(-1,start,candidate,world,frame_rate=100, save={'save':False})
