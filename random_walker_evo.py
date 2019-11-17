from Crypto.Random import get_random_bytes
import matplotlib.pyplot as plt
import scipy.misc as misc
import numpy as np
import base64
import utils
import time
import sys
import os

tic = time.time()


def load_world(W, H, food):
    if not os.path.isfile('random_walker_world.png'):
        print '[*] Saving Randomly Generated World'
        state, pts = utils.generate_world(W, H, food, show=True)
        misc.imsave('random_walker_world.png', state)
    else:
        print '[*] Pre-Generated World Loaded'
        state = np.array(plt.imread('random_walker_world.png'))
    return state


'''  Define World, Create/Load a Universe, Define Evolution Cycle Parameters '''
start = [90, 50]
width = 200
height = 200

SHOW = False
n_food = 150
n_steps = 150
batch_size = 200
n_iterations = 100
mutation_rate = 0.6
mutator_ratio = 0.1
world = load_world(width, height, n_food)

'''     <_Run_Evolution_>   '''
population = {}
scores = {}
for individual in range(batch_size):
    id = base64.b64encode(get_random_bytes(16))
    steps, choices = utils.generate_random_steps(start, n_steps)
    score = utils.check_steps(steps, world)
    population[id] = [steps, choices, score]
    scores[score] = id
best_score = int(np.array(scores.keys()).max())
best_walk = population[scores[best_score]][0]
best_dna = population[scores[best_score]][1]
print 'Best Score: %d' % best_score
print 'Best DNA: %s' % str(best_dna)

for epoch in range(n_iterations):
    score_to_beat = best_score
    mutate = np.array(np.random.random_integers(0,100,batch_size) > int(100*mutation_rate))
    n_mutations = 0
    ii = 0
    for walker in population.keys():
        [moves, dna, fitness] = population[walker]
        if mutate[ii]:
            # Actual amount of the dna to mutate is the mutator_ratio
            changes = np.random(1,9,int(mutator_ratio)*n_steps)
            for gene in dna:

            n_mutations += 1
        ii += 1
if SHOW:
    utils.animate_steps(steps, world)
print '\033[31m\033[1mFINISHED\033[0m \033[1m[%ss Elapsed]\033[0m' % str(time.time()-tic)