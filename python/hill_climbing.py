


import random
import time
from solution import Solution

# ------------------------------------------------------------------ #
#  Hill Climbing binaire                                              #
# ------------------------------------------------------------------ #

def hill_climbing_binary(problem, time_limit):
    # On part d'une solution aléatoire
    best = Solution(problem.d, problem.n)
    best.x = [random.randint(0, 1) for _ in range(problem.n)]
    problem.eval(best)

    start = time.time()
    while time.time() - start < time_limit:
        # On copie la solution actuelle
        current = Solution(problem.d, problem.n)
        current.x = best.x[:]

        # On inverse un bit aléatoire
        i = random.randint(0, problem.n - 1)
        current.x[i] = 1 - current.x[i]

        problem.eval(current)

        # Si c'est mieux on avance
        if current.f < best.f:
            best = current

    return best