import math
import random
import time
from solution import Solution


def _clip(value, lo=-1.0, hi=1.0):
    return max(lo, min(hi, value))


def sa_mixed(problem, time_limit,
             temp_init=100.0,
             temp_min=0.001,
             sigma_init=0.5):


    best = Solution(problem.d, problem.n)
    best.z = [random.uniform(-1, 1) for _ in range(problem.d)]
    best.x = [random.randint(0, 1)  for _ in range(problem.n)]
    problem.eval(best)

    current = Solution(problem.d, problem.n)
    current.z = best.z[:]
    current.x = best.x[:]
    current.f  = best.f

    # Un seul objet voisin pour toute la durée (optimisation mémoire)
    voisin = Solution(problem.d, problem.n)
    voisin.z = current.z[:]
    voisin.x = current.x[:]

    start   = time.time()
    elapsed = 0.0

    while elapsed < time_limit:


        progress    = elapsed / time_limit
        temperature = temp_init * ((temp_min / temp_init) ** progress)
        sigma       = sigma_init * (temperature / temp_init)


        if random.random() < 0.5 and problem.d > 0:

            # Mutation continue : une composante de z
            i      = random.randint(0, problem.d - 1)
            old_z  = voisin.z[i]
            voisin.z[i] = _clip(old_z + random.gauss(0, sigma))
            problem.eval(voisin)

            delta = voisin.f - current.f
            if delta < 0 or random.random() < math.exp(-delta / temperature):
                current.z[i] = voisin.z[i]
                current.f    = voisin.f
            else:
                voisin.z[i] = old_z

        else:


            i = random.randint(0, problem.n - 1)
            voisin.x[i] = 1 - voisin.x[i]
            problem.eval(voisin)

            delta = voisin.f - current.f
            if delta < 0 or random.random() < math.exp(-delta / temperature):
                current.x[i] = voisin.x[i]
                current.f    = voisin.f
            else:
                voisin.x[i] = 1 - voisin.x[i]  # backtrack


        if current.f < best.f:
            best = Solution(problem.d, problem.n)
            best.z = current.z[:]
            best.x = current.x[:]
            best.f = current.f

        elapsed = time.time() - start

    return best