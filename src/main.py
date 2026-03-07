"""
Interfaz CLI del Sistema Recomendador de Películas.
"""

import sys
from pathlib import Path

import pandas as pd

from src.data import (
    NUM_GENRES, load_genres, load_profiles, save_profiles,
    preprocess, create_new_user_profile, PROCESSED_DIR, PROFILES_PATH,
    compute_preference_vector,
)
from src.content_based import recommend_content_based, select_top_preferences
from src.collaborative import (
    recommend_collaborative, compute_neighbors, compute_all_neighbors,
)


def load_catalog() -> pd.DataFrame:
    path = PROCESSED_DIR / "movie_catalog.csv"
    return pd.read_csv(path, sep=";")


def genre_names() -> dict[int, str]:
    """Devuelve {id_interno: nombre_español} para los 20 géneros."""
    g = load_genres()
    return dict(zip(g["id"], g["GeneroSP"]))


# ---------------------------------------------------------------------------
# Visualización de resultados
# ---------------------------------------------------------------------------

def display_recommendations(results: list[dict], technique: str):
    if not results:
        print("\n  No se encontraron recomendaciones.")
        return

    print(f"\n{'='*70}")
    print(f"  Recomendaciones ({technique}) — Top {len(results)}")
    print(f"{'='*70}")

    for i, r in enumerate(results, 1):
        stars = "★" * int(r["ratio"] / 20) + "☆" * (5 - int(r["ratio"] / 20))
        print(f"\n  {i}. {r.get('titulo', 'N/A')}")
        print(f"     Ratio de interés: {r['ratio']:.1f}/100  {stars}")
        print(f"     Puntuación media: {r.get('puntuacion_media', 'N/A')} "
              f"({r.get('votos', 0)} votos)")
        genres = r.get("generos_SP", [])
        if genres:
            print(f"     Géneros: {', '.join(genres)}")
        kw = r.get("keywords", [])
        if kw:
            print(f"     Keywords: {', '.join(kw[:6])}")
        imdb = r.get("imdbId", "")
        if imdb and str(imdb) != "nan":
            print(f"     IMDB: {imdb}")

    print(f"\n{'='*70}")


def display_user_profile(profile: dict, gnames: dict[int, str]):
    prefs = profile["preferences"]
    print(f"\n  Perfil del usuario {profile['id']}:")
    print(f"  Películas en histórico: {len(profile.get('history', {}))}")
    print(f"  Vecinos: {len(profile.get('neighbors', []))}")
    print(f"\n  Vector de preferencias (0-100):")
    for g in range(NUM_GENRES):
        if prefs[g] > 0:
            print(f"    {gnames.get(g, f'Género {g}'):20s}: {prefs[g]:5.1f}")


# ---------------------------------------------------------------------------
# Registro de nuevo usuario
# ---------------------------------------------------------------------------

def register_new_user(profiles: dict, catalog: pd.DataFrame) -> dict:
    """
    Registra un nuevo usuario pidiéndole sus preferencias por género.
    Escala 0-5 estrellas, se convierte a 0-100.
    """
    gnames = genre_names()

    # Determinar nuevo ID
    existing_ids = [p["id"] for p in profiles.values()]
    new_id = max(existing_ids) + 1 if existing_ids else 1

    print(f"\n  === Registro de nuevo usuario (ID: {new_id}) ===")
    print("  Indica tu interés en cada género (0-5 estrellas, 0 = sin interés):\n")

    preferences = [0.0] * NUM_GENRES

    for g in range(NUM_GENRES):
        while True:
            try:
                val = input(f"    {gnames.get(g, f'Género {g}'):20s} [0-5]: ").strip()
                val = float(val.replace(",", "."))
                if 0 <= val <= 5:
                    preferences[g] = round((val / 5.0) * 100, 1)
                    break
                print("      Introduce un valor entre 0 y 5.")
            except (ValueError, EOFError):
                print("      Valor no válido. Introduce un número entre 0 y 5.")

    profile = create_new_user_profile(new_id, preferences)

    # Calcular vecinos del nuevo usuario
    if profiles:
        neighbors = compute_neighbors(str(new_id), preferences, profiles)
        profile["neighbors"] = neighbors
        print(f"\n  Vecinos calculados: {len(neighbors)}")

    profiles[str(new_id)] = profile
    save_profiles(profiles)

    print(f"\n  Usuario {new_id} registrado correctamente.")
    display_user_profile(profile, gnames)

    return profile


# ---------------------------------------------------------------------------
# Menú principal
# ---------------------------------------------------------------------------

