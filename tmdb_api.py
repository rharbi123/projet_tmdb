import os
import requests
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("TMDB_API_KEY")

def get_movie_details(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={API_KEY}&language=fr-FR"
    response = requests.get(url, timeout=10)
    
    if response.status_code != 200:
        return None
        
    data = response.json()
    return {
        "titre": data.get("title"),
        "date_sortie": data.get("release_date"),
        "genres": [genre["name"] for genre in data.get("genres", [])],
        "popularite": data.get("popularity"),
        "note_moyenne": data.get("vote_average"),
        "poster": data.get("poster_path") # Ajouté pour l'image
    }

def search_movie_by_name(nom):
    url = f"https://api.themoviedb.org/3/search/movie?api_key={API_KEY}&query={nom}&language=fr-FR"
    response = requests.get(url, timeout=10)
    
    if response.status_code != 200:
        return []
        
    data = response.json()
    # On renvoie les 5 premiers résultats
    resultats = []
    for film in data.get("results", [])[:5]:
        resultats.append({
            "id": film.get("id"),
            "titre": film.get("title"),
            "date_sortie": film.get("release_date"),
            "note_moyenne": film.get("vote_average"),
            "poster": film.get("poster_path")
        })
    return resultats

def get_movies_by_genre(genre_id):
    url = f"https://api.themoviedb.org/3/discover/movie?api_key={API_KEY}&with_genres={genre_id}&language=fr-FR&sort_by=popularity.desc"
    response = requests.get(url, timeout=10)
    
    if response.status_code != 200:
        return []
        
    data = response.json()
    resultats = []
    for film in data.get("results", [])[:10]: # On prend les 10 plus populaires
        resultats.append({
            "id": film.get("id"),
            "titre": film.get("title"),
            "date_sortie": film.get("release_date"),
            "note_moyenne": film.get("vote_average"),
            "poster": film.get("poster_path")
        })
    return resultats