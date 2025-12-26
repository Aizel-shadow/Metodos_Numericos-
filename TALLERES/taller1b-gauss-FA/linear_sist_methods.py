# -*- coding: utf-8 -*-
"""
Python 3
Versión corregida con contadores de operaciones
@author: z_tjona (modificado)
"""

import logging
from sys import stdout
from datetime import datetime
import numpy as np

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s][%(levelname)s] %(message)s",
    stream=stdout,
    datefmt="%m-%d %H:%M:%S",
)


# ####################################################################
class ContadorOperaciones:
    """Clase para contar operaciones aritméticas"""
    def __init__(self):
        self.sumas_restas = 0
        self.mult_div = 0
        self.intercambios = 0
    
    def reset(self):
        self.sumas_restas = 0
        self.mult_div = 0
        self.intercambios = 0
    
    def __str__(self):
        return (f"Sumas/Restas: {self.sumas_restas}\n"
                f"Mult/Div: {self.mult_div}\n"
                f"Intercambios de filas: {self.intercambios}")


# ####################################################################
def eliminacion_gaussiana(
    A: np.ndarray | list[list[float | int]], 
    contar_ops: bool = False
) -> tuple[np.ndarray, ContadorOperaciones] | np.ndarray:
    """Resuelve un sistema de ecuaciones lineales mediante eliminación gaussiana.

    ## Parameters
    ``A``: matriz aumentada del sistema de ecuaciones lineales. 
           Debe ser de tamaño n-by-(n+1), donde n es el número de incógnitas.
    ``contar_ops``: si True, retorna también un contador de operaciones.

    ## Return
    ``solucion``: vector con la solución del sistema de ecuaciones lineales.
    ``contador``: (opcional) objeto ContadorOperaciones con el conteo de operaciones.
    """
    contador = ContadorOperaciones()
    
    if not isinstance(A, np.ndarray):
        logging.debug("Convirtiendo A a numpy array.")
        A = np.array(A, dtype=float)
    else:
        A = A.astype(float).copy()
    
    assert A.shape[0] == A.shape[1] - 1, "La matriz A debe ser de tamaño n-by-(n+1)."
    n = A.shape[0]

    # Fase de eliminación
    for i in range(0, n - 1):  # loop por columna

        # --- encontrar pivote
        p = None
        for pi in range(i, n):
            if A[pi, i] == 0:
                continue

            if p is None:
                p = pi
                continue

            if abs(A[pi, i]) < abs(A[p, i]):
                p = pi

        if p is None:
            raise ValueError("No existe solución única.")

        if p != i:
            # swap rows
            logging.debug(f"Intercambiando filas {i} y {p}")
            _aux = A[i, :].copy()
            A[i, :] = A[p, :].copy()
            A[p, :] = _aux
            contador.intercambios += 1

        # --- Eliminación: loop por fila
        for j in range(i + 1, n):
            m = A[j, i] / A[i, i]
            contador.mult_div += 1  # división para calcular m
            
            # A[j, i:] = A[j, i:] - m * A[i, i:]
            # Desglosando las operaciones:
            for k in range(i, n + 1):
                # m * A[i, k]: 1 multiplicación
                # A[j, k] - (m * A[i, k]): 1 resta
                contador.mult_div += 1
                contador.sumas_restas += 1
                A[j, k] = A[j, k] - m * A[i, k]

        logging.debug(f"Después de eliminar columna {i}:\n{A}")

    # BUG CORREGIDO: Removido el print inalcanzable después del raise
    if A[n - 1, n - 1] == 0:
        raise ValueError("No existe solución única.")

    # --- Sustitución hacia atrás
    solucion = np.zeros(n)
    solucion[n - 1] = A[n - 1, n] / A[n - 1, n - 1]
    contador.mult_div += 1  # 1 división

    for i in range(n - 2, -1, -1):
        suma = 0
        for j in range(i + 1, n):
            suma += A[i, j] * solucion[j]
            contador.mult_div += 1      # 1 multiplicación
            contador.sumas_restas += 1  # 1 suma
        
        solucion[i] = (A[i, n] - suma) / A[i, i]
        contador.sumas_restas += 1  # 1 resta
        contador.mult_div += 1      # 1 división

    if contar_ops:
        return solucion, contador
    return solucion


