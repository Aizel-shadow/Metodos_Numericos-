import matplotlib.pyplot as plt

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

# Generar datos
n_values = list(range(0, 21))
fib_values = [fibonacci(n) for n in n_values]

# Gráfica
plt.figure(figsize=(8, 6))
plt.plot(n_values, fib_values, marker='o', linewidth=2, markersize=6, color='steelblue')
plt.xlabel('n', fontsize=12)
plt.ylabel('fib(n)', fontsize=12)
plt.title('Serie de Fibonacci', fontsize=14, fontweight='bold')
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()