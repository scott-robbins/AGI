import random
import time


def generate_walk(start, length):
    x = start[0]
    y = start[1]
    walk = [start]
    moves = []
    directions = {1: [x - 1, y - 1], 2: [x, y - 1], 3: [x + 1, y - 1],
                  4: [x - 1, y], 5: [x, y], 6: [x + 1, y],
                  7: [x - 1, y + 1], 8: [x, y + 1], 9: [x + 1, y + 1]}
    [moves.extend(random.sample(directions.keys(), 1)) for j in range(length)]
    for step in moves:
        directions = {1: [x - 1, y - 1], 2: [x, y - 1], 3: [x + 1, y - 1],
                      4: [x - 1, y], 5: [x, y], 6: [x + 1, y],
                      7: [x - 1, y + 1], 8: [x, y + 1], 9: [x + 1, y + 1]}
        [x, y] = directions[step]
        walk.append([x, y])
    return walk, moves


generate_walk([50, 50], 25)
