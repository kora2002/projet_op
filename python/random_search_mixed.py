import random
import time
from solution import Solution


def random_search_mixed(problem, time_limit):
    best = Solution(problem.d, problem.n)
    best.z = [random.uniform(-1, 1) for _ in range(problem.d)]
    best.x = [random.randint(0, 1)  for _ in range(problem.n)]
    problem.eval(best)

    start = time.time()

    while time.time() - start < time_limit:
        current = Solution(problem.d, problem.n)
        current.z = [random.uniform(-1, 1) for _ in range(problem.d)]
        current.x = [random.randint(0, 1)  for _ in range(problem.n)]
        problem.eval(current)

        if current.f < best.f:
            best = current

    return best