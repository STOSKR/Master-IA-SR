# Tema 2: Sistemas Recomendadores (SR)

## 1. Definición y Conceptos Básicos

**Sistema Recomendador (SR)** (Resnick, 1997):
- Tipo específico de filtro de información adaptativo.
- Presenta al usuario únicamente información de su interés, adelantándose a sus necesidades.
- Recomendar = hacer una predicción sobre los intereses del usuario.

### Evolución Histórica

| Año | Sistema | Descripción |
|---|---|---|
| 1992 | Tapestry (Goldberg) | Correo electrónico experimental con filtrado colaborativo |
| 1994 | GroupLens (Resnick) | Noticias |
| 1997 | MovieLens (Konstan) | Recomendador de películas; dataset aún utilizado |
| 1997 | Firefly (Maes) | SR de música con calificación y etiquetado para construir perfiles |

### Definición Formal

Sea $U$ el conjunto de usuarios, $I$ el de ítems, $R$ el conjunto ordenado de ratios:

$$f_u: U \times I \longrightarrow R$$
$$\forall u \in U, \exists i' \in I \mid I_u' = \max_{i \in I}(u, i)$$

- Obtiene un ratio para todos los ítems mediante una función de utilidad personalizada.
- Selecciona el subconjunto de ítems que maximiza la utilidad.

## 2. Personalización y Aplicaciones

- Simula la interacción con un experto humano; se basa en preferencias e intereses del usuario.
- Clasifica los ítems según utilidad o interés para el usuario.
- Permite publicidad personalizada más efectiva y mayor fidelización de clientes.
- Muestra una cantidad de información manejable, adaptada a las necesidades del usuario.

## 3. Usuarios e Ítems

### Usuarios

- **Individual:** Preferencias de un solo usuario.
- **Grupo:** Mezcla de preferencias que satisfaga a todos los miembros; se deben considerar restricciones (niños, discapacidades...).

### Ítems

- Cualquier elemento a recomendar: producto, película, destino turístico, URL, etc.
- El SR calcula el ratio de utilidad de cada ítem y selecciona los de mayor ratio.
- Con gran cantidad de ítems se puede hacer filtrado previo por tipo.

## 4. El Proceso de Recomendación

1. **Obtener información del usuario:** Recopilada previamente o por interacción (difícil).
2. **Recomendación:** Seleccionar los ítems a recomendar.
3. **Feedback:** Satisfacción del usuario con la recomendación (muy difícil).

**Flujo:** Usuario → info entrada → Interfaz → SR → lista de ítems → Interfaz → (feedback optativo) → SR.

**Ejemplo (tienda online):**
- Comprobar accesos anteriores (usuario registrado, cookies) + búsqueda actual.
- Seleccionar ítems similares o comprados por usuarios con búsquedas similares.
- Feedback: compra, visita o clic en ítem recomendado → actualiza perfil del usuario.

## 5. Técnicas de Recomendación Básicas (BRTs)

- **SR Demográfico:** Clasifica al usuario por características demográficas y recomienda según su grupo. Requiere una clasificación de usuarios común al sistema.
- **SR Basado en Contenido:** Recomienda ítems similares a los que el usuario ha puntuado favorablemente. Apropiado cuando los ítems se generan dinámicamente (email, noticias).
- **SR Colaborativo:** Usa información de otros usuarios (vecinos/patrones/inferencias). Recomienda lo que leyeron usuarios similares al actual.

**Otras técnicas:**

| SR basados en conocimiento | SR basados en utilidad | SR basados en casos |
|---|---|---|
| SR basado en restricciones | SR basados en crítica | SR sociales |
| SR multi-criterio | SR context-aware | SR conversacional |

## 6. Información y Algoritmo de Recomendación

**Información utilizada:** Datos del usuario, de otros usuarios, del entorno (demografía) y de los ítems.

**Condiciones para una buena recomendación:**
- **Ítems:** Muchos, bien clasificados (taxonomía/ontología rica) y variados.
- **Usuarios:** Muchos, con mucha información y alta interacción.
- *Mucha información adecuada + bien clasificada + buen algoritmo = buena recomendación.*

**Algoritmo:**
- **Predicción:** Construye un modelo para predecir los ratios de interés de los ítems.
- **Selección:** Selecciona los N ítems no puntuados de mayor ratio para el usuario.

Puede trabajar en dos pasos: preferencias → ítems, o directamente ítems.

## 7. Datos

### Datos de entrada

- Lo que el usuario busca en ese momento (guía y restringe la recomendación).
- Algunos SR aprovechan para solicitar información adicional al usuario.

### Datos base

**Información de ítems:**
- Clasificados en ontología/taxonomía; cada ítem tiene características asociadas.
- A mejor clasificación y mayor variedad de ítems, mejor recomendación.

**Perfil de usuario:**
- **Información demográfica:** Edad, sexo, profesión, familia, país, etc.
- **Modelo de preferencias:** Tipo de ítems de interés con ratio de interés (dinámico; se modifica, añaden o eliminan).
- **Histórico de interacción:** Ítems visitados/comprados con grado de satisfacción.
- **Información interna del SR:** Clasificación del usuario, usuarios similares, etc.

### Datos de salida

- Único ítem o lista ordenada por ratios (top-N o umbral mínimo).
- Puede mostrarse con o sin el ratio numérico.
- Puede ofrecer ítems variados (proporciones de distintas categorías).

## 8. Problemas del Proceso de Recomendación

**Características deseables:**
- Dar recomendación independientemente de los datos disponibles.
- Atender a cualquier usuario, incluso nuevos o con gustos extraños.
- Introducir novedad (ítems similares pero no idénticos).

**Problemas comunes:**

| Problema | Descripción | Solución |
|---|---|---|
| **Nuevo usuario (cold start)** | Sin historial ni puntuaciones | Relleno manual del perfil |
| **Nuevo ítem** | Pocas puntuaciones; difícil de recomendar | Solo afecta a técnicas basadas en puntuaciones |
| **Sparsity / oveja negra** | Gustos poco comunes sin suficientes similitudes | — |
| **Efecto portfolio** | No recomendar ítems demasiado parecidos a los ya vistos | — |
| **Serendipity** | Ofrecer solo similares, sin novedad | — |
| **Recopilar info del usuario** | Miedo a falta de privacidad o proceso tedioso | Información mínima y técnicas no intrusivas |
| **Falta/exceso de resultados** | Recomendaciones vacías o sin sentido | SR conversacionales |
| **Sensibilidad al cambio** | ¿Detecta cambios en las preferencias del usuario? | Feedback |

