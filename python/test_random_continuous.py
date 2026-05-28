import statistics
from mixQUBO import MixQUBO
from random_search_continuous import random_search_continuous
from config import TIME_LIMIT, NB_RUNS, INSTANCES_DIR


def main():
    problem = MixQUBO()
    problem.read_json(f"{INSTANCES_DIR}/mxqubo_v0_0.json")

    results = []

    for i in range(NB_RUNS):
        best = random_search_continuous(problem, TIME_LIMIT)
        results.append(best.f)
        print(f"Run {i+1:02d}/{NB_RUNS} : {best.f:.4f}")

    print(f"\nMeilleur   : {min(results):.4f}")
    print(f"Pire       : {max(results):.4f}")
    print(f"Moyenne    : {statistics.mean(results):.4f}")
    print(f"Ecart-type : {statistics.stdev(results):.4f}")
    print(f"Mediane    : {statistics.median(results):.4f}")


if __name__ == "__main__":
    main()