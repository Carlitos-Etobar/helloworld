import pickle

# Vulnerabilidad 1: Uso de assert
assert 1 == 1  # Bandit debería detectar esto como B101
