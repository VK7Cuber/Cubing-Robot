import sys
import os

# Добавляем корневую директорию проекта в путь
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

def speed_up_algorithm(algorithm):
    speeded_up_algorithm = []
    skip_iteration = False
    for i, movement in enumerate(algorithm):
        if not skip_iteration:
            if not i == len(algorithm) - 1:
                first_movement, second_movement = get_non_conflicting_movements_pair(movement[0])
                if algorithm[i+1][0] == first_movement or algorithm[i+1][0] == second_movement:
                    speeded_up_movement = movement + algorithm[i+1]
                    speeded_up_algorithm.append(speeded_up_movement)
                    skip_iteration = True
                else:
                    speeded_up_algorithm.append(movement)
            else:
                speeded_up_algorithm.append(movement)
        else:
            skip_iteration = False
            continue
    return speeded_up_algorithm


def get_non_conflicting_movements_pair(movement):
    non_conflicting_movements = {
        "UD": ["U", "D"],
        "FB": ["F", "B"],
        "LR": ["L", "R"]
    }
    for m in non_conflicting_movements.keys():
        if movement in m:
            return non_conflicting_movements[m]
            break
    return None