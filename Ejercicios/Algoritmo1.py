

suma = 0
n = 0
while abs(2 - suma) >= 0.1:
    suma += (1/2)**n
    n += 1
print(f"terminos: {n}, Suma: {suma:.6f}, Error: {abs(2-suma):.6f}")






