import statistics
from mixQUBO import MixQUBO
from sa_algorithm import simulated_annealing_binary
from config import TIME_LIMIT, NB_RUNS,INSTANCES_DIR

def main():
    problem = MixQUBO()
    problem.read_json(f"{INSTANCES_DIR}/mxqubo_v0_0.json")

    results = []
    for i in range(NB_RUNS):
        best = simulated_annealing_binary(problem,TIME_LIMIT)
        results.append(best.f)
        print(f"Run {i+1}/{NB_RUNS}: {best.f:4f}")

    print(f"\nMeilleur   : {min(results):.4f}")
    print(f"Pire       : {max(results):.4f}")
    print(f"Moyenne    : {statistics.mean(results):.4f}")
    print(f"Ecart-type : {statistics.stdev(results):.4f}")


if __name__ == "__main__":
    main()


"""
1. SA est le meilleur sur tous les indicateurs
La moyenne passe de -10339 (HC) à -12561 (SA) — soit +2222 points de gain.
2. SA est plus stable que HC
L'écart-type diminue de 674 à 331 — le SA donne des résultats plus réguliers grâce à sa capacité à s'échapper des optima locaux.
3. Progression claire
Random Search → -5243  (baseline)
Hill Climbing → -10339 (+97% vs RS)
Simulated Annealing → -12561 (+140% vs RS)
"""