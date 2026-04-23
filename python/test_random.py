#!/usr/bin/env python3
# -*- coding: utf-8 -*-

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

"""
1. Grande variabilité
L'écart entre le meilleur (-6034) et le pire (-4424) est de 1610 points. L'écart-type de 344 confirme que les résultats sont très instables d'un run à l'autre.
2. Dépendance au hasard
Certains runs donnent de bons résultats (run 17 : -6034) et d'autres sont médiocres (run 22 : -4424). L'algorithme n'apprend rien entre les runs.
3. Aucune exploitation
La recherche aléatoire explore l'espace sans mémoire ni direction. Elle ne tire pas profit des bonnes solutions trouvées pour en chercher de meilleures dans leur voisinage.
4. Sert de baseline
La moyenne de -5243 sera notre référence. Tout algorithme plus intelligent devra faire mieux que cette valeur.
"""