# backend/recomendacion/recomendador.py
import os
import pickle
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from model import NLPModel
from posters import PosterFetcher
from tmdb import get_watch_providers 

class Recomendador:
    def __init__(self):
        # 1. Cargar CSV (Intenta cargar el enriquecido, si no el normal)
        if os.path.exists("data/movies_enriched.csv"):
            self.movies = pd.read_csv("data/movies_enriched.csv")
        else:
            # Fallback por si no encuentra el enriquecido
            self.movies = pd.read_csv("data/movies.csv")
            if "overview" not in self.movies.columns:
                self.movies["overview"] = ""

        self.nlp = NLPModel()
        self.poster_fetcher = PosterFetcher()

        # Preparamos el texto (Aunque carguemos embeddings, es bueno tener la columna lista)
        self.movies["semantic_text"] = (
            self.movies["title"].fillna("") + " " +
            self.movies["genres"].fillna("").str.replace("|", " ") + " " +
            self.movies["overview"].fillna("")
        )

        # 2. CARGA OPTIMIZADA DE EMBEDDINGS (Solución al error de memoria)
        pkl_path = "data/movie_embeddings.pkl"
        
        if os.path.exists(pkl_path):
            print("⚡ Cargando embeddings pre-calculados (Modo Rápido)...")
            with open(pkl_path, "rb") as f:
                self.movie_embeddings = pickle.load(f)
        else:
            print("⚠️ ADVERTENCIA: Calculando embeddings en vivo. Esto puede consumir mucha RAM.")
            self.movie_embeddings = self.nlp.encode(
                self.movies["semantic_text"].tolist()
            )
        
        print("Sistema listo.")

    def recomendar_por_texto(self, query, n=5):
        # 1. Convertir la consulta del usuario a números (embedding)
        query_embedding = self.nlp.encode(query)

        # 2. Calcular similitud con todas las películas
        similarities = cosine_similarity(
            query_embedding,
            self.movie_embeddings
        )[0]

        # 3. Obtener los índices de las mejores puntuaciones
        top_idx = np.argsort(similarities)[::-1][:n]

        results = []
        for i in top_idx:
            row = self.movies.iloc[i]
            title = row["title"]
            
            # A. Obtener datos visuales e ID de TMDB (Posters.py)
            movie_data = self.poster_fetcher.get_movie_data(title)
            tmdb_id = movie_data["tmdb_id"]
            
            # B. Obtener enlace de "dónde ver" si tenemos ID (Tmdb.py)
            watch_link = ""
            if tmdb_id:
                # Busca proveedores en México ('MX').
                providers_info = get_watch_providers(tmdb_id, country='MX')
                watch_link = providers_info.get('link', '') 

            # C. Priorizar la descripción del CSV si existe, sino usar la de TMDB
            overview = row.get("overview")
            if pd.isna(overview) or overview == "":
                overview = movie_data.get("overview", "")

            results.append({
                "movieId": int(row["movieId"]),
                "title": title,
                "genres": row["genres"],
                "score": float(similarities[i]),
                "poster_url": movie_data["poster_url"],
                "tmdb_id": tmdb_id,
                "watch_link": watch_link,
                "overview": overview
            })

        return results