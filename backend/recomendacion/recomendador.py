from model import NLPModel
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
import numpy as np
from posters import PosterFetcher

class Recomendador:
    def __init__(self):
        self.movies = pd.read_csv("data/movies.csv")

        self.nlp = NLPModel()

        self.movies["semantic_text"] = (
            self.movies["title"].fillna("") + " " +
            self.movies["genres"].fillna("")
        )

        self.movie_embeddings = self.nlp.encode(
            self.movies["semantic_text"].tolist()
        )

        self.poster = PosterFetcher()

    def recomendar_por_texto(self, query, n=8):
        query_embedding = self.nlp.encode(query)

        similarities = cosine_similarity(
            query_embedding,
            self.movie_embeddings
        )[0]

        top_idx = np.argsort(similarities)[::-1][:n]

        results = []
        for i in top_idx:
            row = self.movies.iloc[i]
            results.append({
                "movieId": int(row["movieId"]),
                "title": row["title"],
                "genres": row["genres"],
                "score": float(similarities[i]),
                "poster_url": self.poster.get_poster_url(row["title"])
            })

        return results
