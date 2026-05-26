import math
import random
import time
from solution import Solution

# ------------------------------------------------------------------ #
#  Simulated Annealing binaire                                        #
# ------------------------------------------------------------------ #

def simulated_annealing_binary(problem, time_limit):
    # Solution initiale aleatoire
    best = Solution(problem.d, problem.n)
    best.x = [random.randint(0, 1) for _ in range(problem.n)]
    problem.eval(best)

    current = Solution(problem.d, problem.n)
    current.x = best.x[:]
    current.f = best.f

    # Parametres de temperature
    T0        = 100.0   # temperature initiale
    T_min     = 0.01    # temperature plancher — evite la division par zero
    cooling   = 0.9999  # taux de refroidissement geometrique

    temperature = T0

    start = time.time()
    while time.time() - start < time_limit:

        # On copie et on flip un bit
        voisin = Solution(problem.d, problem.n)
        voisin.x = current.x[:]
        i = random.randint(0, problem.n - 1)
        voisin.x[i] = 1 - voisin.x[i]
        problem.eval(voisin)

        delta = voisin.f - current.f

        # On accepte si mieux OU avec une probabilite
        if delta < 0 or random.random() < math.exp(-delta / temperature):
            current = voisin

        # On garde le meilleur global
        if current.f < best.f:
            best = current

        # On refroidit — on ne descend pas sous T_min
        if temperature > T_min:
            temperature *= cooling

    return best
