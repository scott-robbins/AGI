import matplotlib.animation as animation
import matplotlib.pyplot as plt
import scipy.ndimage as ndi
import maze_builder
import numpy as np
import imutils
import time
import sys
import os

tic = time.time()


def run(goal, maze):
    # Determine where to start/stop based on goals
    bounded_x, bounded_y = get_objective(goal)
    cathode, anode = initialize(maze, bounded_x, bounded_y)
    # Find the path of least resistance
    solutions = []
    pathways = {}
    scores = []
    for c in cathode:
        for a in anode:
            path, complete, cost = estimate_pathways(maze, c, a, 500)
            scores.append(cost)
            pathways[int(cost)] = path
            if complete:
                solutions.append(int(cost))
                print '[*] Pathway found from %s->%s' % (str(c),str(a))
    print '%d Paths Found. Sifting through cost functions scores...' % len(pathways)
    best = np.array(scores).min()
    n_good = 0
    for steps in scores:
        if int(steps) == best:
            n_good += 1
    print '[* FINISHED %ss Elapsed *]' % str(time.time()-tic)
    print '[*] %d Complete Solutions Found' % len(solutions)
    print '[*] Best Score: %s [%d best paths]' % (str(best), n_good)
    if int(best) in pathways.keys():
        if pathways[int(best)] not in solutions:
            print '** Not a complete soluton'
    # Animate the best one
    world = np.zeros((maze.shape[0],maze.shape[1],3))
    world[:,:,2] = maze
    imutils.animate_steps(pathways[int(best)], world)
    return len(solutions)


def estimate_pathways(state, start, stop, limit):
    kn = [[1,1,1,1,1,1],
          [1,1,1,1,1,1],
          [1,1,0,0,1,1],
          [1,1,0,0,1,1],
          [1,1,1,1,1,1],
          [1,1,1,1,1,1]]
    terrain = ndi.convolve(state, kn, origin=0)
    avg = terrain.mean()
    steps = []
    complete = False
    score = 0
    while not complete or len(steps)<limit:
        [x1, y1] = start
        grad = terrain[x1, y1]
        moves = {1: [x1-1,y1-1],  2: [x1, y1-1], 3: [x1+1, y1-1],
                 4: [x1-1, y1],   5: [x1, y1],   6: [x1+1, y1],
                 7: [x1-1, y1+1], 8: [x1, y1+1], 9: [x1+1, y1+1]}
        best_next = {}
        for opt in moves.keys():
            [xi, yi] = moves[opt]
            try:
                score = grad + np.sqrt((stop[0]-xi) ** 2 + (stop[1]-yi) ** 2)
                if terrain[xi, yi] < avg or state[xi, yi] == 0:
                    best_next[score] = opt
            except IndexError:
                pass
        best_score = (np.array(best_next.keys()).min())
        choice = moves[best_next[best_score]]
        steps.append(moves[best_next[best_score]])
        start = choice
        score += best_score
        # print 'Best Score: %d' % best_score
        # print 'Position: %s' % str(choice)
        if start == stop:
            complete = True
    return steps, complete, score


def initialize(maze, boundsx, boundsy):
    X = maze.shape[0] - 1
    Y = maze.shape[1] - 1
    # Handle Up/Down
    if not boundsy and boundsy:
        zerosL = []
        zerosR = []
        k = [[0, 0, 0, 0],
             [1, 1, 1, 1],
             [1, 1, 1, 1],
             [1, 1, 1, 1]]
        ey1 = ndi.convolve(maze, k, origin=0)[0, :]
        ey2 = ndi.convolve(maze, k, origin=0)[X, :]
        dy = 0
        for py1 in ey1:
            if py1 == 0:
                zerosL.append([0, dy])
            dy += 1
        dy = 0
        for py2 in ey2:
            if py2 == 0:
                zerosR.append([X, dy])
            dy += 1
        print '[*] %d Possible starting points' % len(zerosR)
        print '[*] %d Possible ending points' % len(zerosL)
        return zerosL, zerosR
    # Handle Left/Right
    if not boundsx and boundsy:
        zerosD = []
        zerosU = []
        k = [[0, 1, 1, 1],
             [0, 1, 1, 1],
             [0, 1, 1, 1],
             [0, 1, 1, 1]]
        ex1 = ndi.convolve(maze, k, origin=0)[:, 0]
        ex2 = ndi.convolve(maze, k, origin=0)[:, Y]
        dx = 0
        for px in ex1:
            if px == 0:
                zerosD.append([dx, 0])
            dx += 1
        dx = 0
        for px2 in ex2:
            if px2 == 0:
                zerosU.append([dx, Y])
            dx += 1
        print '[*] %d Possible starting points' % len(zerosD)
        print '[*] %d Possible ending points' % len(zerosU)
        return zerosD, zerosU


def get_objective(goals):
    anyHeight = False
    anyWidth = False
    x1 = 0;     x2 = 0
    y1 = 0;     y2 = 0
    if 'x1' in goals.keys():
        x1 = goals['x1']
    if 'x2' in goals.keys():
        x2 = goals['x2']
    if 'y1' in goals.keys():
        y1 = goals['y1']
    if 'y2' in goals.keys():
        y2 = goals['y2']
    if y1-y2 == 0: # Left Right
        anyHeight = True
    if x1-x2 == 0:    # Up Down
        anyWidth = True
    if anyHeight:
        print 'Moving Left/Right [%s,%s] -> [%s,%s]' % (x1, y1, x2, y2)
    if anyWidth:
        print 'Moving Up/Down [%s,%s] -> [%s,%s]' % (x1, y1, x2, y2)
    return anyWidth, anyHeight


w = 250; h = 250
# state = np.zeros((w, h))
# First Create a maze (develop with different styles for more robust solvers)
maze = maze_builder.organic_maze_1(maze_builder.seed_maze())
# The Goal is going to be to get from one side to another
# This might be top to bottom/left to right or some other combo
goal_one = {'x1': 0, 'x2': w}   # RIGHT
goal_two = {'x1': w, 'x2': 0}   # LEFT
goal_tre = {'y1': 0, 'y2': h}   # DOWN
goal_four = {'y1': h, 'y2': 0}  # UP

# An additional goal will be to do so in the minimal number of steps
# You MUST only travel through squares that are 0s

if 'run' in sys.argv:
    plt.title('MAZE')
    plt.imshow(maze)
    plt.show()
    solved = run(goal_two, maze)
    if not solved:
        solved = run(goal_one, maze)
    if not solved:
        solved = run(goal_tre, maze)
