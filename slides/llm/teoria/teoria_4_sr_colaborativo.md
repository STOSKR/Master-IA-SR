# Tema 4: SR Colaborativo

## 1. Tipos de SR Básicos (BRTs)

- **SR demográfico:** Preferencias demográficas del usuario.
- **SR basado en contenido:** Preferencias basadas en tipos de ítems que le "gustan" al usuario.
- **SR colaborativo:** Información y/o gustos de otros usuarios → $Vecinos/patrones/inferencias$.

## 2. Concepto del SR Colaborativo

**Es la técnica más utilizada.** Recomienda ítems en función de:
- Los ítems puntuados/comprados/vistos por otros usuarios.
- O por las preferencias comunes con otros usuarios.

**Idea:** Información del usuario actual + información de otros usuarios → Recomendación.

**SR colaborativo tradicional:**
- Define similitudes entre usuarios.
- Usa los ítems puntuados favorablemente por usuarios similares para obtener la recomendación.
- **Usuarios similares (vecinos):** tienen gustos parecidos y han puntuado favorablemente ítems que el usuario actual también ha puntuado favorablemente.

**Diferencia con basado en contenido:**
- *Content-based:* ítems similares → recomendados al usuario.
- *Collaborative:* ítems leídos por usuarios similares → recomendados al usuario.

## 3. Datos

**Datos base:**
- **Ítems:** BD con los ítems a recomendar.
- **Usuarios:** Perfil del usuario + perfil de otros usuarios.

**Perfil de usuario:**
- **Información demográfica:** Edad, género, familia, país, etc.
- **Modelo de preferencias:** Gustos, tipo de ítems de interés.
- **Histórico de interacción:** Ítems recomendados/visitados/comprados con grado de satisfacción.
- **Información interna del SR:** Clasificación del usuario, usuarios similares, etc.

**Aspectos positivos:**
- No es necesario que los datos estén clasificados en ontología/taxonomía ni que tengan etiquetas.

**Aspectos negativos:**
- Necesita datos de muchos usuarios.

## 4. Clasificación de los SR Colaborativos

1. **Métodos basados en memoria** (tradicionales):
   - *Basados en similitud:*
     - Similitud basada en **usuarios** (vecinos)
     - Similitud basada en **ítems**
   - *Basados en estructura:* modelan el problema en forma de grafos.

2. **Métodos basados en modelos** (costosos computacionalmente): crean modelos de cómo los usuarios puntúan los ítems.

3. **Mezcla de ambos métodos.**

Todos tienen en común: se basan en la información de otros usuarios del sistema y del usuario que solicita la recomendación.

## 5. SR Colaborativo Basado en Similitud

- **Similitud basada en usuarios (vecinos):** busca vecinos del usuario actual (por preferencias, ítems puntuados o características).
- **Similitud basada en ítems:** obtiene similitudes entre la forma en que se puntúan los ítems.

Recomienda ítems de los vecinos (si hay vecinos).

## 6. SR Colaborativo Basado en Vecinos (KNN)

**Vecinos de un usuario:** subconjunto de usuarios más afines al usuario actual:
- Con gustos (preferencias) similares.
- Con comportamientos similares en sus interacciones con los ítems.
- Con ítems puntuados de la misma forma.
- Con características similares.

**Tipos de vecinos:**
- **Según preferencias:** los que tienen gustos parecidos.
- **Según ítems:** los que han puntuado ítems de forma similar.
- **Según características:** los que tienen características demográficas similares.
- **Mezcla de dos o más.**

### User-based Filtering (GroupLens, 1994)

*"Puede que te guste porque a 'tus amigos' les gustó."*

1. Calcular la similitud entre el usuario actual y el resto de usuarios.
2. Seleccionar los vecinos de mayor similitud.
3. Recomendar ítems puntuados favorablemente por esos vecinos.

**Ejemplo:**

|  | I1 | I2 | I3 | I4 |
|---|---|---|---|---|
| **U1** | X | X |  |  |
| **U2** | X |  | X | X |
| **U3** | X | X | X |  |
| **U4** |  | X |  | X |
| **U5** |  | X | X | X |

- U1 puntúa I1 e I2 → vecino más similar: U3 → recomienda I3.

### Comparación de enfoques para obtener vecinos

| Enfoque | Precisión | Inconvenientes |
|---|---|---|
| **Basado en ítems** | Más precisa | Pocas coincidencias posibles; matrices muy grandes |
| **Basado en preferencias** | Menos precisa | Requiere conocer las preferencias; matrices más pequeñas |
| **Basado en características** | Mucho menos precisa | Simula un SR demográfico; funciona bien mezclado |

### Número de vecinos

- Encontrar vecinos puede ser costoso; se puede hacer periódicamente y almacenar en el perfil.
- En sistemas grandes, no superar 40-50 vecinos: más vecinos añaden información redundante sin mejorar la recomendación.

### Proceso (ejemplo con ítems)

