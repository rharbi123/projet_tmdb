import os
import time
import requests
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("TMDB_API_KEY")


def masquer_cle(url: str) -> str:
    return url.replace(API_KEY, "***")


def get_movie_details_q1(movie_id, max_retries=3, timeout=10):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={API_KEY}&language=fr-FR"

    for tentative in range(max_retries):
        try:
            response = requests.get(url, timeout=timeout)
        except requests.exceptions.RequestException as e:
            print(f"Erreur réseau : {e}. Pause... (Tentative {tentative + 1}/{max_retries})")
            time.sleep(2 ** tentative)
            continue

        if response.status_code == 200:
            data = response.json()
            return {
                "titre": data.get("title"),
                "date_sortie": data.get("release_date"),
            }

        elif response.status_code in [429, 500, 503]:
            print(f"Erreur {response.status_code}. Pause... (Tentative {tentative + 1}/{max_retries})")
            time.sleep(2 ** tentative)

        elif response.status_code in [400, 401, 403, 404]:
            print(f"Erreur {response.status_code} (requête invalide / non autorisée / introuvable). Arrêt.")
            return None

        else:
            print(f"Erreur inattendue {response.status_code}. Arrêt.")
            return None

    print(f"Échec après {max_retries} tentatives pour l'ID {movie_id}.")
    return None


if __name__ == "__main__":
    print("--- Résultat de la fonction robuste (Q1) ---")
    print(get_movie_details_q1(550))