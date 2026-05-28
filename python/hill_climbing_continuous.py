import random
import time
from solution import Solution


def _clip(value, lo=-1.0, hi=1.0):
    return max(lo, min(hi, value))


def hill_climbing_continuous(problem, time_limit, sigma=0.1):
    current = Solution(problem.d, problem.n)
    current.x = [0] * problem.n
    current.z = [random.uniform(-1, 1) for _ in range(problem.d)]
    problem.eval(current)

    best = Solution(problem.d, problem.n)
    best.x = current.x[:]
    best.z = current.z[:]
    best.f = current.f

    no_improve_count = 0
    max_no_improve = 2 * problem.d

    start = time.time()

    while time.time() - start < time_limit:

        indices = list(range(problem.d))
        random.shuffle(indices)
        improved = False

        for i in indices:
            if time.time() - start >= time_limit:
                return best

            neighbor = Solution(problem.d, problem.n)
            neighbor.x = [0] * problem.n
            neighbor.z = current.z[:]
            neighbor.z[i] = _clip(neighbor.z[i] + random.gauss(0, sigma))
            problem.eval(neighbor)

            if neighbor.f < current.f:
                current = neighbor

                if current.f < best.f:
                    best = Solution(problem.d, problem.n)
                    best.x = current.x[:]
                    best.z = current.z[:]
                    best.f = current.f

                improved = True
                break

        if improved:
            no_improve_count = 0
        else:
            no_improve_count += 1

        if no_improve_count >= max_no_improve:
            break

    return best