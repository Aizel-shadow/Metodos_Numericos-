def iterative(n):
    if n == 0:
        return 0
    else:
        x = 0
        y = 1
        for i in range(1, n):
            z = x + y
            x = y
            y = z
        return y

# Tabla de Fibonacci
print("Tabla Fibonacci:")
print("| n  | fib(n) |")
print("|----|--------|")
for n in range(9):
    print(f"| {n}  | {iterative(n)} |")

# Casos solicitados
print("\nCasos solicitados:")
print(f"n = 11:   {iterative(11)}")
print(f"n = 84:   {iterative(84)}")
print(f"n = 1531: {iterative(1531)}")