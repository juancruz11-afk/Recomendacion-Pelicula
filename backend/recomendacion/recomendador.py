# backend/recomendacion/recomendador.py
from model import NLPModel
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
import numpy as np
from posters import PosterFetcher
from tmdb import get_watch_providers # Importamos la función de proveedores

class Recomendador:
    def __init__(self):
        # Cargamos los datos
        self.movies = pd.read_csv("data/movies_enriched.csv")
        self.nlp = NLPModel()
        self.poster_fetcher = PosterFetcher()

        # Preparamos el texto para la búsqueda semántica.
        # NOTA: Para mejorar la búsqueda por "descripción", idealmente 
        # deberías tener una columna 'overview' en tu CSV y sumarla aquí.
        self.movies["semantic_text"] = (
            self.movies["title"].fillna("") + " " +
            self.movies["genres"].fillna("").str.replace("|", " ") + " " +  # <--- ¡AGREGUE ESTE + !
            self.movies["overview"].fillna("") # <--- ¡Esto es la clave!
        )

        # Generamos los embeddings (esto tarda un poco al iniciar)
        print("Generando embeddings de películas...")
        self.movie_embeddings = self.nlp.encode(
            self.movies["semantic_text"].tolist()
        )
        print("Embeddings listos.")

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
            
            # A. Obtener datos visuales e ID de TMDB
            movie_data = self.poster_fetcher.get_movie_data(title)
            tmdb_id = movie_data["tmdb_id"]
            
            # B. Obtener enlace de "dónde ver" si tenemos ID
            watch_link = ""
            providers_info = {}
            if tmdb_id:
                # Busca proveedores en México ('MX'). Cambia 'ES' o 'US' según necesites.
                providers_info = get_watch_providers(tmdb_id, country='MX')
                watch_link = providers_info.get('link', '') # Enlace directo a TMDB Watch

            results.append({
                "movieId": int(row["movieId"]),
                "title": title,
                "genres": row["genres"],
                "score": float(similarities[i]),
                "poster_url": movie_data["poster_url"],
                "tmdb_id": tmdb_id,
                "watch_link": watch_link, # <--- Aquí está tu redirección
                "overview": movie_data.get("overview") # Útil para mostrar descripción en el frontend
            })

        return results