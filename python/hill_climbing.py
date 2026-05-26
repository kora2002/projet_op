import random
import time
from solution import Solution

# ------------------------------------------------------------------ #
#  Iterated Local Search (ILS) binaire                               #
#                                                                     #
#  Structure :                                                        #
#    1. local_search : HC pur jusqu'à blocage (aucune amélioration    #
#                      après max_no_improve tentatives)               #
#    2. perturbation : flip de k bits pour sortir de l'optimum local  #
#    3. répéter jusqu'à time_limit                                    #
# ------------------------------------------------------------------ #

def local_search(problem, solution, max_no_improve):
    """
    Hill Climbing pur : s'arrête quand aucune amélioration
    n'est trouvée après max_no_improve tentatives consécutives.
    """
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
    """
    Flip k bits distincts aléatoires pour s'échapper de l'optimum local.
    k doit être > 1 (sinon identique à la recherche locale).
    """
    indices = random.sample(range(len(solution.x)), k)
    for i in indices:
        solution.x[i] = 1 - solution.x[i]
    return solution


def ils_binary(problem, time_limit):
    # Paramètres
    max_no_improve = problem.n       # on essaie n fois avant de déclarer blocage
    k = max(2, problem.n // 10)     # on flip 10% des bits lors de la perturbation

    # Solution initiale aléatoire
    current = Solution(problem.d, problem.n)
    current.x = [random.randint(0, 1) for _ in range(problem.n)]
    problem.eval(current)

    # Phase 1 : local search initiale
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

        # Phase 3 : local search depuis le candidat perturbé
        candidat = local_search(problem, candidat, max_no_improve)

        # Critère d'acceptation : on accepte si meilleur (acceptation stricte)
        if candidat.f < current.f:
            current = candidat

        # Mise à jour du meilleur global
        if current.f < best.f:
            best = current

    return best
