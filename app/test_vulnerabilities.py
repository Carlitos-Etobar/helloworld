import pickle

# Vulnerabilidad 1: Uso de assert
assert 1 == 1  # Bandit debería detectar esto como B101

# Vulnerabilidad 2: Uso de eval
eval("print('Esto es inseguro')")  # Bandit debería detectar esto como B102

# Vulnerabilidad 3: Uso de exec
exec("print('Esto también es inseguro')")  # Bandit debería