# ####################################################################
def descomposicion_LU(
    A: np.ndarray,
    contar_ops: bool = False
) -> tuple[np.ndarray, np.ndarray, ContadorOperaciones] | tuple[np.ndarray, np.ndarray]:
    """Realiza la descomposición LU de una matriz cuadrada A.
    [IMPORTANTE] No se realiza pivoteo.

    ## Parameters
    ``A``: matriz cuadrada de tamaño n-by-n.
    ``contar_ops``: si True, retorna también un contador de operaciones.

    ## Return
    ``L``: matriz triangular inferior.
    ``U``: matriz triangular superior.
    ``contador``: (opcional) objeto ContadorOperaciones con el conteo de operaciones.
    """
    contador = ContadorOperaciones()
    
    A = np.array(A, dtype=float).copy()
    assert A.shape[0] == A.shape[1], "La matriz A debe ser cuadrada."
    n = A.shape[0]

    L = np.zeros((n, n), dtype=float)

    for i in range(0, n):  # loop por columna

        if A[i, i] == 0:
            raise ValueError("No existe solución única (pivote cero, se requiere pivoteo).")

        L[i, i] = 1
        for j in range(i + 1, n):
            m = A[j, i] / A[i, i]
            contador.mult_div += 1  # 1 división
            
            # A[j, i:] = A[j, i:] - m * A[i, i:]
            for k in range(i, n):
                contador.mult_div += 1      # 1 multiplicación
                contador.sumas_restas += 1  # 1 resta
                A[j, k] = A[j, k] - m * A[i, k]
            
            L[j, i] = m

        logging.debug(f"Después de procesar columna {i}:\n{A}")

    if A[n - 1, n - 1] == 0:
        raise ValueError("No existe solución única.")

    if contar_ops:
        return L, A, contador
    return L, A


# ####################################################################
def resolver_LU(
    L: np.ndarray, 
    U: np.ndarray, 
    b: np.ndarray,
    contar_ops: bool = False
) -> tuple[np.ndarray, ContadorOperaciones] | np.ndarray:
    """Resuelve un sistema de ecuaciones lineales mediante la descomposición LU.

    ## Parameters
    ``L``: matriz triangular inferior.
    ``U``: matriz triangular superior.
    ``b``: vector de términos independientes.
    ``contar_ops``: si True, retorna también un contador de operaciones.

    ## Return
    ``solucion``: vector con la solución del sistema de ecuaciones lineales.
    ``contador``: (opcional) objeto ContadorOperaciones con el conteo de operaciones.
    """
    contador = ContadorOperaciones()
    n = L.shape[0]

    # --- Sustitución hacia adelante (Ly = b)
    logging.debug("Sustitución hacia adelante")
    y = np.zeros((n, 1), dtype=float)
    y[0] = b[0] / L[0, 0]
    contador.mult_div += 1  # 1 división

    for i in range(1, n):
        suma = 0
        for j in range(i):
            suma += L[i, j] * y[j]
            contador.mult_div += 1      # 1 multiplicación
            contador.sumas_restas += 1  # 1 suma
        
        y[i] = (b[i] - suma) / L[i, i]
        contador.sumas_restas += 1  # 1 resta
        contador.mult_div += 1      # 1 división

    logging.debug(f"y = \n{y}")

    # --- Sustitución hacia atrás (Ux = y)
    logging.debug("Sustitución hacia atrás")
    sol = np.zeros((n, 1), dtype=float)
    sol[-1] = y[-1] / U[-1, -1]
    contador.mult_div += 1  # 1 división

    for i in range(n - 2, -1, -1):
        suma = 0
        for j in range(i + 1, n):
            suma += U[i, j] * sol[j]
            contador.mult_div += 1      # 1 multiplicación
            contador.sumas_restas += 1  # 1 suma
        
        sol[i] = (y[i] - suma) / U[i, i]
        contador.sumas_restas += 1  # 1 resta
        contador.mult_div += 1      # 1 división

    logging.debug(f"x = \n{sol}")
    
    if contar_ops:
        return sol, contador
    return sol


