#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    Génération des résultats CSV — partie mixte (multiprocessing).

    z dans [-1, 1]^d et x dans {0, 1}^n optimisés simultanément.

    Colonnes results_summary_mixed.csv : algorithme, instance, min, max, moyenne, ecart_type, mediane
    Colonnes results_detail_mixed.csv  : algorithme, instance, run, f
"""

import csv
import statistics
import multiprocessing as mp

from mixQUBO import MixQUBO
from random_search_mixed import random_search_mixed
from hill_climbing_mixed import hill_climbing_mixed
from sa_mixed import sa_mixed
from config import TIME_LIMIT, NB_RUNS, NB_INSTANCES, INSTANCES_DIR

# ------------------------------------------------------------------ #
#  Configuration                                                      #
# ------------------------------------------------------------------ #

ALGORITHMES = {
    "random_search_mixed" : random_search_mixed,
    "hill_climbing_mixed" : hill_climbing_mixed,
    "sa_mixed"            : sa_mixed,
}

OUTPUT_SUMMARY = "results_summary_mixed.csv"
OUTPUT_DETAIL  = "results_detail_mixed.csv"

# ------------------------------------------------------------------ #
#  Tâche unitaire (1 algo x 1 instance x NB_RUNS runs)               #
# ------------------------------------------------------------------ #

def run_task(args):
    algo_name, instance_id = args

    instance_file = f"{INSTANCES_DIR}/mxqubo_v0_{instance_id}.json"
    problem = MixQUBO()
    problem.read_json(instance_file)

    algo_fn = ALGORITHMES[algo_name]
    results = []

    for run in range(NB_RUNS):
        best = algo_fn(problem, TIME_LIMIT)
        results.append((run, best.f))

    print(f"[OK] {algo_name:22s} | instance {instance_id:02d} "
          f"| moy={statistics.mean(r for _, r in results):.2f}", flush=True)

    return algo_name, instance_id, results

# ------------------------------------------------------------------ #
#  Main                                                               #
# ------------------------------------------------------------------ #

def main():
    tasks = [
        (algo_name, instance_id)
        for algo_name in ALGORITHMES
        for instance_id in range(NB_INSTANCES)
    ]

    nb_cores = mp.cpu_count()
    print(f"Lancement de {len(tasks)} taches sur {nb_cores} coeur(s)...")
    print(f"Optimisation mixte : z dans [-1,1]^d et x dans {{0,1}}^n\n")

    with mp.Pool(processes=nb_cores) as pool:
        all_results = pool.map(run_task, tasks)

    summary_rows = []
    detail_rows  = []

    for algo_name, instance_id, runs in all_results:
        fs = [f for _, f in runs]

        summary_rows.append({
            "algorithme" : algo_name,
            "instance"   : instance_id,
            "min"        : round(min(fs), 6),
            "max"        : round(max(fs), 6),
            "moyenne"    : round(statistics.mean(fs), 6),
            "ecart_type" : round(statistics.stdev(fs), 6),
            "mediane"    : round(statistics.median(fs), 6),
        })

        for run, f in runs:
            detail_rows.append({
                "algorithme" : algo_name,
                "instance"   : instance_id,
                "run"        : run,
                "f"          : round(f, 6),
            })

    summary_rows.sort(key=lambda r: (r["algorithme"], r["instance"]))
    detail_rows.sort(key=lambda r:  (r["algorithme"], r["instance"], r["run"]))

    with open(OUTPUT_SUMMARY, "w", newline="") as f:
        writer = csv.DictWriter(
            f, fieldnames=["algorithme", "instance", "min", "max",
                           "moyenne", "ecart_type", "mediane"])
        writer.writeheader()
        writer.writerows(summary_rows)

    with open(OUTPUT_DETAIL, "w", newline="") as f:
        writer = csv.DictWriter(
            f, fieldnames=["algorithme", "instance", "run", "f"])
        writer.writeheader()
        writer.writerows(detail_rows)

    print(f"\n[OK] {OUTPUT_SUMMARY}")
    print(f"[OK] {OUTPUT_DETAIL}")


if __name__ == "__main__":
    main()