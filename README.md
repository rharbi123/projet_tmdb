# 🎬 Projet TMDB - API & Data Pipeline

Ce projet a été réalisé dans le cadre du Mini Projet. Il interagit avec l'API de The Movie Database (TMDB) pour récupérer des informations sur les films, gérer les erreurs, optimiser les requêtes avec du cache, et stocker les données dans une base SQL.

## 🚀 Fonctionnalités

- **Requêtes API robustes (Q1)** : Gestion des erreurs (429, 500, 503), tentatives (retry) et pauses (timeout).
- **Haute performance (Q2)** : Utilisation de `asyncio` et `aiohttp` pour exécuter des requêtes en parallèle.
- **Cache avancé (Q3)** : Mise en cache des résultats pendant 1 heure avec protection contre les "race conditions" (`asyncio.Lock`).
- **Data Pipeline** : Téléchargement, décompression et lecture du fichier `.gz` quotidien de TMDB (1.2M de lignes).
- **Base de données** : Injection des données dans une base SQLite (`tmdb.db`).
- **Mise à jour automatisée** : Script planifiant la mise à jour de la base tous les 90 jours.
- **Interface Streamlit** : Application web avec recherche par ID, Nom (avec autocomplétion locale) et Genre.