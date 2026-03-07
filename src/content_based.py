"""
SR Basado en Contenido (SRBC).

Recomienda películas que coinciden con las preferencias más altas del usuario.
"""

import ast

import numpy as np
import pandas as pd

TOP_PREFS_MIN = 5
TOP_PREFS_MAX = 8
LOW_THRESHOLD_RATIO = 0.4   # descartamos preferencias < 40% del máximo seleccionado
VOTE_CONFIDENCE_BASE = 1000  # votos para confianza plena en puntuacion_media


def select_top_preferences(preferences: list[float],
                           min_prefs: int = TOP_PREFS_MIN,
                           max_prefs: int = TOP_PREFS_MAX) -> list[float]:
    """
    Selecciona las 5-8 preferencias de mayor ratio del perfil.
    Descarta las que estén por debajo del umbral relativo (40% del máximo
    entre las seleccionadas). No modifica el vector original.
    """
    indexed = sorted(enumerate(preferences), key=lambda x: x[1], reverse=True)

    # Tomar las top max_prefs con valor > 0
    candidates = [(i, v) for i, v in indexed if v > 0][:max_prefs]

    if not candidates:
        return [0.0] * len(preferences)

    max_val = candidates[0][1]
    threshold = max_val * LOW_THRESHOLD_RATIO

    # Filtrar por umbral, manteniendo al menos min_prefs si es posible
    filtered = [(i, v) for i, v in candidates if v >= threshold]
    if len(filtered) < min_prefs:
        filtered = candidates[:min_prefs]

    # Construir nuevo vector filtrado
    selected = [0.0] * len(preferences)
    for i, v in filtered:
        selected[i] = v
    return selected


def _parse_list_column(val):
    """Parsea una columna que puede ser string repr de lista o ya lista."""
    if isinstance(val, list):
        return val
    if isinstance(val, str):
        try:
            return ast.literal_eval(val)
        except (ValueError, SyntaxError):
            return []
    return []


def compute_item_ratio(selected_prefs: list[float], movie_genres: list[int],
                       puntuacion_media: float, votos: int) -> float:
    """
    Calcula el ratio de interés de un ítem para el usuario.

    Componentes:
    - Preferencia media de los géneros coincidentes (50%)
    - Puntuación media del ítem ponderada por confianza de votos (30%)
    - Proporción de géneros del ítem que coinciden con preferencias (20%)
    """
    if not movie_genres:
        return 0.0

    # Preferencias coincidentes con los géneros de la película
    matching = [selected_prefs[g] for g in movie_genres if g < len(selected_prefs) and selected_prefs[g] > 0]

    if not matching:
        return 0.0

    avg_pref = np.mean(matching)
    match_ratio = len(matching) / len(movie_genres)

    # Puntuación media normalizada a 0-100
    quality = puntuacion_media * 10

    # Confianza basada en votos (logarítmica)
    vote_conf = min(1.0, np.log1p(votos) / np.log1p(VOTE_CONFIDENCE_BASE))

    ratio = avg_pref * 0.5 + quality * vote_conf * 0.3 + match_ratio * 100 * 0.2
    return round(ratio, 2)


def recommend_content_based(user_profile: dict, catalog: pd.DataFrame,
                            n: int = 10) -> list[dict]:
    """
    Genera recomendaciones basadas en contenido para un usuario.

    1. Selecciona sub-vector de preferencias (5-8 de mayor ratio).
    2. Obtiene movies clasificadas en alguna preferencia seleccionada.
    3. Elimina películas ya vistas (histórico).
    4. Calcula ratio de interés por ítem.
    5. Ordena y devuelve los N mejores.
    """
    preferences = user_profile["preferences"]
    history = set(user_profile.get("history", {}).keys())

    # 1. Sub-vector de preferencias
    selected = select_top_preferences(preferences)
    selected_genre_ids = {i for i, v in enumerate(selected) if v > 0}

    if not selected_genre_ids:
        return []

    # Preparar catálogo
    df = catalog.copy()
    df["generos_internos"] = df["generos_internos"].apply(_parse_list_column)
    df["keywords_list"] = df["keywords_list"].apply(
        lambda x: _parse_list_column(x) if isinstance(x, (str, list)) else []
    )

    # 2. Filtrar películas que tengan al menos un género seleccionado
    df = df[df["generos_internos"].apply(
        lambda gs: any(g in selected_genre_ids for g in gs)
    )]

    # 3. Eliminar películas ya vistas
    df = df[~df["movieId"].astype(str).isin(history)]

    if df.empty:
        return []

    # 4. Calcular ratio de interés
    df = df.copy()
    df["ratio"] = df.apply(
        lambda row: compute_item_ratio(
            selected, row["generos_internos"],
            float(row.get("puntuacion_media", 0)),
            int(row.get("votos", 0)),
        ),
        axis=1,
    )

    # 5. Ordenar y devolver top N
    df = df.sort_values("ratio", ascending=False).head(n)

    results = []
    for _, row in df.iterrows():
        results.append({
            "movieId": int(row["movieId"]),
            "titulo": row.get("titulo", ""),
            "ratio": row["ratio"],
            "puntuacion_media": row.get("puntuacion_media", 0),
            "votos": int(row.get("votos", 0)),
            "generos_SP": _parse_list_column(row.get("generos_SP", [])),
            "generos_internos": row["generos_internos"],
            "keywords": row.get("keywords_list", []),
            "poster_path": row.get("poster_path", ""),
            "imdbId": row.get("imdbId", ""),
        })

    return results
