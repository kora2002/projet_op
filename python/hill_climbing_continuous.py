"""
    Hill Climbing continu pour mixQUBO
    x est fixé au vecteur nul, on optimise z dans [-1, 1]^d

    - First improvement : on accepte le premier voisin améliorant
    - Stagnation : arrêt si aucune amélioration sur 2*d cycles consécutifs
    - Temps limite : sécurité supplémentaire
"""

import random
import time
from solution import Solution


def _clip(value, lo=-1.0, hi=1.0):
    """Restreint value dans [lo, hi]."""
    return max(lo, min(hi, value))


def hill_climbing_continuous(problem, time_limit, sigma=0.1):
    """
    Hill Climbing continu (first improvement + stagnation control)
    x fixé à 0, optimisation de z dans [-1, 1]^d

    Critères d'arrêt :
        1. Stagnation : aucune amélioration sur 2*d cycles consécutifs
           → optimum local atteint
        2. Temps limite : sécurité si d est très grand
    """
    # Solution initiale
    current = Solution(problem.d, problem.n)
    current.x = [0] * problem.n
    current.z = [random.uniform(-1, 1) for _ in range(problem.d)]
    problem.eval(current)

    # Copie explicite pour éviter le bug de référence
    best = Solution(problem.d, problem.n)
    best.x = current.x[:]
    best.z = current.z[:]
    best.f = current.f

    # Contrôle de stagnation adapté à la dimension
    no_improve_count = 0
    max_no_improve = 2 * problem.d

    start = time.time()

    while time.time() - start < time_limit:

        # Un cycle complet sur toutes les composantes (sans remise)
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

            # First improvement : on accepte dès que c'est mieux
            if neighbor.f < current.f:
                current = neighbor

                # Mise à jour du meilleur global (copie explicite)
                if current.f < best.f:
                    best = Solution(problem.d, problem.n)
                    best.x = current.x[:]
                    best.z = current.z[:]
                    best.f = current.f

                improved = True
                break

        # Gestion stagnation
        if improved:
            no_improve_count = 0
        else:
            no_improve_count += 1

        # Critère d'arrêt : optimum local atteint
        if no_improve_count >= max_no_improve:
            break

    return best