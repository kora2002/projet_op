"""
    Test du Hill Climbing continu
    Instance 0 — x = 0...0 fixé, optimisation de z dans [-1, 1]^d

    Critères d'arrêt :
        1. Stagnation : aucune amélioration sur 2*d cycles consécutifs
        2. Temps limite : sécurité supplémentaire
"""

import statistics
from mixQUBO import MixQUBO
from hill_climbing_continuous import hill_climbing_continuous
from config import TIME_LIMIT, NB_RUNS, INSTANCES_DIR


def main():
    problem = MixQUBO()
    problem.read_json(f"{INSTANCES_DIR}/mxqubo_v0_0.json")

    print(f"Dimension continue : d = {problem.d}")
    print(f"Dimension binaire  : n = {problem.n}")
    print(f"max_no_improve     : {2 * problem.d} cycles")
    print(f"Temps limite       : {TIME_LIMIT}s")
    print(f"Nombre de runs     : {NB_RUNS}")
    print("-" * 40)

    results = []

    for i in range(NB_RUNS):
        best = hill_climbing_continuous(problem, TIME_LIMIT)
        results.append(best.f)
        print(f"Run {i+1:02d}/{NB_RUNS} : {best.f:.4f}")

    print(f"\nMeilleur   : {min(results):.4f}")
    print(f"Pire       : {max(results):.4f}")
    print(f"Moyenne    : {statistics.mean(results):.4f}")
    print(f"Ecart-type : {statistics.stdev(results):.4f}")
    print(f"Mediane    : {statistics.median(results):.4f}")

    """
    Commentaires attendus :
    - Le Hill Climbing améliore nettement la recherche aléatoire grâce à
      l'exploitation du voisinage gaussien.
    - Le critère de stagnation (2*d cycles sans amélioration) détecte
      précisément les optima locaux et évite de tourner inutilement.
    - L'écart-type peut être élevé : selon le point de départ aléatoire,
      le HC converge vers des optima locaux de qualité très variable.
    - Ces résultats serviront de référence intermédiaire entre la
      recherche aléatoire (baseline) et le Simulated Annealing.
    """


if __name__ == "__main__":
    main()