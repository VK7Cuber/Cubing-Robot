import random


def make_scramble():
    turns = ["U", "D", "L", "F", "R", "B",
             "U'", "D'", "L'", "F'", "R'", "B'",
             "U2", "D2", "L2", "F2", "R2", "B2",
             "U2", "D2", "L2", "F2", "R2", "B2"]
    scramble = []
    scramble.append(turns[int(make_random_index())])
    for i in range(random.randint(17, 25)):
        index = make_random_index()
        while turns[index][0] == scramble[i][0]:
            index = make_random_index()
        scramble.append(turns[int(index)])
    return scramble

def make_random_index():
    index = random.randint(0, 18) * random.random()
    while not (0 < index < 24):
        index = random.randint(0, 24) * random.random()
    return int(index)


def reverse_algorithm(algorithm):
    reversed_algorithm = []
    for i in range(len(algorithm)):
        if "2" not in algorithm[i]:
            if "'" in algorithm[i]:
                reversed_algorithm.append(algorithm[i][0])
            else:
                reversed_algorithm.append(algorithm[i][0] + "'")
        else:
            reversed_algorithm.append(algorithm[i])
    reversed_algorithm = list(map(str, reversed(reversed_algorithm)))
    return reversed_algorithm

