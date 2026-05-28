import random
import time
from solution import Solution


def local_search(problem, solution, max_no_improve):
    no_improve = 0

    while no_improve < max_no_improve:
        voisin = Solution(problem.d, problem.n)
        voisin.x = solution.x[:]

        i = random.randint(0, problem.n - 1)
        voisin.x[i] = 1 - voisin.x[i]
        problem.eval(voisin)

        if voisin.f < solution.f:
            solution = voisin
            no_improve = 0
        else:
            no_improve += 1

    return solution


def perturbation(solution, k):
    indices = random.sample(range(len(solution.x)), k)
    for i in indices:
        solution.x[i] = 1 - solution.x[i]
    return solution


def ils_binary(problem, time_limit):
    max_no_improve = problem.n
    k = max(2, problem.n // 10)

    current = Solution(problem.d, problem.n)
    current.x = [random.randint(0, 1) for _ in range(problem.n)]
    problem.eval(current)

    current = local_search(problem, current, max_no_improve)
    best = current

    start = time.time()
    while time.time() - start < time_limit:
        # Phase 2 : perturbation
        candidat = Solution(problem.d, problem.n)
        candidat.x = current.x[:]
        candidat.f = current.f
        candidat = perturbation(candidat, k)
        problem.eval(candidat)

        candidat = local_search(problem, candidat, max_no_improve)

        if candidat.f < current.f:
            current = candidat

        if current.f < best.f:
            best = current

    return best
