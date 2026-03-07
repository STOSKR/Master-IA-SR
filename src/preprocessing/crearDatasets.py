"""
Genera en data/processed/:
  - ratings_enriquecidos.csv  (rating-level, con toda la info de película)
  - peliculas.csv             (una fila por película, géneros como lista)
  - usuarios.csv              (una fila por usuario, media de rating por género)
"""

from pathlib import Path
import pandas as pd

DATA_DIR = Path("data/raw")
OUT_DIR = Path("data/processed")
OUT_DIR.mkdir(exist_ok=True)

generos_df = pd.read_csv(DATA_DIR / "generos.csv", sep=";")
links_df = pd.read_csv(DATA_DIR / "links.csv", sep=";")
peliculas_df = pd.read_csv(DATA_DIR / "peliculas.csv", sep=";", decimal=",")
ratings_df = pd.read_csv(DATA_DIR / "ratings_small.csv", sep=";", decimal=",")
keywords_raw = pd.read_csv(DATA_DIR / "keywords.csv", sep=";", low_memory=False)

peliculas_df = peliculas_df.drop_duplicates(subset=["id"])
links_df = links_df.drop_duplicates(subset=["movieId"])
links_df["tmdbId"] = pd.to_numeric(links_df["tmdbId"], errors='coerce').astype('Int64')

dataset_to_internal = generos_df.set_index("IdDataset")["id"].to_dict()
dataset_to_spanish = generos_df.set_index("IdDataset")["GeneroSP"].to_dict()

GEN_COLS = [c for c in peliculas_df.columns if "id_genero" in c]
peliculas_df[GEN_COLS] = peliculas_df[GEN_COLS].apply(pd.to_numeric, errors="coerce").astype("Int64")

# Colapsar columnas id_genero* en una sola lista
peliculas_out = peliculas_df.drop(columns=GEN_COLS).copy()
peliculas_out["generos"] = peliculas_df[GEN_COLS].apply(
    lambda row: [int(v) for v in row if pd.notna(v)],
    axis=1,
)
peliculas_out.to_csv(OUT_DIR / "peliculas.csv", index=False, sep=";")
print(f"[OK] peliculas.csv          -> {peliculas_out.shape}")

# Preparar columnas derivadas de géneros en peliculas (para el join)
peliculas_df["generos_SP"] = peliculas_df[GEN_COLS].apply(
    lambda row: [
        dataset_to_spanish[v] for v in row if pd.notna(v) and v in dataset_to_spanish
    ],
    axis=1,
)
peliculas_df["generos_internos"] = peliculas_df[GEN_COLS].apply(
    lambda row: [
        int(dataset_to_internal[v])
        for v in row
        if pd.notna(v) and v in dataset_to_internal
    ],
    axis=1,
)
peliculas_df = peliculas_df.rename(columns={"id": "movieId"})

# Add keywords por película
n_kw_cols = len(keywords_raw.columns) - 2
keywords_raw.columns = ["id", "contador"] + [f"kw_{i}" for i in range(n_kw_cols)]
kw_cols = [c for c in keywords_raw.columns if c.startswith("kw_")]

keywords_agg = (
    keywords_raw.melt(id_vars="id", value_vars=kw_cols, value_name="keyword")
    .dropna(subset=["keyword"])
    .groupby("id")["keyword"]
    .apply(list)
    .reset_index()
    .rename(columns={"id": "movieId", "keyword": "keywords_list"})
)

# Tabla RATINGS_ENRIQUECIDOS
ratings_enr = (
    ratings_df.merge(peliculas_df, on="movieId", how="inner")
    .merge(links_df[["movieId", "imdbId", "tmdbId"]], on="movieId", how="left")
    .merge(keywords_agg, on="movieId", how="left")
)

ratings_enr.to_csv(OUT_DIR / "ratings_enriquecidos.csv", index=False, sep=";")
print(f"[OK] ratings_enriquecidos.csv -> {ratings_enr.shape}")

# Tabla USUARIOS
# Explotar por género interno (0-19) para obtener una fila por (usuario, género)
ratings_exp = (
    ratings_enr[["userId", "rating", "generos_internos"]]
    .explode("generos_internos")
    .dropna(subset=["generos_internos"])
)
ratings_exp["generos_internos"] = ratings_exp["generos_internos"].astype(int)

# Media de rating por usuario y género
user_genre = (
    ratings_exp.groupby(["userId", "generos_internos"])["rating"]
    .mean()
    .unstack(level="generos_internos")
)

# Garantizar las 20 columnas (0-19) aunque un género no tenga ratings
all_genres = list(range(20))
user_genre = user_genre.reindex(columns=all_genres)

# Añadir id y renombrar userId
usuarios_out = user_genre.reset_index().rename(columns={"userId": "id_usu"})
usuarios_out.insert(0, "id", range(len(usuarios_out)))

usuarios_out.to_csv(OUT_DIR / "usuarios.csv", index=False, sep=";")
print(f"[OK] usuarios.csv           -> {usuarios_out.shape}")
