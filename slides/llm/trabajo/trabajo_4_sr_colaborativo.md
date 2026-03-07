# Trabajo 4: SR Colaborativo (SRC)

## Descripción
El SRC busca usuarios similares al usuario actual (vecinos) y recomienda ítems que les han gustado. La similitud se calcula con el **coeficiente de correlación de Pearson**.

## Preferencias para la búsqueda de vecinos
- Se usan las **preferencias por género** (no el histórico de ítems — más de 27.000 películas harían las matrices demasiado grandes).
- A diferencia del SRBC, se usan **todas las preferencias** (no un subconjunto).
- El vector debe estar mayormente relleno: un 0 significa "no interesado", no "sin dato".
- Si hay pocas preferencias con valor puede dar lugar a **falsos vecinos**.

|                     | SRBC                                               | SRC                      |
|---------------------|----------------------------------------------------|--------------------------|
| **Usuario dataset** | Preferencias de películas favorables (5-8 de mayor ratio) | Todas las preferencias   |
| **Usuario nuevo**   | Preferencias pedidas al registrarse                | Todas las preferencias   |

## Búsqueda de vecinos

### Matriz de ratios
- Filas: usuarios. Columnas: las 20 preferencias (géneros).
- Se usa **unión** (todos los géneros, no solo los comunes). Valores no informados = 0.

### Proceso
1. Crear la matriz de preferencias de todos los usuarios.
2. Para cada par $(u, u')$, calcular el coeficiente de Pearson.
3. Repetir para todos los usuarios.
4. Seleccionar los **40-50 vecinos** con mayor afinidad (coeficiente más cercano a 1), o los que superen un umbral.

### Diferencias por tipo de usuario
- **Usuario del dataset**: preproceso (calcular vecinos de todos los usuarios y guardarlos en sus perfiles).
- **Usuario nuevo**: al registrarse, se calculan sus vecinos y se almacenan en su perfil.

## Correlación de Pearson

$$r_{uu'} = \frac{Cov(v_u,\, v_{u'})}{\sqrt{Var(v_u) \cdot Var(v_{u'})}}$$

- $r = 1$: correlación positiva perfecta.
- $0 < r < 1$: correlación positiva.
- $r = 0$: sin relación lineal.
- $-1 < r < 0$: correlación negativa.
- $r = -1$: correlación negativa perfecta.

La relación de vecindad es **asimétrica**, pero el coeficiente de Pearson es **simétrico**.

## Perfil de usuario
- `id_usuario`.
- Modelo de preferencias.
- Histórico: ítems visitados con su ratio.
- Información interna: lista de vecinos $V_u = \{(u', ra_{u'}) \mid u' \in U,\; ra_{u'} \in [0, 100]\}$.

Número de vecinos variable; para cada vecino se guarda su `id` y su grado de afinidad (0-100).

## Obtención de la lista de ítems recomendados
1. Para cada vecino, obtener los ítems de su histórico puntuados **favorablemente**.
2. Eliminar ítems repetidos (presentes en más de un vecino).
3. Combinar los ratios ponderando por afinidad:

$$ru_i = \frac{\displaystyle\sum_{u' \in V_u,\, i \in l_{u'}} ra_{u'} \cdot ru'_i}{\displaystyle\sum_{u' \in V_u,\, i \in l_{u'}} |ra_{u'}|}$$

4. Calcular el ratio de interés del ítem para el usuario.
5. Eliminar los ítems ya vistos por el usuario (en su histórico).

## Proceso final
- Ordenar por ratio y mostrar los N ítems con mayor ratio (similar al SRBC).

**Flujo por tipo de usuario:**
- **Usuario del dataset / ya registrado**: ya tiene vecinos calculados → mostrar recomendación directamente.
- **Usuario nuevo**: registrar → pedir preferencias → calcular vecinos → mostrar recomendación.
