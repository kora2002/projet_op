#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    Boîtes à moustaches par instance — partie mixte
    Lecture de results_detail_mixed.csv
    Un graphique par instance (16 instances) en grille 4x4
"""

import csv
import matplotlib.pyplot as plt
from collections import defaultdict

# ------------------------------------------------------------------ #
#  Lecture du CSV                                                     #
# ------------------------------------------------------------------ #

data = defaultdict(lambda: defaultdict(list))

with open("results_detail_mixed.csv", newline="") as f:
    reader = csv.DictReader(f)
    for row in reader:
        data[int(row["instance"])][row["algorithme"]].append(float(row["f"]))

# Ordre et labels
ordre    = ["random_search_mixed", "hill_climbing_mixed", "sa_mixed"]
labels   = ["Random\nSearch", "Hill\nClimbing", "SA\nMixte"]
couleurs = ["#4C72B0", "#DD8452", "#55A868"]

# ------------------------------------------------------------------ #
#  Grille 4x4 — un subplot par instance                              #
# ------------------------------------------------------------------ #

fig, axes = plt.subplots(4, 4, figsize=(18, 14))
fig.suptitle("Comparaison des algorithmes par instance — Optimisation mixte",
             fontsize=15, fontweight="bold", y=1.01)

for instance_id, ax in enumerate(axes.flat):
    valeurs = [data[instance_id][algo] for algo in ordre]

    bp = ax.boxplot(valeurs, labels=labels, patch_artist=True, notch=False)

    for patch, couleur in zip(bp["boxes"], couleurs):
        patch.set_facecolor(couleur)
        patch.set_alpha(0.7)

    ax.set_title(f"Instance {instance_id:02d}", fontsize=10, fontweight="bold")
    ax.set_ylabel("f", fontsize=9)
    ax.grid(axis="y", linestyle="--", alpha=0.4)
    ax.tick_params(axis="x", labelsize=8)

plt.tight_layout()
plt.savefig("boxplot_mixed_par_instance.png", dpi=150, bbox_inches="tight")
plt.show()
print("[OK] boxplot_mixed_par_instance.png")