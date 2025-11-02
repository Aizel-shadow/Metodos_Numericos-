import matplotlib.pyplot as plt
import math

def fibonacci(n):
    if n == 0:
        return 0
    x = 0
    y = 1
    for i in range(1, n):
        z = x + y
        x = y
        y = z
    return y

# Generar datos del cociente
n_values = list(range(2, 21))
ratio_values = [fibonacci(n) / fibonacci(n-1) for n in n_values]

# Número áureo
phi = (1 + math.sqrt(5)) / 2

# Imprimir tabla
print("| n  | fib(n)/fib(n-1) |")
print("|----|-----------------|")
for n in range(2, 12):
    ratio = fibonacci(n) / fibonacci(n-1)
    print(f"| {n:<2} | {ratio:.6f}      |")

# Gráfica
plt.figure(figsize=(8, 6))
plt.plot(n_values, ratio_values, marker='o', linewidth=2, markersize=6, 
         color='orange', label='fib(n)/fib(n-1)')
plt.axhline(y=phi, color='red', linestyle='--', linewidth=2, 
            label=f'Número áureo φ')
plt.xlabel('n', fontsize=12)
plt.ylabel('Cociente', fontsize=12)
plt.title('Aproximación al numero aureo (φ)', fontsize=14, fontweight='bold')
plt.legend()
plt.grid(True, alpha=0.3)
plt.ylim(1.3, 2.1)
plt.tight_layout()
plt.show()