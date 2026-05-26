#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    Visualisation des résultats par boxplot.

    - Abscisse : instances (0 à 15)
    - Ordonnée : valeur de f (score)
    - Une figure par algorithme + une figure de comparaison globale
"""

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

# ------------------------------------------------------------------ #
#  Chargement                                                         #
# ------------------------------------------------------------------ #

df = pd.read_csv("results_detail.csv")

ALGOS = df["algorithme"].unique()
INSTANCES = sorted(df["instance"].unique())

COLORS = {
    "random_search": "#4C72B0",
    "hill_climbing": "#55A868",
    "simulated_annealing": "#C44E52",
}

LABELS = {
    "random_search": "Random Search",
    "hill_climbing": "Hill Climbing",
    "simulated_annealing": "Simulated Annealing",
}

# ------------------------------------------------------------------ #
#  Figure 1 : une sous-figure par algorithme                         #
# ------------------------------------------------------------------ #

fig, axes = plt.subplots(len(ALGOS), 1, figsize=(16, 4 * len(ALGOS)), sharex=True)
fig.suptitle("Boxplots par algorithme — 16 instances × 30 runs", fontsize=14, fontweight="bold")

for ax, algo in zip(axes, ALGOS):
    data = [
        df[(df["algorithme"] == algo) & (df["instance"] == i)]["f"].values
        for i in INSTANCES
    ]

    bp = ax.boxplot(data, patch_artist=True, positions=INSTANCES,
                    widths=0.6, showfliers=True)

    for patch in bp["boxes"]:
        patch.set_facecolor(COLORS[algo])
        patch.set_alpha(0.7)

    ax.set_title(LABELS[algo], fontsize=11, fontweight="bold")
    ax.set_ylabel("f(z, x)")
    ax.set_xticks(INSTANCES)
    ax.grid(axis="y", linestyle="--", alpha=0.5)

axes[-1].set_xlabel("Instance")
plt.tight_layout()
plt.savefig("boxplot_par_algo.png", dpi=150, bbox_inches="tight")
print("[OK] boxplot_par_algo.png")

# ------------------------------------------------------------------ #
#  Figure 2 : comparaison des 3 algos côte à côte par instance       #
# ------------------------------------------------------------------ #

fig2, ax2 = plt.subplots(figsize=(18, 6))
fig2.suptitle("Comparaison des algorithmes par instance", fontsize=14, fontweight="bold")

n_algos = len(ALGOS)
width = 0.25
offsets = np.linspace(-(n_algos - 1) * width / 2,
                      (n_algos - 1) * width / 2, n_algos)

for offset, algo in zip(offsets, ALGOS):
    data = [
        df[(df["algorithme"] == algo) & (df["instance"] == i)]["f"].values
        for i in INSTANCES
    ]
    positions = [i + offset for i in INSTANCES]

    bp = ax2.boxplot(data, patch_artist=True, positions=positions,
                     widths=width * 0.9, showfliers=False)

    for patch in bp["boxes"]:
        patch.set_facecolor(COLORS[algo])
        patch.set_alpha(0.75)

# Légende
patches = [
    mpatches.Patch(color=COLORS[algo], label=LABELS[algo])
    for algo in ALGOS
]
ax2.legend(handles=patches, loc="lower left", fontsize=10)
ax2.set_xticks(INSTANCES)
ax2.set_xticklabels([f"inst {i}" for i in INSTANCES], rotation=45, ha="right")
ax2.set_xlabel("Instance")
ax2.set_ylabel("f(z, x)")
ax2.grid(axis="y", linestyle="--", alpha=0.5)

plt.tight_layout()
plt.savefig("boxplot_comparaison.png", dpi=150, bbox_inches="tight")
print("[OK] boxplot_comparaison.png")

plt.show()