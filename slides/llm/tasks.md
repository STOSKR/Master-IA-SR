# Tareas

## Lista de tareas sesión 1:
1. Usar el fichero `ratings_small.csv`
2. Crear perfil de usuario por cada usuario (1-671): vector de preferencias (20 géneros, escala 0-100), histórico de interacción (películas del train con su puntuación) e información interna (vecinos, inicialmente vacía)
3. División de dataset en train (70%) - test (30%) con shuffle para que no sean sesgados
4. Almacenar datos de las películas; asegurar que no hay referencias a películas que no existan en `peliculas.csv`
5. Inferir vector de preferencias de los usuarios del dataset a partir de las películas puntuadas favorablemente en el fichero de entrenamiento
6. Registro con preguntas para analizar la preferencia del usuario (nuevo usuario)

## Lista de tareas sesión 2:
1. Seleccionar subvector de preferencias para SR basado en contenido (SRBC): quedarse con las 5-8 de mayor ratio; descartar las que tengan valores bajos respecto al grupo (ej: umbral <40%). No borrar el vector original, crear uno nuevo filtrado.
2. Obtener la lista de ítems recomendados SRBC: eliminar películas vistas (histórico de train), obtener el ratio de interés de cada ítem (función propia basada en: preferencias coincidentes, puntuación media y nº de votos), ordenar por ratio y mostrar N ítems con mayor ratio
3. Interfaz: permitir seleccionar la técnica de recomendación (SRBC, SRC o híbrido) y mostrar resultados con carátulas, keywords, datos IMDB y ratio/estrellas

## Lista de tareas sesión 3 (lab 10-Marzo-2026):
1. Preproceso de vecinos para todos los usuarios del dataset: calcular correlación de Pearson entre todos los pares de usuarios usando el vector completo de preferencias; almacenar los 40-50 vecinos de mayor afinidad en el perfil de cada usuario
2. Para usuario nuevo: calcular sus vecinos al registrarse y almacenarlos en su perfil
3. Obtener lista de ítems recomendados SRC: para cada vecino obtener ítems puntuados favorablemente, eliminar ítems ya vistos por el usuario, combinar ratios ponderando por afinidad con el vecino, ordenar y mostrar N ítems

## Tareas pendientes (sin sesión asignada):
1. **Recomendación para grupos**: combinar los perfiles de los usuarios del grupo para obtener una lista de ítems que ningún miembro haya visto
2. **SR Híbrido**: combinar los resultados del SRBC y el SRC en una única lista de recomendaciones
3. **Métricas de evaluación**: calcular Precisión, Recall, F1 y MAE usando el conjunto de test, solo para usuarios del dataset y para un único usuario a la vez