# ####################################################################
def gauss_jordan(
    A: np.ndarray | list[list[float | int]], 
    contar_ops: bool = False
) -> tuple[np.ndarray, ContadorOperaciones] | np.ndarray:
    """Resuelve un sistema de ecuaciones lineales mediante Gauss-Jordan.

    ## Parameters
    ``A``: matriz aumentada del sistema de ecuaciones lineales. 
           Debe ser de tamaño n-by-(n+1).
    ``contar_ops``: si True, retorna también un contador de operaciones.

    ## Return
    ``solucion``: vector con la solución del sistema de ecuaciones lineales.
    ``contador``: (opcional) objeto ContadorOperaciones con el conteo de operaciones.
    """
    contador = ContadorOperaciones()
    
    if not isinstance(A, np.ndarray):
        A = np.array(A, dtype=float)
    else:
        A = A.astype(float).copy()
    
    assert A.shape[0] == A.shape[1] - 1, "La matriz A debe ser de tamaño n-by-(n+1)."
    n = A.shape[0]

    # Fase de eliminación (hacia adelante y hacia atrás)
    for i in range(n):
        # Buscar pivote
        p = None
        for pi in range(i, n):
            if A[pi, i] == 0:
                continue
            if p is None:
                p = pi
                continue
            if abs(A[pi, i]) > abs(A[p, i]):
                p = pi

        if p is None:
            raise ValueError("No existe solución única.")

        if p != i:
            _aux = A[i, :].copy()
            A[i, :] = A[p, :].copy()
            A[p, :] = _aux
            contador.intercambios += 1

        # Normalizar fila pivote
        pivot = A[i, i]
        for k in range(i, n + 1):
            A[i, k] = A[i, k] / pivot
            contador.mult_div += 1
        
        # Eliminar en todas las demás filas (no solo hacia abajo)
        for j in range(n):
            if j == i:
                continue
            
            m = A[j, i]
            for k in range(i, n + 1):
                contador.mult_div += 1      # 1 multiplicación
                contador.sumas_restas += 1  # 1 resta
                A[j, k] = A[j, k] - m * A[i, k]

    solucion = A[:, n]
    
    if contar_ops:
        return solucion, contador
    return solucion


# ####################################################################
def matriz_aumentada(A: np.ndarray, b: np.ndarray) -> np.ndarray:
    """Construye la matriz aumentada de un sistema de ecuaciones lineales."""
    if not isinstance(A, np.ndarray):
        A = np.array(A, dtype=float)
    if not isinstance(b, np.ndarray):
        b = np.array(b, dtype=float)
    assert A.shape[0] == b.shape[0], "Las dimensiones de A y b no coinciden."
    return np.hstack((A, b.reshape(-1, 1)))


def separar_m_aumentada(Ab: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """Separa la matriz aumentada en A y b."""
    if not isinstance(Ab, np.ndarray):
        Ab = np.array(Ab, dtype=float)
    return Ab[:, :-1], Ab[:, -1].reshape(-1, 1)




def complejidad_teorica_gauss(n: int) -> dict:
    """Retorna la complejidad teórica del método de Gauss."""
    # Eliminación: n³/3 + n²/2 - 5n/6 operaciones de mult/div
    #              n³/3 - n/3 operaciones de suma/resta
    # Sustitución: n²/2 + n/2 operaciones de mult/div
    #              n²/2 - n/2 operaciones de suma/resta
    
    mult_div = (n**3)/3 + (n**2)/2 - (5*n)/6 + (n**2)/2 + n/2
    sumas_restas = (n**3)/3 - n/3 + (n**2)/2 - n/2
    
    return {
        'mult_div': int(mult_div),
        'sumas_restas': int(sumas_restas)
    }


def complejidad_teorica_gauss_jordan(n: int) -> dict:
    """Retorna la complejidad teórica del método de Gauss-Jordan."""
    # Gauss-Jordan tiene mayor complejidad: aproximadamente n³/2 para mult/div
    mult_div = (n**3)/2 + (n**2)/2 - n/2
    sumas_restas = (n**3)/2 - (n**2)/2
    
    return {
        'mult_div': int(mult_div),
        'sumas_restas': int(sumas_restas)
    }


def complejidad_teorica_LU(n: int) -> dict:
    """Retorna la complejidad teórica de la descomposición LU."""
    # Descomposición: n³/3 - n/3 operaciones
    # Resolución (2 sustituciones): n²
    
    descomp_mult_div = (n**3)/3 - n/3
    descomp_sumas_restas = (n**3)/3 - n/3
    
    resolucion_mult_div = n**2
    resolucion_sumas_restas = n**2 - n
    
    return {
        'descomposicion': {
            'mult_div': int(descomp_mult_div),
            'sumas_restas': int(descomp_sumas_restas)
        },
        'resolucion': {
            'mult_div': int(resolucion_mult_div),
            'sumas_restas': int(resolucion_sumas_restas)
        },
        'total': {
            'mult_div': int(descomp_mult_div + resolucion_mult_div),
            'sumas_restas': int(descomp_sumas_restas + resolucion_sumas_restas)
        }
    }