"""
Carga de datos, preprocesado, división train/test y gestión de perfiles de usuario.
"""

import json
from pathlib import Path

import numpy as np
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent.parent
RAW_DIR = BASE_DIR / "data" / "raw"
PROCESSED_DIR = BASE_DIR / "data" / "processed"
PROFILES_PATH = PROCESSED_DIR / "user_profiles.json"

NUM_GENRES = 20
FAVORABLE_THRESHOLD = 3.0   # rating >= 3.0 en escala 0.5-5 se considera favorable
CONFIDENCE_N = 5            # nº mínimo de películas favorables para confianza plena


# ---------------------------------------------------------------------------
# Carga de datos crudos
# ---------------------------------------------------------------------------

def load_genres() -> pd.DataFrame:
    return pd.read_csv(RAW_DIR / "generos.csv", sep=";")


def load_movies() -> pd.DataFrame:
    """Carga peliculas.csv, elimina duplicados y construye listas de géneros internos."""
    df = pd.read_csv(RAW_DIR / "peliculas.csv", sep=";", decimal=",")
    df = df.drop_duplicates(subset=["id"])

    generos = load_genres()
    ds_to_internal = generos.set_index("IdDataset")["id"].to_dict()
    ds_to_spanish = generos.set_index("IdDataset")["GeneroSP"].to_dict()

    gen_cols = [c for c in df.columns if "id_genero" in c]
    df[gen_cols] = df[gen_cols].apply(pd.to_numeric, errors="coerce")

    df["generos_internos"] = df[gen_cols].apply(
        lambda row: [int(ds_to_internal[v]) for v in row if pd.notna(v) and v in ds_to_internal],
        axis=1,
    )
    df["generos_SP"] = df[gen_cols].apply(
        lambda row: [ds_to_spanish[v] for v in row if pd.notna(v) and v in ds_to_spanish],
        axis=1,
    )

    df = df.drop(columns=gen_cols).rename(columns={"id": "movieId"})
    return df


def load_ratings() -> pd.DataFrame:
    return pd.read_csv(RAW_DIR / "ratings_small.csv", sep=";", decimal=",")


def load_keywords() -> pd.DataFrame:
    kw_raw = pd.read_csv(RAW_DIR / "keywords.csv", sep=";", low_memory=False)
    n_kw = len(kw_raw.columns) - 2
    kw_raw.columns = ["id", "contador"] + [f"kw_{i}" for i in range(n_kw)]
    kw_cols = [c for c in kw_raw.columns if c.startswith("kw_")]
    return (
        kw_raw.melt(id_vars="id", value_vars=kw_cols, value_name="keyword")
        .dropna(subset=["keyword"])
        .groupby("id")["keyword"]
        .apply(list)
        .reset_index()
        .rename(columns={"id": "movieId", "keyword": "keywords_list"})
    )


def load_links() -> pd.DataFrame:
    df = pd.read_csv(RAW_DIR / "links.csv", sep=";")
    return df.drop_duplicates(subset=["movieId"])


# ---------------------------------------------------------------------------
# Validación y filtrado
# ---------------------------------------------------------------------------

def filter_ratings_to_valid_movies(ratings: pd.DataFrame, movies: pd.DataFrame) -> pd.DataFrame:
    """Elimina ratings que referencien películas inexistentes en peliculas.csv."""
    valid_ids = set(movies["movieId"].values)
    before = len(ratings)
    ratings = ratings[ratings["movieId"].isin(valid_ids)].copy()
    removed = before - len(ratings)
    if removed > 0:
        print(f"  Eliminados {removed} ratings de películas inexistentes")
    return ratings


# ---------------------------------------------------------------------------
# División train / test
# ---------------------------------------------------------------------------

def train_test_split(ratings: pd.DataFrame, train_ratio: float = 0.7, seed: int = 42):
    """Divide los ratings en train y test con mezcla aleatoria."""
    shuffled = ratings.sample(frac=1, random_state=seed).reset_index(drop=True)
    split_idx = int(len(shuffled) * train_ratio)
    train = shuffled.iloc[:split_idx].reset_index(drop=True)
    test = shuffled.iloc[split_idx:].reset_index(drop=True)
    return train, test


# ---------------------------------------------------------------------------
# Vector de preferencias del usuario
# ---------------------------------------------------------------------------

