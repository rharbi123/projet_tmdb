import gzip
import json
import pandas as pd

fichier = "movie_ids_11_05_2026.json.gz"

print("Lecture du fichier ligne par ligne...")

# On lit chaque ligne du .gz et on la transforme en dictionnaire Python
data = []
with gzip.open(fichier, "rt", encoding="utf-8") as f:
    for ligne in f:
        data.append(json.loads(ligne))

# On crée le DataFrame à partir de la liste
df = pd.DataFrame(data)

print("\n--- Aperçu du DataFrame ---")
print(df.head())

print(f"\nNombre total de lignes : {len(df)}")
print(f"Colonnes : {df.columns.tolist()}")