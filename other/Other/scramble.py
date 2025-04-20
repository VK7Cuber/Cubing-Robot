import random

turns = ["U", "D", "L", "F", "R", "B",
         "U'", "D'", "L'", "F'", "R'", "B'",
         "U2", "D2", "L2", "F2", "R2", "B2",
         "U2", "D2", "L2", "F2", "R2", "B2"]


def make_scramble():
    scramble = [get_random_turn()]
    for i in range(random.randint(17, 25)):
        turn = get_random_turn()
        while turn[0] == scramble[i][0]:
            turn = get_random_turn()
        scramble.append(turn)
    return scramble


def get_random_turn():
    index = random.randint(0, 23)
    return turns[index]


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