def compute_preference_vector(user_ratings: pd.DataFrame, movies: pd.DataFrame) -> list[float]:
    """
    Calcula el vector de preferencias (20 géneros, escala 0-100) a partir de las
    películas puntuadas favorablemente (rating >= 3.0) en el set de entrenamiento.

    Fórmula por género g:
        mean_scaled = media(rating / 5 * 100) de las películas favorables en g
        confidence  = min(1, n_favorable / CONFIDENCE_N)
        preferencia[g] = mean_scaled * confidence

    Así se tiene en cuenta tanto la puntuación dada como el nº de películas.
    """
    preferences = [0.0] * NUM_GENRES

    favorable = user_ratings[user_ratings["rating"] >= FAVORABLE_THRESHOLD]
    if favorable.empty:
        return preferences

    movie_genres = dict(zip(movies["movieId"], movies["generos_internos"]))

    genre_ratings: dict[int, list[float]] = {g: [] for g in range(NUM_GENRES)}
    for _, row in favorable.iterrows():
        genres = movie_genres.get(row["movieId"], [])
        if isinstance(genres, list):
            for g in genres:
                genre_ratings[g].append(row["rating"])

    for g in range(NUM_GENRES):
        if genre_ratings[g]:
            mean_scaled = (np.mean(genre_ratings[g]) / 5.0) * 100
            confidence = min(1.0, len(genre_ratings[g]) / CONFIDENCE_N)
            preferences[g] = round(mean_scaled * confidence, 1)

    return preferences


# ---------------------------------------------------------------------------
# Perfiles de usuario
# ---------------------------------------------------------------------------

def build_user_profiles(train: pd.DataFrame, movies: pd.DataFrame) -> dict:
    """
    Crea un perfil por cada usuario del dataset a partir del train:
    - preferences: vector de 20 posiciones (0-100)
    - history: {movieId_str: rating} con las películas del train
    - neighbors: lista vacía (se rellena en sesión 3)
    """
    profiles: dict = {}
    user_ids = sorted(train["userId"].unique())

    for uid in user_ids:
        user_train = train[train["userId"] == uid]
        preferences = compute_preference_vector(user_train, movies)
        history = {
            str(int(row["movieId"])): float(row["rating"])
            for _, row in user_train.iterrows()
        }
        profiles[str(uid)] = {
            "id": int(uid),
            "preferences": preferences,
            "history": history,
            "neighbors": [],
        }

    return profiles


def create_new_user_profile(user_id: int, preferences: list[float]) -> dict:
    """Crea un perfil para un usuario nuevo (sin histórico)."""
    return {
        "id": user_id,
        "preferences": preferences,
        "history": {},
        "neighbors": [],
    }


# ---------------------------------------------------------------------------
# Persistencia
# ---------------------------------------------------------------------------

def save_profiles(profiles: dict, path: Path | None = None):
    if path is None:
        path = PROFILES_PATH
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w") as f:
        json.dump(profiles, f, indent=2)


def load_profiles(path: Path | None = None) -> dict:
    if path is None:
        path = PROFILES_PATH
    with open(path) as f:
        return json.load(f)


def build_movie_catalog(movies: pd.DataFrame, keywords: pd.DataFrame,
                        links: pd.DataFrame) -> pd.DataFrame:
    """Construye catálogo consolidado de películas."""
    catalog = movies.merge(keywords, on="movieId", how="left")
    catalog = catalog.merge(links[["movieId", "imdbId", "tmdbId"]], on="movieId", how="left")
    return catalog


# ---------------------------------------------------------------------------
# Pipeline completo
# ---------------------------------------------------------------------------

def preprocess():
    """Ejecuta el pipeline completo de preprocesado."""
    print("=== Pipeline de preprocesado ===\n")

    print("1. Cargando datos crudos...")
    movies = load_movies()
    ratings = load_ratings()
    keywords = load_keywords()
    links = load_links()
    generos = load_genres()
    print(f"   Películas: {len(movies)}, Ratings: {len(ratings)}")

    print("\n2. Filtrando ratings a películas válidas...")
    ratings = filter_ratings_to_valid_movies(ratings, movies)
    print(f"   Ratings válidos: {len(ratings)}, Usuarios: {ratings['userId'].nunique()}")

    print("\n3. Dividiendo en train (70%) / test (30%) con shuffle...")
    train, test = train_test_split(ratings)
    print(f"   Train: {len(train)}, Test: {len(test)}")

    print("\n4. Construyendo catálogo de películas...")
    catalog = build_movie_catalog(movies, keywords, links)
    print(f"   Catálogo: {len(catalog)} películas")

    print("\n5. Construyendo perfiles de usuario...")
    profiles = build_user_profiles(train, movies)
    print(f"   Perfiles: {len(profiles)} usuarios")

    # Guardar
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    train.to_csv(PROCESSED_DIR / "train.csv", index=False, sep=";", decimal=",")
    test.to_csv(PROCESSED_DIR / "test.csv", index=False, sep=";", decimal=",")
    catalog.to_csv(PROCESSED_DIR / "movie_catalog.csv", index=False, sep=";")
    generos.to_csv(PROCESSED_DIR / "generos.csv", index=False, sep=";")
    save_profiles(profiles)

    print("\n=== Preprocesado completado ===")
    return movies, ratings, train, test, catalog, profiles


if __name__ == "__main__":
    preprocess()
