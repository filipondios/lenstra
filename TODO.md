# TODO — De "detector débil" a factorizador con Miller–Rabin

## Contexto y decisión de diseño (leer antes de empezar)

El proyecto actual **no factoriza**: sólo imprime "no primo" cuando una inversión modular falla,
y ni siquiera calcula el factor. Además, intenta usar Lenstra ECM con un punto que no está en la curva.

**Aclaración importante:** Miller–Rabin **no es un algoritmo de factorización**, es un *test de primalidad*.
Para obtener los factores primos hay que combinarlo con un algoritmo de factorización:

```
n
 ├─ 1. Miller–Rabin  →  ¿es primo?  ── sí ─→ devolver [n]
 │                                  └─ no
 ├─ 2. Trial division (primos pequeños)
 ├─ 3. Pollard rho (factores pequeños/medianos, rápido)
 └─ 4. ECM / Lenstra corregido (factores grandes) → recursar sobre cada factor
```

Objetivo final: `python lenstra.py -n <numero>` imprime la descomposición prima,
p. ej. `561 = 3^1 * 11^1 * 17^1`, con productos de factores == n (invariante verificable).

Rango objetivo decidido: para `n < 2^64`, Miller–Rabin determinista con bases fijas;
para `n >= 2^64`, probabilístico con `--rounds`. Entry point: `lenstra.py` en la raíz;
librería: `lib/` (ya es la estructura actual, sin cambios).

---

## Fase 0 — Preliminares (15 min)

- [x] Crear rama `refactor/factorizacion` y confirmar el estado limpio de `git status`.
- [x] Decidir nombre del entry point: conservar `lenstra.py` como CLI única y mover la librería a `lib/`. Ya estaba así.
- [x] Anotar el rango objetivo de `n`: ver la sección "Contexto y decisión de diseño" arriba.
- [x] Instalar el entorno de tests con uv: `uv venv && uv pip install pytest`; ejecutar con `.venv/bin/python -m pytest -q`. Se eligió pytest porque los tests ya usan `assert` a nivel de módulo.

## Fase 1 — Arreglar los bloqueadores del código actual

- [ ] **Punto inicial dentro de la curva** (`lenstra.py:27`): hoy es `Point(0, pow(curve.b, 2))`,
      pero y²=b⁴ ≠ b. Reemplazar por el truco estándar: elegir `x`, `y` aleatorios y definir
      `b = (y*y - x*x*x - a*x) % n`. Verificado: con a=18, b=9, n=101, el punto actual da y²≡97 vs RHS≡9.
- [ ] **Recuperar el factor cuando falla la inversión** (`lenstra.py:37-41`): hoy se captura `ValueError`
      y se descarta. Calcular `g = gcd(p.x - q.x, n)` (o `gcd(2*p.y, n)` al duplicar) e imprimirlo.
      Verificado: `gcd(24,15)=3`, `gcd(24,561)=3`.
- [ ] **No confundir todo `ValueError` con "factor encontrado"** (`lenstra.py:24-41`, `lib/curve.py:16,32,42`):
      definir una excepción propia lanzada **sólo** desde la inversión modular. Hoy `n=0`, `n=1` y `n=-7`
      imprimen "is not prime" porque falla `randint(1, modulo-1)`, no por encontrar un factor.
- [ ] **Validar entrada** (`lenstra.py:7-17`): `n >= 2`, `iterations >= 1` y `choices` para `-b`
      (hoy `-b foo` lanza `KeyError` en crudo, y `-i -1` imprime "maybe prime").
- [ ] **Arreglar los tests** (`tests/addition.py`, `tests/multiplication.py`):
      - imports relativos `..lib` / `..lenstra.point` → imports absolutos `from lib.point import Point`.
      - `Curve(0, 7, 97)` → `Curve(97)` + asignar `a`, `b` (o ampliar el constructor a `Curve(a, b, modulo)`).
      - añadir `tests/__init__.py` y un runner (`pytest` o `python -m unittest discover`).
      - Nota: las fórmulas de suma/duplicación **ya son correctas** (verificado: (17,19)+(17,19)=(95,75),
        101·(72,57)=(99,43) mod 107). Sólo están mal los tests.
- [ ] **Aislar efectos secundarios**: envolver el CLI en `main()` con `if __name__ == '__main__':`.
      Hoy importar `lenstra.py` ya ejecuta `parse_args()`.

**Criterio de aceptación Fase 1:** los tests corren y pasan; `n=15` devuelve el factor `3`; `n=1`, `n=0`,
`-b foo` dan errores claros, no falsos "no primo".

## Fase 2 — Miller–Rabin (test de primalidad)

- [ ] Crear `lib/miller_rabin.py` con `is_prime(n, rounds=None) -> bool`.
- [ ] Descomponer `n-1 = d * 2^s` con `d` impar y aplicar el test de la base `a`.
- [ ] Bases deterministas para `n < 2^64`: `[2, 3, 5, 7, 11, 13, 17]` cubre hasta 341.550.071.821.
      Para `n < 3.317.444.400.000.000.000` usar `[2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37]`.
      Para `n` mayor, bases aleatorias con `rounds` configurable (por defecto 40).
