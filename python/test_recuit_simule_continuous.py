import statistics
from mixQUBO import MixQUBO
from recuit_simule_continuous import simulated_annealing_continuous
from config import TIME_LIMIT, NB_RUNS, INSTANCES_DIR


def main():
    problem = MixQUBO()
    problem.read_json(f"{INSTANCES_DIR}/mxqubo_v0_0.json")

    print(f"Dimension continue : d = {problem.d}")
    print(f"Dimension binaire  : n = {problem.n}")
    print(f"Temps limite       : {TIME_LIMIT}s")
    print(f"Nombre de runs     : {NB_RUNS}")
    print("-" * 40)

    results = []

    for i in range(NB_RUNS):
        best = simulated_annealing_continuous(problem, TIME_LIMIT)
        results.append(best.f)
        print(f"Run {i+1:02d}/{NB_RUNS} : {best.f:.4f}")

    print(f"\nMeilleur   : {min(results):.4f}")
    print(f"Pire       : {max(results):.4f}")
    print(f"Moyenne    : {statistics.mean(results):.4f}")
    print(f"Ecart-type : {statistics.stdev(results):.4f}")
    print(f"Mediane    : {statistics.median(results):.4f}")

    """
    Commentaires attendus :
    - Le SA dépasse le Hill Climbing grâce à sa capacité à s'échapper
      des optima locaux en acceptant parfois des solutions moins bonnes.
    - Le sigma adaptatif (proportionnel à T) permet une exploration large
      au début puis une exploitation fine en fin de recherche.
    - L'écart-type devrait être plus faible que le HC : le SA évite
      les mauvais bassins comme -4140 observés en Hill Climbing.
    - Progression attendue :
        Random Search  → -4845  (baseline)
        Hill Climbing  → -5375  (+11% vs RS)
        Simulated Ann. → ???    (mieux que HC)
    """


if __name__ == "__main__":
    main()