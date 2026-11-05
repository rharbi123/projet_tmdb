import gzip
import json

# Nom du fichier téléchargé
fichier = "movie_ids_11_05_2026.json.gz"

print("--- Aperçu des 5 premières lignes ---")

# Ouvre le fichier compressé en lecture texte
with gzip.open(fichier, "rt", encoding="utf-8") as f:
    for i, ligne in enumerate(f):
        # Chaque ligne est un JSON indépendant
        objet = json.loads(ligne)
        print(objet)
        
        # On s'arrête après 5 lignes pour ne pas spammer la console
        if i == 4:
            break