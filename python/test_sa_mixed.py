import statistics
from mixQUBO import MixQUBO
from sa_mixed import sa_mixed
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
        best = sa_mixed(problem, TIME_LIMIT)
        results.append(best.f)
        print(f"Run {i+1:02d}/{NB_RUNS} : {best.f:.4f}")

    print(f"\nMeilleur   : {min(results):.4f}")
    print(f"Pire       : {max(results):.4f}")
    print(f"Moyenne    : {statistics.mean(results):.4f}")
    print(f"Ecart-type : {statistics.stdev(results):.4f}")
    print(f"Mediane    : {statistics.median(results):.4f}")

    """
    Commentaires attendus :
    - Le SA mixte est attendu comme le meilleur algorithme du projet.
    - Le refroidissement basé sur le temps réel garantit une exploration
      large au début et une exploitation fine en fin de recherche.
    - L'acceptation probabiliste permet de s'échapper des optima locaux
      contrairement au Hill Climbing mixte.
    - Progression attendue :
        Random Search mixte  → baseline
        Hill Climbing mixte  → amélioration significative
        SA mixte             → meilleur sur moyenne et stabilité
    """


if __name__ == "__main__":
    main()