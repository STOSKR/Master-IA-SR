# Trabajo 1: Aplicación SR

## Descripción del trabajo
- Grupos de 3 personas (excepcionalmente 4).
- Implementar un SR completo con interfaz gráfica, usando un dataset de películas.
- La aplicación debe ser una página web en funcionamiento hasta que salgan las notas.
- Lenguaje de programación y plataforma a elección del grupo.
- El resultado de la recomendación debe evaluarse mediante métricas.

## Criterios de evaluación
- **60%** Contenido del trabajo.
- **20%** Presentación y memoria.
- **20%** Coevaluación de los compañeros.
- La aplicación puntúa sobre 9. Para optar al 10, añadir al menos dos mejoras.

## Objetivo
- Los ítems a recomendar son películas del dataset.
- El objetivo es obtener una lista de películas adaptada a los gustos del usuario.
- Se calcula un ratio de interés del usuario en cada película y se recomiendan los de mayor ratio.

## Interfaz

### Selección inicial
Al iniciar, el usuario selecciona:
- Un usuario individual o un grupo.
- Tipo de recomendación: para usuario o para grupo.

### Recomendación para un grupo
- Seleccionar los componentes del grupo (solo usuarios registrados).

### Recomendación para un usuario
- **Usuario existente del dataset**: ya tiene perfil creado en el preproceso.
- **Nuevo usuario**: se registra, se le piden sus preferencias y se crea su perfil.

### Técnica de recomendación
Al acceder, seleccionar técnica:
- SR basado en contenido.
- SR colaborativo.
- SR híbrido.

### Resultado mostrado
- N ítems de mayor interés (N definido por la interfaz).
- Opcionales: carátulas, keywords, datos de IMDB, clasificación en taxonomía.
- Grado de seguridad/ratio/estrellas por ítem.

## Preferencias
Las preferencias son un vector de 20 posiciones (una por género) con el ratio de interés del usuario en ese género.

| Ejemplo ratio | 0 | 20 | 50 | 90 |
|---|---|---|---|---|
| Índice género  | 0 |  1 |  2 | 19 |

- **Usuarios del dataset**: inferidas de las películas puntuadas favorablemente.
- **Nuevo usuario**: se piden al registrarse (estrellas, barras, etc.); se almacenan en su perfil.

## Métricas de evaluación
- Métricas: Precisión, Recall, F1 y MAE.
- Solo para usuarios del dataset y para un único usuario.
- Dividir los ratings en: **entrenamiento** (70%) y **test** (30%).

## Presentación
- Mostrar el funcionamiento de la aplicación (vídeo, presentación o demo en directo).
- Explicar brevemente el código.
- Mostrar cómo cambia la recomendación para usuarios distintos y cómo se adapta al perfil.
