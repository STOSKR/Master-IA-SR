"""
SR Colaborativo (SRC).

Busca usuarios similares (vecinos) mediante correlación de Pearson sobre el
vector completo de preferencias y recomienda ítems valorados favorablemente
por los vecinos, ponderados por afinidad.
"""

import ast

import numpy as np
import pandas as pd

from src.data import NUM_GENRES, FAVORABLE_THRESHOLD

NUM_NEIGHBORS = 50


def _pearson_correlation(v1: list[float], v2: list[float]) -> float:
    """Calcula el coeficiente de correlación de Pearson entre dos vectores."""
    a = np.array(v1, dtype=float)
    b = np.array(v2, dtype=float)

    if np.std(a) < 1e-10 or np.std(b) < 1e-10:
        return 0.0

    corr = np.corrcoef(a, b)[0, 1]
    if np.isnan(corr):
        return 0.0
    return float(corr)


def pearson_to_affinity(pearson: float) -> float:
    """Convierte Pearson [-1,1] a afinidad [0,100]."""
    return round((pearson + 1) * 50, 2)


def compute_neighbors(user_id: str, user_prefs: list[float],
                      all_profiles: dict, n_neighbors: int = NUM_NEIGHBORS) -> list[list]:
    """
    Calcula los vecinos de un usuario usando correlación de Pearson
    sobre el vector completo de preferencias (20 géneros).
    Devuelve los n_neighbors de mayor afinidad como [[vecino_id, afinidad], ...].
    """
    similarities = []
    for other_id, other_profile in all_profiles.items():
        if str(other_id) == str(user_id):
            continue
        pearson = _pearson_correlation(user_prefs, other_profile["preferences"])
        affinity = pearson_to_affinity(pearson)
        similarities.append([str(other_id), affinity])

    # Ordenar por afinidad descendente y tomar los top n
    similarities.sort(key=lambda x: x[1], reverse=True)
    return similarities[:n_neighbors]


def compute_all_neighbors(profiles: dict, n_neighbors: int = NUM_NEIGHBORS) -> dict:
    """
    Preproceso: calcula los vecinos de todos los usuarios del dataset.
    Almacena los 40-50 vecinos de mayor afinidad en cada perfil.
    """
    print("  Calculando vecinos para todos los usuarios...")

    # Construir matriz de preferencias para eficiencia
    user_ids = list(profiles.keys())
    n_users = len(user_ids)
    pref_matrix = np.array([profiles[uid]["preferences"] for uid in user_ids])

    # Calcular matriz de correlación de Pearson
    # Normalizar filas (restar media, dividir por std)
    means = pref_matrix.mean(axis=1, keepdims=True)
    stds = pref_matrix.std(axis=1, keepdims=True)
    stds[stds < 1e-10] = 1  # evitar división por cero
    normalized = (pref_matrix - means) / stds

    # Matriz de correlación: (normalized @ normalized.T) / n_cols
    corr_matrix = (normalized @ normalized.T) / pref_matrix.shape[1]

    # Para cada usuario, obtener los top-N vecinos
    for i, uid in enumerate(user_ids):
        correlations = corr_matrix[i]
        # Poner -inf para uno mismo
        correlations[i] = -np.inf

        # Índices de mayor correlación
        top_indices = np.argsort(correlations)[::-1][:n_neighbors]

        neighbors = []
        for j in top_indices:
            affinity = pearson_to_affinity(float(correlations[j]))
            neighbors.append([user_ids[j], affinity])

        profiles[uid]["neighbors"] = neighbors

    print(f"  Vecinos calculados para {n_users} usuarios")
    return profiles


def _parse_list_column(val):
    if isinstance(val, list):
        return val
    if isinstance(val, str):
        try:
            return ast.literal_eval(val)
        except (ValueError, SyntaxError):
            return []
    return []


def recommend_collaborative(user_profile: dict, all_profiles: dict,
                            catalog: pd.DataFrame, n: int = 10) -> list[dict]:
    """
    Genera recomendaciones colaborativas para un usuario.

    1. Obtiene los vecinos del usuario.
    2. Para cada vecino, recoge ítems puntuados favorablemente.
    3. Elimina ítems ya vistos por el usuario.
    4. Combina ratios ponderados por afinidad:
       ru_i = sum(afinidad * rating_vecino) / sum(|afinidad|)
    5. Ordena y devuelve top N.
    """
    neighbors = user_profile.get("neighbors", [])
    if not neighbors:
        return []

    history = set(user_profile.get("history", {}).keys())

    # Recoger ítems de vecinos
    # {movieId_str: [(affinity, rating), ...]}
    item_scores: dict[str, list[tuple[float, float]]] = {}

    for neighbor_id, affinity in neighbors:
        if affinity <= 50:  # solo vecinos con afinidad positiva (Pearson > 0)
            continue
        neighbor = all_profiles.get(str(neighbor_id))
        if neighbor is None:
            continue

        for movie_id_str, rating in neighbor["history"].items():
            if rating < FAVORABLE_THRESHOLD:
                continue
            if movie_id_str in history:
                continue
            if movie_id_str not in item_scores:
                item_scores[movie_id_str] = []
            item_scores[movie_id_str].append((affinity, rating))

    if not item_scores:
        return []

    # Calcular ratio ponderado para cada ítem
    recommendations = []
    for movie_id_str, scores in item_scores.items():
        numerator = sum(aff * rat for aff, rat in scores)
        denominator = sum(abs(aff) for aff, _ in scores)
        if denominator == 0:
            continue
        weighted_rating = numerator / denominator  # escala 0.5-5
        # Convertir a 0-100
        ratio = round((weighted_rating / 5.0) * 100, 2)
        recommendations.append((movie_id_str, ratio))

    # Ordenar por ratio descendente
    recommendations.sort(key=lambda x: x[1], reverse=True)
    top_n = recommendations[:n]

    # Enriquecer con datos del catálogo
    df = catalog.copy()
    df["movieId_str"] = df["movieId"].astype(str)
    df = df.set_index("movieId_str")

    results = []
    for movie_id_str, ratio in top_n:
        if movie_id_str in df.index:
            row = df.loc[movie_id_str]
            results.append({
                "movieId": int(movie_id_str),
                "titulo": row.get("titulo", ""),
                "ratio": ratio,
                "puntuacion_media": row.get("puntuacion_media", 0),
                "votos": int(row.get("votos", 0)),
                "generos_SP": _parse_list_column(row.get("generos_SP", [])),
                "generos_internos": _parse_list_column(row.get("generos_internos", [])),
                "keywords": _parse_list_column(row.get("keywords_list", [])) if pd.notna(row.get("keywords_list")) else [],
                "poster_path": row.get("poster_path", ""),
                "imdbId": row.get("imdbId", ""),
            })
        else:
            results.append({
                "movieId": int(movie_id_str),
                "titulo": "Desconocida",
                "ratio": ratio,
            })

    return results
