import random
import time
from solution import Solution


def random_search_continuous(problem, time_limit):
    """ on x = [0, 0, ..., 0] """
    best = Solution(problem.d, problem.n)
    best.x = [0] * problem.n                                      # on met x à 0
    best.z = [random.uniform(-1, 1) for _ in range(problem.d)]    # z est pris aléatoire
    problem.eval(best)

    start = time.time()

    while time.time() - start < time_limit:
        current = Solution(problem.d, problem.n)
        current.x = [0] * problem.n
        current.z = [random.uniform(-1, 1) for _ in range(problem.d)]
        problem.eval(current)

        if current.f < best.f:
            best = current

    return best