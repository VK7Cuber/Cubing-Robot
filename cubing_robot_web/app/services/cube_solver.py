from typing import List
from rubik_solver import utils


DEFAULT_SOLVED = 'yyyyyyyyybbbbbbbbbrrrrrrrrrgggggggggooooooooowwwwwwwww'


def solve_kociemba(configuration: str) -> List[str]:
	if configuration == DEFAULT_SOLVED:
		return []
	return utils.solve(configuration, 'Kociemba')