def select_user(profiles: dict, catalog: pd.DataFrame) -> dict | None:
    print("\n  === Selección de usuario ===")
    print("  1. Usuario existente del dataset")
    print("  2. Nuevo usuario (registro)")
    print("  0. Volver")

    choice = input("\n  Opción: ").strip()

    if choice == "1":
        uid = input("  ID de usuario (1-671): ").strip()
        if uid in profiles:
            return profiles[uid]
        else:
            print(f"  Usuario {uid} no encontrado.")
            return None
    elif choice == "2":
        return register_new_user(profiles, catalog)
    return None


def select_technique() -> str | None:
    print("\n  === Técnica de recomendación ===")
    print("  1. SR Basado en Contenido (SRBC)")
    print("  2. SR Colaborativo (SRC)")
    print("  3. SR Híbrido")
    print("  0. Volver")

    choice = input("\n  Opción: ").strip()
    return {"1": "SRBC", "2": "SRC", "3": "HIBRIDO"}.get(choice)


def ask_n_recommendations() -> int:
    while True:
        try:
            n = int(input("  Número de recomendaciones (1-50): ").strip())
            if 1 <= n <= 50:
                return n
        except ValueError:
            pass
        print("  Introduce un número entre 1 y 50.")


def run_recommendation(user_profile: dict, profiles: dict, catalog: pd.DataFrame):
    technique = select_technique()
    if technique is None:
        return

    n = ask_n_recommendations()

    if technique == "SRBC":
        results = recommend_content_based(user_profile, catalog, n=n)
        display_recommendations(results, "SR Basado en Contenido")

    elif technique == "SRC":
        if not user_profile.get("neighbors"):
            print("\n  El usuario no tiene vecinos calculados.")
            print("  Ejecute el preproceso de vecinos primero.")
            return
        results = recommend_collaborative(user_profile, profiles, catalog, n=n)
        display_recommendations(results, "SR Colaborativo")

    elif technique == "HIBRIDO":
        # Combinar SRBC y SRC
        results_cb = recommend_content_based(user_profile, catalog, n=n)
        results_cf = []
        if user_profile.get("neighbors"):
            results_cf = recommend_collaborative(user_profile, profiles, catalog, n=n)

        # Fusionar por movieId, promediando ratios
        combined: dict[int, dict] = {}
        for r in results_cb:
            mid = r["movieId"]
            combined[mid] = r.copy()
            combined[mid]["ratio_cb"] = r["ratio"]
            combined[mid]["ratio_cf"] = 0

        for r in results_cf:
            mid = r["movieId"]
            if mid in combined:
                combined[mid]["ratio_cf"] = r["ratio"]
            else:
                combined[mid] = r.copy()
                combined[mid]["ratio_cb"] = 0
                combined[mid]["ratio_cf"] = r["ratio"]

        # Ratio híbrido: 50% SRBC + 50% SRC
        for mid in combined:
            cb = combined[mid].get("ratio_cb", 0)
            cf = combined[mid].get("ratio_cf", 0)
            combined[mid]["ratio"] = round((cb + cf) / 2, 2)

        results = sorted(combined.values(), key=lambda x: x["ratio"], reverse=True)[:n]
        display_recommendations(results, "SR Híbrido (50% SRBC + 50% SRC)")


def main():
    print("\n" + "=" * 70)
    print("  SISTEMA RECOMENDADOR DE PELÍCULAS")
    print("=" * 70)

    # Comprobar si existen datos preprocesados
    if not PROFILES_PATH.exists():
        print("\n  No se encontraron datos preprocesados. Ejecutando preprocesado...")
        preprocess()

    print("\n  Cargando datos...")
    profiles = load_profiles()
    catalog = load_catalog()
    gnames = genre_names()
    print(f"  {len(profiles)} usuarios, {len(catalog)} películas")

    while True:
        print("\n  === Menú Principal ===")
        print("  1. Obtener recomendación")
        print("  2. Ver perfil de usuario")
        print("  3. Registrar nuevo usuario")
        print("  4. Preprocesar vecinos (SRC)")
        print("  5. Re-ejecutar preprocesado completo")
        print("  0. Salir")

        choice = input("\n  Opción: ").strip()

        if choice == "0":
            print("\n  ¡Hasta luego!")
            break

        elif choice == "1":
            user = select_user(profiles, catalog)
            if user:
                run_recommendation(user, profiles, catalog)

        elif choice == "2":
            uid = input("  ID de usuario: ").strip()
            if uid in profiles:
                display_user_profile(profiles[uid], gnames)
            else:
                print(f"  Usuario {uid} no encontrado.")

        elif choice == "3":
            register_new_user(profiles, catalog)

        elif choice == "4":
            print("\n  Calculando vecinos de todos los usuarios...")
            profiles = compute_all_neighbors(profiles)
            save_profiles(profiles)
            print("  Vecinos guardados.")

        elif choice == "5":
            preprocess()
            profiles = load_profiles()
            catalog = load_catalog()
            print("  Datos recargados.")

        else:
            print("  Opción no válida.")


if __name__ == "__main__":
    main()
