# Trabajo 2: Datos base

## Objetivo
- Los ítems a recomendar son películas de "The Movies Dataset".
- El objetivo es obtener una lista de ítems recomendados adaptada al usuario (ratio de interés).
- Esta parte prepara el almacenamiento de datos y define las estructuras necesarias para el recomendador.

## Dataset
- Fuente: [The Movies Dataset en Kaggle](https://www.kaggle.com/datasets/rounakbanik/the-movies-dataset).
- Metadatos de más de 45.000 películas, 26 millones de ratings de más de 270.000 usuarios.
- Se proporcionan dos versiones: original y procesada. **Se recomienda usar la procesada.**

### Versión procesada
- Solo películas de habla inglesa, con puntuaciones y keywords en inglés (máx. 12 por película).
- Codificada en UTF-8.
- Puede haber películas en algunos ficheros que no existan en otros. **No recomendar películas que no estén en `peliculas.csv`.**

## Ficheros del dataset

### Géneros (`generos.csv`)
20 géneros. Columnas: `id`, `IdDataset`, `Genero` (inglés), `GeneroSP` (español).

| id | IdDataset | Genero           | GeneroSP        |
|----|-----------|------------------|-----------------|
| 0  | 12        | Adventure        | Aventura        |
| 1  | 14        | Fantasy          | Fantasía        |
| 2  | 16        | Animation        | Animación       |
| 3  | 18        | Drama            | Drama           |
| 4  | 27        | Horror           | Terror          |
| 5  | 28        | Action           | Acción          |
| 6  | 35        | Comedy           | Comedia         |
| 7  | 36        | History          | Histórica       |
| 8  | 37        | Western          | Oeste           |
| 9  | 53        | Thriller         | Suspense        |
| 10 | 80        | Crime            | Crimen          |
| 11 | 99        | Documentary      | Documental      |
| 12 | 878       | Science Fiction  | Ciencia ficción |
| 13 | 9648      | Mystery          | Misterio        |
| 14 | 10402     | Music            | Musical         |
| 15 | 10749     | Romance          | Romance         |
| 16 | 10751     | Family           | Familiar        |
| 17 | 10752     | War              | Guerra          |
| 18 | 10769     | Foreign          | Extranjera      |
| 19 | 10770     | TV Movie         | TV              |

### Etiquetas (`keywords.csv`)
- No todas las películas tienen etiquetas. Cada película tiene máx. 12 etiquetas.
- Columnas: `id` (película), `contador` (nº etiquetas), `kw_1`, ..., `kw_N`.

| id | contador | kw_1     | kw_2   | kw_3           |
|----|----------|----------|--------|----------------|
| 2  | 7        | underdog | prison | factory worker |
| 5  | 9        | hotel    | witch  | bet            |
| 11 | 12       | android  | galaxy | hermit         |

### Películas (`peliculas.csv`)
- 27.840 películas (inglesas, clasificadas y puntuadas).
- Columnas: `id`, `imdbId`, `titulo`, `poster_path`, `puntuacion_media`, `votos`, `contgeneros`, `id_genero_1`, ..., `id_genero_N`.

### Puntuaciones (`ratings_small.csv`)
- 100.004 puntuaciones, usuarios 1-671.
- Columnas: `userId`, `movieId`, `rating` (float, 0.5-5).
- No hay datos demográficos de usuario → no se puede usar SR Demográfico.

## División del dataset
- **Entrenamiento**: 70% de los ratings.
- **Test**: 30% de los ratings.

## Perfil de usuario
Se crea un perfil por cada usuario que ha puntuado ítems. Compuesto por:

### 1. Modelo de preferencias
- Vector de 20 posiciones: ratio de interés en cada género (0-100).
- **Usuario del dataset**: inferido de las puntuaciones favorables del fichero de entrenamiento.
  - Convertir puntuaciones (0.5-5) a escala 0-100.
  - Si no hay películas puntuadas en una categoría → 0.
  - Calcular ratio teniendo en cuenta: nº de películas puntuadas en esa categoría y puntuaciones dadas.
- **Usuario registrado**: se piden las preferencias en el registro.

### 2. Histórico de interacción
- Conjunto de películas vistas por el usuario (del fichero de entrenamiento) con su puntuación (0.5-5).

### 3. Información interna del SR
- Información calculada por el SR para facilitar la recomendación (ej: vecinos para SR Colaborativo).
- Inicialmente vacía.
- Para vecinos: nº de vecinos + lista de `(id_vecino, afinidad)` con afinidad en [0, 100].

## Lista de ítems recomendados
- **Para un usuario**: todas las películas no vistas (no en su histórico).
- **Para un grupo**: todas las películas no vistas por ningún miembro del grupo.
- Formato por ítem: `(id_película, ratio_interés)`, ordenada por ratio (mayor a menor).

> ⚠️ **Importante**: Al cargar los datos en la aplicación no puede haber referencias a películas que no existan en `peliculas.csv`.

## Próximos pasos
- Dividir el fichero de ratings en entrenamiento y test.
- Crear y rellenar los perfiles de usuario.
- Almacenar los datos de las películas.
