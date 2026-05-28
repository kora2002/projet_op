from mixQUBO import MixQUBO
import statistics
from datetime import datetime
from random_search import random_search_binary
from config import TIME_LIMIT,NB_RUNS

def main():
    problem = MixQUBO()
    problem.read_json("../instances/mxqubo_v0_0.json")

    results = []

    for i in range(NB_RUNS):
        best = random_search_binary(problem, TIME_LIMIT)
        results.append(best.f)
        print(f"Run {i + 1}/30 : {best.f:.4f}")

    print(f"\nMeilleur   : {min(results):.4f}")
    print(f"Pire       : {max(results):.4f}")
    print(f"Moyenne    : {statistics.mean(results):.4f}")
    print(f"Ecart-type : {statistics.stdev(results):.4f}")


if __name__ == "__main__":
    main()
