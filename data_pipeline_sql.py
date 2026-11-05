import gzip
import json
import pandas as pd
from sqlalchemy import create_engine

fichier = "movie_ids_11_05_2026.json.gz"

print("Lecture du fichier...")
data = []
with gzip.open(fichier, "rt", encoding="utf-8") as f:
    for ligne in f:
        data.append(json.loads(ligne))

df = pd.DataFrame(data)
print(f"{len(df)} lignes chargées.")

# Création de la base SQLite (fichier tmdb.db)
engine = create_engine("sqlite:///tmdb.db")

print("Injection dans la table 'movies'...")
df.to_sql("movies", engine, if_exists="replace", index=False)

print("Injection terminée. Table 'movies' créée dans tmdb.db.")