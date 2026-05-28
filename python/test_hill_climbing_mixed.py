
"""
    Test du Hill Climbing mixte par alternance
    Instance 0 — optimisation mixte : z dans [-1, 1]^d et x dans {0, 1}^n
"""

import statistics
from mixQUBO import MixQUBO
from hill_climbing_mixed import hill_climbing_mixed
from config import TIME_LIMIT, NB_RUNS, INSTANCES_DIR


def main():
    problem = MixQUBO()
    problem.read_json(f"{INSTANCES_DIR}/mxqubo_v0_0.json")

    print(f"Dimension continue : d = {problem.d}")
    print(f"Dimension binaire  : n = {problem.n}")
    print(f"Temps limite       : {TIME_LIMIT:.3f}s")
    print(f"Nombre de runs     : {NB_RUNS}")
    print("-" * 40)

    results = []

    for i in range(NB_RUNS):
        best = hill_climbing_mixed(problem, TIME_LIMIT)
        results.append(best.f)
        print(f"Run {i+1:02d}/{NB_RUNS} : {best.f:.4f}")

    print(f"\nMeilleur   : {min(results):.4f}")
    print(f"Pire       : {max(results):.4f}")
    print(f"Moyenne    : {statistics.mean(results):.4f}")
    print(f"Ecart-type : {statistics.stdev(results):.4f}")
    print(f"Mediane    : {statistics.median(results):.4f}")

    """
    Commentaires attendus :
    - Le HC mixte par alternance exploite les deux espaces successivement.
    - Grâce au best-improvement, chaque cycle retient le meilleur voisin
      parmi tous les voisins testés dans z et x.
    - Critère d'arrêt : optimum local strict atteint quand aucune
      amélioration n'est possible ni dans z ni dans x.
    - Attendu meilleur que les HC continu et binaire seuls
      grâce à la synergie entre les deux espaces.
    """


if __name__ == "__main__":
    main()