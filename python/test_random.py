#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import mixQUBO as mxq
import statistics
from datetime import datetime
from random_search import random_search_binary

def main():
    f = mxq.MixQUBO()
    f.read_json("../instances/mxqubo_v0_0.json")


    time_limit = 7.0

    results = []

    with open("results_random_binary.csv", "a") as file:
        file.write(f"\n=== Lancement : {datetime.now()} ===\n")
        file.write("id f z x\n")

        for i in range(30):
            best = random_search_binary(f, time_limit)
            results.append(best.f)
            print(f"Run {i+1}: {best.f:.6f}")
            # utilise le __str__ du prof directement
            file.write(f"{i} {str(best)}\n")

        # Statistiques
        stats = (
            f"\nMin       : {min(results):.6f}\n"
            f"Max       : {max(results):.6f}\n"
            f"Moyenne   : {statistics.mean(results):.6f}\n"
            f"Écart-type: {statistics.stdev(results):.6f}\n"
            f"Médiane   : {statistics.median(results):.6f}\n"
        )
        print("\n--- Statistiques ---")
        print(stats)
        file.write(stats)

if __name__ == "__main__":
    main()
