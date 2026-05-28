import math
import random
import time
from solution import Solution


def _clip(value, lo=-1.0, hi=1.0):
    return max(lo, min(hi, value))


def simulated_annealing_continuous(problem, time_limit,
                                   temp_init=1.0,
                                   refroidissement=0.9999,
                                   sigma_init=0.5):
    best = Solution(problem.d, problem.n)
    best.x = [0] * problem.n
    best.z = [random.uniform(-1, 1) for _ in range(problem.d)]
    problem.eval(best)

    current = Solution(problem.d, problem.n)
    current.x = [0] * problem.n
    current.z = best.z[:]
    current.f = best.f

    temperature = temp_init

    start = time.time()

    while time.time() - start < time_limit:
        # Sigma adaptatif : large au début, fin à la fin
        sigma = sigma_init * temperature / temp_init

        # Voisin : perturbation gaussienne d'une composante
        voisin = Solution(problem.d, problem.n)
        voisin.x = [0] * problem.n
        voisin.z = current.z[:]

        i = random.randint(0, problem.d - 1)
        voisin.z[i] = _clip(voisin.z[i] + random.gauss(0, sigma))

        problem.eval(voisin)

        delta = voisin.f - current.f

        # Acceptation : amélioration certaine ou dégradation probabiliste
        if delta < 0 or random.random() < math.exp(-delta / temperature):
            current = voisin

        # Meilleur global
        if current.f < best.f:
            best = current

        # Refroidissement
        temperature *= refroidissement

    return best