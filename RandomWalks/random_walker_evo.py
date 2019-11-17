from Crypto.Random import get_random_bytes
import matplotlib.pyplot as plt
import scipy.misc as misc
from tqdm import tqdm
import numpy as np
import base64
import utils
import time
import sys
import os

tic = time.time()

'''  Define World, Create/Load a Universe, Define Evolution Cycle Parameters '''
start = [90, 50]
width = 200
height = 200

SHOW = True
n_food = 150
n_steps = 150
batch_size = 200
n_iterations = 100
mutation_rate = 0.6
mutator_ratio = 0.1


def load_world(W, H, food):
    if not os.path.isfile('random_walker_world.png'):
        print '[*] Saving Randomly Generated World'
        state, pts = utils.generate_world(W, H, food, show=True)
        misc.imsave('random_walker_world.png', state)
    else:
        print '[*] Pre-Generated World Loaded'
        state = np.array(plt.imread('random_walker_world.png'))
    return state


def evolution_1(populate):
    bar = tqdm(total=n_iterations)
    for epoch in range(n_iterations):
        ''' 
        For Each Generation mutate the genes of batch individuals
        And ensure that each generation ensures the batch total count (when some die, add fresh)
        '''
        mutate = np.array(np.random.random_integers(0, 100, batch_size) > int(100 * mutation_rate))
        n_mutations = 0
        ii = 0
        for walker in populate.keys():
            [moves, dna, fitness] = populate[walker]
            if mutate[ii]:
                # Actual amount of the dna to mutate is the mutator_ratio
                changes = np.random.random_integers(1, 100, int(mutator_ratio) * n_steps) >= 90
                child_dna = []
                for gene in dna:
                    if changes:
                        child_dna.append(np.random.random_integers(1, 9, 1)[0])
                    else:
                        child_dna.append(gene)
                    n_mutations += 1
                # TODO:
                moves = utils.inds2steps(start, child_dna, world)
                new_score = utils.check_steps(moves, world)
                dna = child_dna
            if not mutate[ii]:
                new_score = fitness
            scores.append(new_score)
            populate[walker] = [moves, dna, fitness]
            # TODO: Not working correctly but hard to tell because I cant watch all of them
            # TODO: Check for new highest fitness at each epoch end
            # TODO:
            ii += 1
        bar.update(1)
    bar.close()
    Best_Final = np.array(scores).max()
    print '[*] Best Final Score: %d' % Best_Final
    print '[*] %d Mutations Total' % n_mutations


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
print 'Best ID: %s' % str(scores[best_score])


# evolution_1(population)
'''   Mutate/Cross-Over   '''
mean_score = np.array(scores.keys()).mean()
mutate = list(np.random.random_integers(0, 100, batch_size) > int(100 * mutation_rate))
above_average = 0
for individual in population.keys():
    [walk, moves, s] = population[individual]
    if s < mean_score:
        if mutate.pop():
            # Actual amount of the dna to mutate is the mutator_ratio
            changes = list(np.random.random_integers(1,100,batch_size) > mutator_ratio*100)
            child_dna = []
            for gene in moves:
                if changes.pop():
                    child_dna.append(np.random.random_integers(1, 9, 1)[0])
                else:
                    child_dna.append(gene)
            new_steps = utils.inds2steps(start, child_dna)
            new_scores = utils.check_steps(new_steps, world)
            if new_scores > best_score:
                print '[*] New Best Score: %d' % new_scores
                best_score = new_scores
                best_walk = new_steps
            # population[individual] = [walk, child_dna, s]

if SHOW:
    print best_walk[0:10]
    utils.animate_steps(best_walk, world)
print '\033[31m\033[1mFINISHED\033[0m \033[1m[%ss Elapsed]\033[0m' % str(time.time()-tic)