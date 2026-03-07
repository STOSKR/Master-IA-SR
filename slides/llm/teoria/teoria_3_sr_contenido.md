# Tema 3: SR Basado en Contenido

## 1. Tipos de Sistemas Recomendadores Básicos (BRTs)

- **SR demográfico:** Se basa en información sobre el usuario y sus preferencias demográficas.
- **SR basado en contenido:** Se enfoca en los tipos de ítems que le "gustan" al usuario y sus preferencias basadas en contenido.
- **SR colaborativo:** Utiliza información y/o gustos de otros usuarios mediante $vecinos/patrones/inferencias$.

## 2. Concepto General del SR Basado en Contenido

El filtro o sistema basado en contenido genera una recomendación combinando:
1. Preferencias / Histórico del usuario actual.
2. Clasificación de los ítems.

**Idea principal:** Se recomienda al usuario ítems con características similares a los que ha puntuado favorablemente en el pasado, o bien los que están clasificados según sus preferencias explícitas. Los ítems deben estar clasificados en una ontología o taxonomía.

**Funcionamiento según el conocimiento del usuario:**
- **Si se conocen las preferencias:** Se recomiendan directamente ítems que las satisfacen.
- **Si no se conocen:** Se infieren del histórico de ítems puntuados y luego se recomiendan ítems afines.

**¿Cuándo usarlo?**
- Cuando se conocen bien los gustos del usuario.
- Cuando no hay información de otros usuarios.
- Cuando los ítems se generan dinámicamente (ej. emails, noticias).
- Se suele usar de forma híbrida junto con otras técnicas.

## 3. Datos Utilizados

- **Usuario:** Perfil, preferencias e histórico.
- **Ítems:** Base de datos con ítems clasificados en una taxonomía u ontología.
- **Otra información:** Características aumentadas (etiquetas) y puntuaciones.

## 4. Clasificación de Ítems

La clasificación de los ítems es la clave fundamental; una mejor clasificación genera una mejor recomendación.

| Taxonomía | Ontología |
|---|---|
| Estructura jerárquica (tipo árbol) | Red semántica compleja |
| Relación principal: "es un tipo de" | Define múltiples tipos de relaciones |
| Más simple y rápida | Más expresiva e inteligente |
| Permite filtrado por categoría | Permite razonamiento semántico e inferencia |
| Recomendaciones basadas en categorías | Recomendaciones basadas en significado y contexto |

### Características Aumentadas o Etiquetas

Información adicional sobre el ítem obtenida mediante visión artificial, NLP, audio o scraping.

**Formas de usar etiquetas:**
1. **Filtrado a posteriori:** Obtener recomendaciones regulares y usar etiquetas al final para filtrar.
2. **Como preferencia ponderada:** Añadir el interés del usuario por etiquetas directamente al modelo de preferencias.
3. **Solo visualización:** Mostrar la etiqueta al usuario sin que influya en el cálculo algorítmico.

## 5. El Perfil y las Preferencias del Usuario

Preferencias = intereses en el dominio; habitualmente corresponden a la clasificación taxonómica de los ítems (ej. $0..100$ o verdadero/falso).

**Perfil de usuario:**
- **Información demográfica:** Edad, género, país, etc.
- **Modelo de preferencias:** Gustos, tipos de ítems de interés.
- **Histórico de interacción:** Ítems visitados/comprados y grado de satisfacción.
- **Información interna:** Cálculos del SR como usuarios similares.

Las preferencias son dinámicas: evolucionan con el tiempo, aparecen nuevas o cambian de peso.

## 6. Proceso Matemático de Recomendación

Dadas las preferencias de un usuario $u$ y la clasificación/información de un ítem $i$, el ratio de interés se calcula como:

$$r_{ui} = f(\text{preferencias}_u,\ \text{clasificación}_i,\ \text{otraInformación}_i)$$

## 7. Variantes: Sesión y Secuencia

**SR Basado en Sesión (Session-Based):**
- Modela únicamente las interacciones dentro de la sesión actual.
- Ideal para usuarios anónimos, sesiones cortas o sin login.
- Algoritmos: GRU4Rec, Markov, grafos.

**SR Basado en Secuencia (Sequence-Based):**
- Considera la ordenación temporal de todo el histórico.
- Busca patrones temporales: evolución, hábitos recurrentes y cambios de intención.
- Algoritmos: GRU/LSTM, SASRec, Transformers.

## 8. Ventajas e Inconvenientes

**Ventajas:**
- Se ajusta a los gustos del usuario, incrementando la satisfacción.
- No sufre de *cold-start* para ítems nuevos (no necesita datos de otros usuarios).
- Acomoda usuarios con gustos extraños.
- Facilita la explicación transparente de las recomendaciones.

**Inconvenientes:**
- Muy dependiente de la calidad del clasificado/etiquetado de los ítems.
- Tiende a la *sobre-especialización* (siempre recomienda ítems similares).
- Falta de novedad y descubrimiento.

## 9. Estado Actual y Futuro

- **Presente:** Integración de Deep Learning, multimodalidad (texto, imágenes, audio), características dinámicas, enfoque en explicabilidad, privacidad y ética.
- **Futuro:** Mejorar la representación del dominio y las técnicas para extraer modelos de puntuación y preferencias más precisos.

**Futuro:** La investigación se enfoca en mejorar la representación del dominio y las técnicas para extraer modelos de puntuación y preferencias más precisos.