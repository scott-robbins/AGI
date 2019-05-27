import matplotlib.animation as animation
import matplotlib.pyplot as plt
import scipy.ndimage as ndi
import numpy as np
import utility


def random_walk_seeds(config):
    """
    Provide random walk seed data
    for a given configuration (i.e,
    population size, and world dims, etc.)
    :param config:
    :return:
    """
    initial_state = np.zeros((config['width'], config['height']))
    seed_data = {}
    for walker in range(config['initial_population']):
        if config['start']:
            walk = utility.spawn_random_walk(config['start'], config['n_steps'])
        else:
            walk = utility.spawn_random_walk(utility.spawn_random_point(initial_state), config['n_steps'])
        seed_data[walker] = walk
    return seed_data


def create_random_state(config):
    """
    Create a random initial state
    based on the properties of a given
    configuration.
    :param config:
    :return:
    """
    initial_state = np.zeros((config['width'], config['height']))
    for pt in range(config['initial_population']):
        [x, y] = utility.spawn_random_point(initial_state)
        initial_state[x, y] = 1
    return initial_state


def run(config, seeds):
    n_collisions = {}
    for walk in seeds.keys():
        state = create_random_state(config)
        collisions = 0
        pos = config['start']
        config['walks'][walk] = seeds[walk]
        for step in seeds[walk]:
            try:
                state[pos[0], pos[1]] = 0
                if state[step[0], step[1]] == 1:
                    collisions += 1
                state[step[0], step[1]] = 1
                pos = step
            except IndexError:
                pass
        n_collisions[walk] = collisions
    config['collisions'] = n_collisions
    return config


def assign_fitness(config):
    avg = np.array(config['collisions'].values()).mean()
    top = np.array(config['collisions'].values()).max()
    displacement = list()
    cost = {}
    for id in range(len(config['walks'])):
        walk = config['walks'][id]
        counts = config['collisions'][id]
        stop = walk[len(walk)-2]
        start = config['start']
        disp = np.sqrt(((stop[0]-start[0])**2)+((stop[1]-start[1])**2))
        displacement.append(disp)
        ''' COST FUNCTION '''
        cost[id] = (counts**2)*avg/top + disp
    '''  Mutation Threshold defined as mean of Cost '''
    thresh = np.array(cost.values()).mean()
    mutates = {}
    for j in cost.keys():
        if cost[j] >= thresh:
            mutates[j] = False
        else:
            mutates[j] = True
    ''' If Mutates[id] steps mutated/total_steps == config['mutation_rate'] '''
    if len(mutates.keys()) == len(config['walks']):
        print 'Mutating Generation'
        config = mutate_dataset(config, mutates)
    return config


def mutate_dataset(config, mutates):
    for id in mutates.keys():
        if mutates[id]:
            walk = config['walk'][id]
    return config


def main():
    config = {'width': 250,
              'height': 250,
              'n_steps': 100,
              'start': [120, 120],
              'initial_population': 1000,
              'n_generations': 1000,
              'mutation_rate': 0.5,
              'walks': {}}

    seed_walks = random_walk_seeds(config)
    # Before walks can be evaluated/mutated
    # Need to have goals defined
    state = create_random_state(config)
    # Preview
    # plt.imshow(state, 'gray')
    # plt.show()

    '''     GOALS
     [1] - Maximize Eating of Random Particles
     [2] - Maximize Distance from Starting Point
    '''
    config = run(config, seed_walks)
    print 'Mean Collision Count: ' + str(np.array(config['collisions'].values()).mean())
    print 'Max Collision Count: ' + str(np.array(config['collisions'].values()).max())
    print '[' + ' Total Experiments Run]'

    # Now Evaluate the fitness of each walk, and mutate/crossover
    config = assign_fitness(config)
    

if __name__ == '__main__':
    main()

