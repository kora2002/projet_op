# ------------------------------------------------------------------ #
#  Configuration globale du projet                                    #
# ------------------------------------------------------------------ #

# Temps d'execution du code etalon sur notre machine (en secondes)
TEMPS_ETALON = 26.966

# Ratio par rapport a la machine etalon (10 secondes)
RATIO = TEMPS_ETALON / 10.0

# Temps limite equivalent a 15 secondes sur la machine etalon
TIME_LIMIT = 15 * RATIO

# Nombre de runs pour les algorithmes stochastiques
NB_RUNS = 30

# Nombre d'instances
NB_INSTANCES = 16

# Repertoire des instances
INSTANCES_DIR = "../instances"