1. Crear la **Ratings Matrix** (usuarios × ítems).
2. Calcular el **ratio de similitud** entre el usuario actual y el resto (distancia euclídea, coseno, Pearson).
3. **Ponderar** el ratio de cada ítem de cada vecino por su afinidad.
4. **Weight Sum:** sumar los ratios ponderados por ítem.
5. **Normalizar:** dividir la suma de ratios del ítem por la suma de similitudes → ratio final para el usuario.

### Inconvenientes del SR basado en vecinos

- Nunca puede recomendar un ítem no puntuado por un vecino.
- Problema para ítems nuevos en el sistema.

## 7. Métricas de Similitud

Para calcular la similitud de dos usuarios A y B (representados como vectores):

**1. Similitud del coseno:**
$$Sim(A,B) = \frac{A \cdot B}{||A||\ ||B||}$$
- Rango: $[-1, 1]$. 1 = totalmente similares, 0 = ortogonales, -1 = opuestos.
- **Ventajas:** Funciona bien con datos dispersos; computacionalmente eficiente.
- **Desventajas:** No considera diferencias de escala; problemas con pocas posiciones en común.

**2. Distancia euclídea inversa:**
$$Sim(A,B) = \frac{1}{1 + d(A,B)}$$
- Rango: $(0, 1]$. 1 = muy similares, 0 = muy diferentes.
- **Ventajas:** Fácil de calcular; funciona bien buscando puntuaciones exactas.
- **Desventajas:** Funciona mal con escalas diferentes; no captura relaciones positivas/negativas.

**3. Coeficiente de correlación de Pearson:**
$$Sim(A,B) = \frac{\sum(A_i - \bar{A})(B_i - \bar{B})}{\sqrt{\sum(A_i - \bar{A})^2}\ \sqrt{\sum(B_i - \bar{B})^2}}$$
- Rango: $[-1, 1]$. 1 = relación positiva perfecta, 0 = sin relación, -1 = relación negativa.
- **Ventajas:** Considera la escala; detecta si siguen el mismo patrón; muy usada en SR clásicos.
- **Desventajas:** Puede no funcionar con pocos datos en común; solo captura relaciones lineales.
- Solo se puede usar cuando los datos tienen distribución normal (si no, usar Spearman).

**Comparativa:**

| Métrica | Importa la escala | Detecta relaciones inversas |
|---|---|---|
| Similitud del coseno (ángulo entre vectores) | No | Sí |
| Distancia euclídea inversa (diferencia absoluta) | Sí | No |
| Correlación de Pearson (relación lineal) | No | Sí |

La mejor métrica depende del contexto (ej. coseno para patrones similares como Netflix; euclídea para valores exactos como en salud).

## 8. Matriz de Ratios: Sparsity y Dispersión

**Problemas:**
- **Dispersión de ratios:** diferencias notables entre puntuaciones de usuarios (escalas distintas). *Solución:* normalizar (restar la media, z-score, Pearson).
- **Sparsity:** posiciones vacías en la matriz (el 99% puede estar vacío).

**Estrategias para evitar sparsity:**
- Rellenar posiciones vacías (media, ML, factorización matricial SVD/ALS).
- Agrupar usuarios/ítems con clustering.
- Usar modelos robustos (SVD++, Deep Learning).
- Filtrado previo de usuarios sin mínimo de coincidencias.

**Comparación de vectores con posiciones vacías:**
1. **Intersección:** solo posiciones rellenas de ambos (mayor precisión).
2. **Unión:** todas las posiciones rellenas de ambos.
3. **Todas:** todas las posiciones (rellenando a 0).

**Resumen:**
- **Vecinos según preferencias:** rellenar a 0 (0 = sin interés); usar unión.
- **Vecinos según ítems:** usar solo los que ambos han puntuado; usar intersección.

## 9. Selección de Vecinos y Proceso de Recomendación

**Selección de vecinos** (tres estrategias):
1. Todos los usuarios con similitud mayor que un umbral $\delta$.
2. Los N usuarios de mayor afinidad.
3. Los N usuarios siempre que superen $\delta$.

**Proceso de recomendación:**
1. Recopilar todos los ítems puntuados favorablemente por los vecinos.
2. Calcular el ratio de interés $r_i$ de cada ítem para $u$.
3. Obtener una lista ordenada de ítems a recomendar.

## 10. Ventajas e Inconvenientes

**Ventajas:**
- No es necesario que los ítems estén clasificados.
- Trabaja bien con objetos complejos.
- Introduce novedad en la recomendación.

**Inconvenientes:**
- Trabaja mal cuando hay pocos datos (cold start, sparsity).
- No puede dar recomendación a un usuario nuevo o con gustos muy extraños.
- No puede recomendar un ítem que nunca ha sido puntuado.

## 11. Estado Actual y Futuro

- Integración de deep learning y redes neuronales.
- Uso de grandes modelos de lenguaje (LLMs) para entender la intención del usuario.
- Uso de factores complejos obtenidos del comportamiento de otros usuarios.
