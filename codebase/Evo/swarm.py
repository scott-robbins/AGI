import matplotlib.animation as animation
import matplotlib.pyplot as plt
import scipy.ndimage as ndi
import networkx as nx
import numpy as np
import utility
import time


class Point:
    x = 0
    y = 0
    v = []
    steps = list()

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def set_velocity(self, dx, dy):
        self.v = [dx, dy]

    def update(self):
        if self.v:
            self.x += self.v[0]
            self.y += self.v[1]


def select_swarm_leader(points, verbose):
    ii = 0
    nn = {}
    # Choose leader by whose the most connected
    for p1 in points:
        cnxs = []
        for p2 in points:
            if p1 != p2:
                cnxs.append(np.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[0]) ** 2))
        nn[int(np.array(cnxs).mean())] = p1
        ii += 1

    leader = np.array(nn[np.array(nn.keys()).min()])
    if verbose:
        print 'Leader Chosen: [%d,%d]' % (leader[0], leader[1])

    vectors = {}
    for pi in points:
        Point1 = Point(pi[0], pi[1])
        if pi[0] == leader[0] and pi[1] == leader[1]:
            vectors[Point1] = []
        for pj in points:
            Point2 = Point(pj[0], pj[1])
            if pi != pj and pi[0] == leader[0] and pi[1] == leader[1]:
                vectors[Point1].append([Point1, Point2])

    if verbose:
        for k in vectors.keys():
            for connection in vectors[k]:
                print '[%d,%d]<->[%d,%d]' % (connection[0].x, connection[0].y,
                                             connection[1].x, connection[1].y)
    return leader, vectors


width = 250
height = 250

state = np.zeros((width, height))
n_agents = 4
points = []

for point in range(n_agents):
    [x, y] = utility.spawn_random_point(state)
    points.append([x, y])
    state[x, y] = 1

step_size = 5

leader, vectors = select_swarm_leader(points, True)
alpha = vectors.keys().pop()
alpha.steps = utility.spawn_random_walk([alpha.x, alpha.y], step_size)
for point in vectors[alpha]:
    point.steps = utility.spawn_random_walk([point.x, point.y], step_size)


