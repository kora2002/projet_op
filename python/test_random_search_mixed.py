import statistics
from mixQUBO import MixQUBO
from random_search_mixed import random_search_mixed
from config import TIME_LIMIT, NB_RUNS, INSTANCES_DIR


def main():
    problem = MixQUBO()
    problem.read_json(f"{INSTANCES_DIR}/mxqubo_v0_0.json")

    results = []
    print("--- Test : Random Search Mixed (Instance 0) ---")
    for i in range(NB_RUNS):
        best = random_search_mixed(problem, TIME_LIMIT)
        results.append(best.f)
        print(f"Run {i + 1:02d}/{NB_RUNS} : f = {best.f:.4f}")

    print("\n[Statistiques Random Search Mixed]")
    print(f"Meilleur   : {min(results):.4f}")
    print(f"Pire       : {max(results):.4f}")
    print(f"Moyenne    : {statistics.mean(results):.4f}")
    print(f"Ecart-type : {statistics.stdev(results):.4f}")


if __name__ == "__main__":
    main()