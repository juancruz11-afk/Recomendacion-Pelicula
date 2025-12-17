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
        # 1. Cargar CSV
        if os.path.exists("data/movies_enriched.csv"):
            self.movies = pd.read_csv("data/movies_enriched.csv")
        else:
            self.movies = pd.read_csv("data/movies.csv")
            if "overview" not in self.movies.columns:
                self.movies["overview"] = ""

        # NO cargamos el modelo aquí (Lazy Loading)
        self.nlp = None 
        
        self.poster_fetcher = PosterFetcher()

        # Preparar textos
        self.movies["semantic_text"] = (
            self.movies["title"].fillna("") + " " +
            self.movies["genres"].fillna("").str.replace("|", " ") + " " +
            self.movies["overview"].fillna("")
        )

        # 2. CARGA DE EMBEDDINGS (Solo datos, no modelo)
        pkl_path = "data/movie_embeddings.pkl"
        
        if os.path.exists(pkl_path):
            print("⚡ Cargando embeddings pre-calculados...")
            with open(pkl_path, "rb") as f:
                self.movie_embeddings = pickle.load(f)
        else:
            print("⚠️ ADVERTENCIA: No se encontró el archivo .pkl. El sistema podría fallar por memoria.")
            self.movie_embeddings = None
        
        print("Sistema iniciado (Modelo en espera).")

    def _cargar_modelo_si_es_necesario(self):
        """Carga el modelo de IA solo si no está cargado aún"""
        if self.nlp is None:
            print("⏳ Cargando modelo de IA por primera vez...")
            self.nlp = NLPModel()
            
            # Si no había archivo .pkl, calculamos los embeddings ahora (Plan B)
            if self.movie_embeddings is None:
                print("Calculando embeddings en vivo...")
                self.movie_embeddings = self.nlp.encode(
                    self.movies["semantic_text"].tolist()
                )

    def recomendar_por_texto(self, query, n=5):
        # 1. Asegurar que el modelo esté cargado
        self._cargar_modelo_si_es_necesario()

        # 2. Convertir la consulta del usuario a números
        query_embedding = self.nlp.encode(query)

        # 3. Calcular similitud
        similarities = cosine_similarity(
            query_embedding,
            self.movie_embeddings
        )[0]

        top_idx = np.argsort(similarities)[::-1][:n]

        results = []
        for i in top_idx:
            row = self.movies.iloc[i]
            title = row["title"]
            
            movie_data = self.poster_fetcher.get_movie_data(title)
            tmdb_id = movie_data["tmdb_id"]
            
            watch_link = ""
            if tmdb_id:
                providers_info = get_watch_providers(tmdb_id, country='MX')
                watch_link = providers_info.get('link', '') 

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