- [ ] Casos límite: `n < 2` → False; 2 y 3 → True; pares → False; 4 → False.
- [ ] Testear contra números conocidos: 561, 1105, 1729 (Carmichael → compuestos), 2^61-1 (primo),
      3.215.031.751 (pseudoprimo fuerte en bases 2,3,5,7,11,13,17 → debe dar compuesto con la base 31).
- [ ] Usar `is_prime(n)` como **primer filtro** en el flujo: si es primo, devolver `[n]` y terminar.

## Fase 3 — Factorización real

- [ ] Crear `lib/factor.py` con `factorize(n) -> dict[int, int]` (primo → exponente).
- [ ] Step 1: trial division por primos pequeños (2, 3, 5, ..., 1000) y divisiones repetidas.
- [ ] Step 2: Pollard rho con `f(x) = x² + c` y `gcd(|x-y|, n)`; reintentar con otra `c` si falla.
- [ ] Step 3: ECM/Lenstra corregido para factores grandes:
      - parámetro explícito `B1` (ej. 10000) en lugar del factorial implícito `while k < n`.
      - `k = lcm(1..B1)` (o producto de potencias de primos ≤ B1) en vez de `2·3·4·...·m`.
      - etapa 2 opcional (B2) para primos de orden de grupo entre B1 y B2.
      - ejecutar varias curvas con `a`, `b` aleatorios derivados del punto.
- [ ] Recursión: `factorize(g)` y `factorize(n//g)` hasta que ambos sean primos ( Miller–Rabin ).
- [ ] Invariante: `math.prod(p**e for p, e in factors.items()) == n` antes de devolver.
- [ ] Ordenar salida por primo ascendente.

## Fase 4 — Tests (los que faltan y los que hay que arreglar)

- [ ] `tests/test_curve.py`: suma, duplicación, punto infinito, inverso (p + (-p) = ∞).
- [ ] `tests/test_miller_rabin.py`: primos, compuestos, Carmichael, pseudoprimos, n<2, potencias de 2.
- [ ] `tests/test_factor.py`: 1 → {}, primos → {p:1}, cuadrados → {p:2}, 561 → {3:1,11:1,17:1},
      semiprimos grandes (p·q con p,q de ~64 bits), números con factor repetido, invariante producto==n.
- [ ] `tests/test_cli.py`: ejecutar el entry point con `subprocess` y comprobar stdout y exit code
      (0=éxito, 2=entrada inválida).
- [ ] Property test: para 200 `n` aleatorios en [2, 10^9], el producto de los factores devueltos es `n`
      y cada factor pasa `is_prime`.
- [ ] Ejecutar todo en CI (GitHub Actions: `python -m pytest -q` en cada push).

## Fase 5 — CLI experiencia de uso

- [ ] Unificar argumentos: `-n/--number`, `-b/--base`, `--rounds` (Miller–Rabin), `--b1`, `--curvas`,
      `-v/--verbose`, `--seed` (reproducibilidad), `--json` (salida estructurada).
- [ ] Salida por defecto, p. ej.:
      ```
      561 = 3^1 * 11^1 * 17^1  (compuesto, verificado con Miller–Rabin)
      ```
      Para primos: `104729 es primo (Miller–Rabin, 7 bases deterministas)`.
- [ ] En `-v`, imprimir cada curva/factor encontrado y el tiempo invertido.
- [ ] `exit(1)` si no se encuentra la factorización completa dentro del presupuesto, con mensaje claro.
- [ ] Mensaje de error de `argparse` para `-b` inválido en lugar de `KeyError`.

## Fase 6 — Documentación y cierre

- [ ] Reescribir `README.md`: quitar la afirmación de que "encuentra factores pequeños" (hoy no es cierto)
      y documentar Miller–Rabin + Pollard rho + ECM, con ejemplos reales de salida.
- [ ] Explicar en el README que Miller–Rabin es probabilístico para n ≥ 2^64 y por qué se usan
      varias bases; aclarar el significado de "maybe prime" del programa anterior.
- [ ] Añadir `pyproject.toml` (nombre, versión, entry point `factorizador = lenstra:main`, Python ≥3.9).
- [ ] Añadir licencia ya existente al paquete; verificar que `LICENSE` esté referenciada.
- [ ] Eliminar código muerto: contador `iteration` manual en `lenstra.py:35`, rama de logging duplicada.
- [ ] Benchmark rápido: tiempo para semiprimos de 32, 64 y 128 bits; anotar los números en el README.

## Criterios de "aplicación terminada"

- [ ] `python lenstra.py -n 561` → `561 = 3^1 * 11^1 * 17^1`.
- [ ] `python lenstra.py -n 104729` → `104729 es primo`.
- [ ] `python lenstra.py -n 0`, `-b foo`, `-i -1` → errores claros, sin tracebacks.
- [ ] `python -m pytest -q` → todos verde, incluyendo el invariante producto==n.
- [ ] README y `--help` coinciden con el comportamiento real.
