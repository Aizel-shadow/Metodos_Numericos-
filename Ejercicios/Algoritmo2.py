import random

def bubble_sort(a):
    n = len(a)
    for i in range(n):
        swapped = False
        for j in range(1, n - i):
            if a[j] < a[j-1]:
                a[j], a[j-1] = a[j-1], a[j]
                swapped = True
        if not swapped:
            break

# Caso 1
v1 = [3, 2, 5, 8, 4, 1]
print("Caso 1:", v1)
bubble_sort(v1)
print("Ordenado:", v1)

# Caso 2
v2 = [-1, 0, 4, 5, 6, 7]
print("\nCaso 2:", v2)
bubble_sort(v2)
print("Ordenado:", v2)

# Caso 3 (reducido a 1000 elementos para que sea rápido)
v3 = [random.randint(-200, 145) for _ in range(1000)]
print("\nCaso 3: 1,000 num aleatorios")
print("Primeros 10:", v3[:10])
bubble_sort(v3)
print("Ordenados:", v3[:10])
print("Completado")