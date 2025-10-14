# Markdown
## Subtitulo 1
### Subtitulo 2
* **Documentación en Github**
* Ecuaciones!
    * En Notebook de python
* Viñeta 1
* Viñeta 2
# Documentar en lenguaje de *programación*
``` python
def suma(x1:int, x2:int):
    return x1 + x2
```

``` matlab
function y = suma(x1, x2)
    y = x1+ x2;
```
# Micelánea
* Cambia distribución de teclado
windows + spacio

# Redacción de ecuaciones en Markdown 
Comando para previsualizar: ctrl+shift+v

# Ejemplo
Fórmula para calcular las raices de la ecuación cuadrática. 
$x_1= (-b + \sqrt{b^2 -4ac})/2a $

$x_1= \frac{-b + \sqrt{b^2 -4ac}}{2a} $

$x_2= \frac{-b - \sqrt{b^2 -4ac}}{2a} $

$\pi,\alpha,\beta, \hat{y}, \leftarrow$

# Ejercicio
Escribir la ecuación Navier Stokes.

$\rho \partial$
$\rho \delta$

$\rho  \frac{ D \overrightarrow{V}}{Dt} = $

$\sum_i^4$

Hay que subirlo al taller.


# Taller!
* Se debe presentar:
    * Notebook
    * Enlace al repositorio

## Ejercicio 1
La sumatoria $1 + 1/2 + 1/4 +1/8 ... $ tal que el error absoluto $e_{abs} < 10^{-1}$.

## Ejercicio 2 (Bubble sort)
<!-- ![XSDF](.\E2.jpeg) -->

### Corrida de escritorio
$v_1=[3, 2, 5, 8, 4, 1]$

| i | Vector |
| -- | -- |
| 0 | $ [3, 2, 5, 8, 4, 1] $ |
| 1 | $ [3, 2, 5, 4, 1, 8] $|
| 2 | $ [3, 2, 4, 1, 5, 8] $|
| 3 | $ [3, 2, 1, 4, 5, 8] $|
...

Resultado final:

$v_{sorted} = [1,2,3,4,5,8]$

Casos de prueba:
* $v_2=[-1, 0, 4, 5, 6, 7]$
* $v_3$ 100_000 número aleatorios entre -200 y 145. 

# Algoritmo 3
![XSDF](.\fibonacci.jpeg)

| n | fib(n) |
| -- | -- |
| 0 | 0 |
| 1 | 1 |
| 2 | 1 |
| 3 | 2 |
| 4 | 3 |
| 5 | 5 |
| 6 | 8 |
| 6 | 13 |
| ... | ... |
|$n = 11 $ | ? |
|$n = 84 $ | ? |
|$n = 1531$ | ? |

## Graficar!
* El valor de la serie $fib(n)$
* El valor del cociente 

    $\phi \rightarrow \frac{fib(n)} {fib(n-1)} \approx 1.618$ número áureo.


| n | $ fib(n) /fib(n-1) $ |
| -- | -- |
| 2 | $1/1=1 $ |
| 3 | $2/1 = 2$ |
| 4 | $3/2 = 1.5$ |
| 5 | $5/3= 1.66667$ |
| 6 | $8/5= 1.6$ |
| 7 | $13/8 = 1.625 $ |
| 8 | $21/13 = 1.615 $ |
| ... | ... |
|$\infty $ | $ \frac{1 + \sqrt{5}} {2} \approx 1.618$ (número áureo) |


# Breve revisión *git*
* Inicializar repositorio
``` bash
git init 
```
* ¿Qué significa la U?
    * No están añadidos
    * Se añaden con
    ``` bash
    git add file1 file2... 
    ```
    * Nunca!  Añade **TODO**!
    ``` bash
    git add . 
    ```
    * git commit
    ``` bash
    git commit -m "actualización de código" 
    ```
