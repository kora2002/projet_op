import math

temperature = 100.0
delta = 50.0  # la nouvelle solution est 50 points moins bonne

P = math.exp(-delta / temperature)
print(f"Probabilité d'accepter : {P:.4f}")

temperature = 1.0  # temperature basse
P = math.exp(-delta / temperature)
print(f"Probabilité d'accepter : {P:.4f}")