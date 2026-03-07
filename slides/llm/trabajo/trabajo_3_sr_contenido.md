# Trabajo 3: SR basado en contenido (SRBC)

## Descripción
El SRBC recomienda películas que satisfacen los gustos del usuario:
- Utiliza el vector de preferencias del perfil del usuario.
- Busca ítems clasificados en los géneros con mayor ratio de preferencia.

## Preferencias del usuario
- Todos los usuarios tienen preferencias en el momento de solicitar la recomendación.
- **Usuario nuevo**: se piden al registrarse.
- **Usuario del dataset**: se obtienen de las películas puntuadas favorablemente.

El perfil contiene: `id_usuario`, preferencias, histórico de interacción, información interna del SR.

## Selección de preferencias para la recomendación
No se usan todas las preferencias del perfil, sino un subconjunto de las **5-8 con mayor ratio**:
- **No borrar** el vector original. Crear un nuevo vector filtrado.
- Si entre las 5-8 mejores hay valores bajos, descartarlos (ej: si los valores son 90-80-75-10-3, usar solo 90-80-75).

**Ejemplo:**

| Género                   |  0 |  1 |  2 |  3 |  4 |  5 |  6 |  7 | 19 |
|--------------------------|----|----|----|----|----|----|----|----|--- |
| Preferencias del perfil  |  0 | 90 | 10 | 90 |  7 | 85 |  0 | 77 | 86 |
| Nuevo vector (filtrado)  |  0 | 90 |  0 | 90 |  0 | 85 |  0 | 77 | 86 |

## Proceso de recomendación
1. A partir del vector filtrado, obtener todos los ítems clasificados en alguna de las preferencias seleccionadas.
2. Eliminar los ítems ya vistos (en el histórico de entrenamiento; si es usuario nuevo, no tiene histórico).
3. Para cada ítem restante, calcular el ratio de interés del usuario.
4. Ordenar la lista por ratio (de mayor a menor).
5. Mostrar los N ítems con mayor ratio en la interfaz.

## Cálculo del ratio de interés (Paso 3)
El ratio se calcula en función de (la fórmula la definís vosotros):
- Ratio de las preferencias del usuario que coinciden con las categorías del ítem.
- Número de preferencias coincidentes.
- Puntuación media de los usuarios al ítem.
- Número de votos (fiabilidad de la puntuación media).

**Ejemplo — Ítem: Forrest Gump**
- Puntuación media: 8.2, Votos: 8147.
- Géneros: Comedy (6), Drama (3), Romance (15).
- Preferencias del usuario: `ru_p6=90`, `ru_p3=100`, `ru_p15=0`.

$$r_{ui} = f(ru_{p6},\; ru_{p3},\; \text{puntuacion\_media},\; \text{votos})$$

La función debe tener en cuenta: nº de preferencias coincidentes, ratio de cada preferencia coincidente, puntuación media y nº de votos.

## Mostrar resultados (Paso 5)
- N ítems de mayor ratio (N definido por la interfaz o por umbral de ratio).
- Mostrar: carátulas, etiquetas (keywords), información de IMDB, estrellas, explicación de la recomendación.
