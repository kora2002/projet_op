
import statistics
from mixQUBO import MixQUBO
from hill_climbing import hill_climbing_binary
from config import TIME_LIMIT, NB_RUNS,INSTANCES_DIR

# ------------------------------------------------------------------ #
#  Test sur l'instance 0 avec 30 runs                                #
# ------------------------------------------------------------------ #

def main():
    problem = MixQUBO()
    problem.read_json(f"{INSTANCES_DIR}/mxqubo_v0_0.json")

    results = []

    for i in range(NB_RUNS):
        best = hill_climbing_binary(problem, TIME_LIMIT)
        results.append(best.f)
        print(f"Run {i+1}/30 : {best.f:.4f}")

    print(f"\nMeilleur   : {min(results):.4f}")
    print(f"Pire       : {max(results):.4f}")
    print(f"Moyenne    : {statistics.mean(results):.4f}")
    print(f"Ecart-type : {statistics.stdev(results):.4f}")

if __name__ == "__main__":
    main()


"""
1. Énorme amélioration
La moyenne passe de -5243(random_search) à -10339(hill climbing) — presque le double ! Le Hill Climbing est bien plus efficace que la recherche aléatoire.
2. Écart-type plus grand
L'écart-type passe de 344 à 674. Cela s'explique car le Hill Climbing peut rester bloqué dans des zones différentes selon le point de départ aléatoire.
3. Problème des optima locaux
Le Hill Climbing ne peut qu'améliorer la solution. Quand aucun bit flip n'améliore f, il est bloqué — c'est la limite principale de cet algorithme.
"""