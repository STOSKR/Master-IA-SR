# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is an academic project for the AIWR (Aplicaciones Inteligentes con Razonamiento y Búsqueda) course in the MUIARFID Master's program. It builds a **movie recommendation system** using the MovieLens dataset. All work lives in `proyecto.ipynb`.

## Running the Notebook

Open and run with Jupyter:
```bash
jupyter notebook proyecto.ipynb
```
Or with JupyterLab:
```bash
jupyter lab proyecto.ipynb
```

Cells must be run in order from top to bottom — later cells depend on variables built in earlier ones.

## Data Architecture

All CSVs are in `Data_set/` and use **semicolons as separators** (`sep=';'`) and **commas as decimals** (`decimal=','`).

### Source Tables

| File | Key | Notes |
|---|---|---|
| `peliculas.csv` | `id` → renamed to `movieId` | Up to 8 `id_genero` columns (wide format); remove duplicates on `id` |
| `ratings_small.csv` | `userId`, `movieId` | ~100k ratings (0.5–5 scale); 670 users |
| `ratings.csv` | same | Full dataset (~1M ratings) — not used by default |
| `generos.csv` | `IdDataset` | Maps numeric genre IDs to `Genero` (English) and `GeneroSP` (Spanish) |
| `keywords.csv` | `id` | Wide format: `contador` + hundreds of `kw_N` columns; requires renaming + melt |
| `links.csv` | `movieId` | Cross-reference to `imdbId` and `tmdbId`; remove duplicates on `movieId` |

`Data_set/Original/` contains the raw Kaggle source files (not used directly).

### ID Alignment

`peliculas.csv` uses column `id` while `ratings_small.csv` uses `movieId`. The notebook renames `peliculas.id → movieId` before joining. After the INNER JOIN on `movieId`, the working dataset covers **1,959 movies** and **670 users** (32,016 rating rows).

### Built DataFrame (`df`) — Rating-level

Each row is one user rating, enriched with:
- Movie metadata: `titulo`, `poster_path`, `puntuacion_media`, `votos`, `contgeneros`, `id_genero.*`
- `generos_SP`: Python list of Spanish genre names (derived from `generos.csv`)
- `imdbId`, `tmdbId` (left-joined from `links.csv`)
- `keywords_list`: Python list of keyword strings (left-joined after melting `keywords.csv`)

### Keywords Processing Pattern

`keywords.csv` arrives in wide format. Standard processing:
```python
n_kw_cols = len(keywords_raw.columns) - 2
keywords_raw.columns = ['id', 'contador'] + [f'kw_{i}' for i in range(n_kw_cols)]
kw_cols = [c for c in keywords_raw.columns if c.startswith('kw_')]
keywords_agg = (
    keywords_raw.melt(id_vars='id', value_vars=kw_cols, value_name='keyword')
    .dropna(subset=['keyword'])
    .groupby('id')['keyword'].apply(list)
    .reset_index()
    .rename(columns={'id': 'movieId', 'keyword': 'keywords_list'})
)
```

## Work in Progress

The notebook notes indicate these components are still to be built:
- **User table**: per-user preference scores by genre
- **Recommendation algorithms**: collaborative filtering (and possibly content-based)

## PDF References

- `1._Aplicaci_n/Trabajo_1._Aplicaci_n.pdf` — assignment spec for the application part
- `2._Datos_base/Trabajo_2._Datos_base.pdf` and `.pptx` — assignment spec for the database/data part
