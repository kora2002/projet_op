import random
import time
from solution import Solution


def _clip(value, lo=-1.0, hi=1.0):
    return max(lo, min(hi, value))


# ---------------------------------------------------------
# Optimisation continue (best-improvement + backtrack)
# ---------------------------------------------------------
def _hc_continuous_step(problem, current, sigma=0.1):
    best_f = current.f
    best_idx = None
    best_val = None

    indices = list(range(problem.d))
    random.shuffle(indices)

    tmp_neighbor = Solution(problem.d, problem.n)
    tmp_neighbor.x = current.x[:]  # copie explicite — pas de référence partagée
    tmp_neighbor.z = current.z[:]

    for i in indices:
        old_val = tmp_neighbor.z[i]

        # Mutation
        tmp_neighbor.z[i] = _clip(old_val + random.gauss(0, sigma))
        problem.eval(tmp_neighbor)

        if tmp_neighbor.f < best_f:
            best_f   = tmp_neighbor.f
            best_idx = i
            best_val = tmp_neighbor.z[i]

        # Backtrack pour le prochain test
        tmp_neighbor.z[i] = old_val

    # Construction de la solution finale seulement si amélioration
    if best_idx is not None:
        best_neighbor = Solution(problem.d, problem.n)
        best_neighbor.x = current.x[:]
        best_neighbor.z = current.z[:]
        best_neighbor.z[best_idx] = best_val
        best_neighbor.f = best_f
        return best_neighbor, True

    return current, False


# ---------------------------------------------------------
# Optimisation binaire (best-improvement + backtrack)
# ---------------------------------------------------------
def _hc_binary_step(problem, current):
    best_f   = current.f
    best_idx = None

    indices = list(range(problem.n))
    random.shuffle(indices)

    tmp_neighbor = Solution(problem.d, problem.n)
    tmp_neighbor.z = current.z[:]  # copie explicite — pas de référence partagée
    tmp_neighbor.x = current.x[:]

    for i in indices:
        # Flip
        tmp_neighbor.x[i] = 1 - tmp_neighbor.x[i]
        problem.eval(tmp_neighbor)

        if tmp_neighbor.f < best_f:
            best_f   = tmp_neighbor.f
            best_idx = i

        # Backtrack
        tmp_neighbor.x[i] = 1 - tmp_neighbor.x[i]

    # Construction de la solution finale seulement si amélioration
    if best_idx is not None:
        best_neighbor = Solution(problem.d, problem.n)
        best_neighbor.z = current.z[:]
        best_neighbor.x = current.x[:]
        best_neighbor.x[best_idx] = 1 - best_neighbor.x[best_idx]
        best_neighbor.f = best_f
        return best_neighbor, True

    return current, False


# ---------------------------------------------------------
# Algorithme principal
# ---------------------------------------------------------
def hill_climbing_mixed(problem, time_limit, sigma=0.1):
    """
    Hill Climbing mixte par alternance (coordinate descent).

    Critères d'arrêt :
        1. Optimum local strict : aucune amélioration dans z ET x
        2. Temps limite (sécurité)
    """
    # Solution initiale aléatoire mixte
    current = Solution(problem.d, problem.n)
    current.z = [random.uniform(-1, 1) for _ in range(problem.d)]
    current.x = [random.randint(0, 1)  for _ in range(problem.n)]
    problem.eval(current)

    # Copie explicite du meilleur
    best = Solution(problem.d, problem.n)
    best.z = current.z[:]
    best.x = current.x[:]
    best.f = current.f

    start = time.time()

    while time.time() - start < time_limit:

        # Étape 1 : optimisation continue (x fixé)
        current, improved_z = _hc_continuous_step(problem, current, sigma)

        if time.time() - start >= time_limit:
            break

        # Étape 2 : optimisation binaire (z fixé)
        current, improved_x = _hc_binary_step(problem, current)

        # Mise à jour du meilleur global
        if current.f < best.f:
            best = Solution(problem.d, problem.n)
            best.z = current.z[:]
            best.x = current.x[:]
            best.f = current.f

        # Critère d'arrêt : optimum local strict sur les deux espaces
        if not improved_z and not improved_x:
            break

    return best