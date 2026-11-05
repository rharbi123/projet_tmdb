import os
import gzip
import json
import time
import requests
import pandas as pd
import schedule
from datetime import date
from sqlalchemy import create_engine

def mettre_a_jour():
    print("\n--- Début de la mise à jour ---")
    today = date.today().strftime("%m_%d_%Y")
    nom_fichier = f"movie_ids_{today}.json.gz"
    url = f"https://files.tmdb.org/p/exports/{nom_fichier}"

    print(f"Téléchargement de : {url}")
    reponse = requests.get(url, stream=True)

    if reponse.status_code == 200:
        with open(nom_fichier, "wb") as f:
            for chunk in reponse.iter_content(chunk_size=8192):
                f.write(chunk)
        print(f"Fichier {nom_fichier} téléchargé.")

        print("Lecture du fichier...")
        data = []
        with gzip.open(nom_fichier, "rt", encoding="utf-8") as f:
            for ligne in f:
                data.append(json.loads(ligne))
                
        df = pd.DataFrame(data)
        print(f"{len(df)} lignes chargées.")

        engine = create_engine("sqlite:///tmdb.db")
        print("Mise à jour de la table 'movies'...")
        df.to_sql("movies", engine, if_exists="replace", index=False)
        print("Mise à jour terminée avec succès.")
    else:
        print(f"Erreur (Statut {reponse.status_code}). Le fichier du jour n'est peut-être pas encore disponible.")
    print("--- Fin de la mise à jour ---")

# Lancer une première fois au démarrage
mettre_a_jour()

# Planifier la prochaine mise à jour dans 90 jours (environ 3 mois)
schedule.every(90).days.do(mettre_a_jour)

print("\nScript en attente. Prochaine mise à jour dans 90 jours (laisser le terminal ouvert).")

# Boucle pour maintenir le script en vie
while True:
    schedule.run_pending()
    time.sleep(60) # Vérifie toutes les minutes si c'est l'heure