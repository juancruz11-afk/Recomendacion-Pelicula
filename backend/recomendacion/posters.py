# backend/recomendacion/posters.py
import os
import requests
import re
from dotenv import load_dotenv

load_dotenv()
TMDB_API_KEY = os.getenv("TMDB_API_KEY")

class PosterFetcher:
    def __init__(self, api_key=TMDB_API_KEY):
        self.api_key = api_key
        self.base_search = "https://api.themoviedb.org/3/search/movie"
        self.base_image = "https://image.tmdb.org/t/p/w500"

    def get_movie_data(self, title):
        """
        Busca la película en TMDB y devuelve un diccionario con:
        - poster_url
        - tmdb_id (necesario para buscar proveedores)
        - overview (opcional, útil para el futuro)
        """
        # Limpiar el título (quitar el año entre paréntesis si existe)
        clean_title = re.sub(r'\s*\(\d{4}\)', '', title).strip()
        
        try:
            params = {
                'api_key': self.api_key,
                'query': clean_title,
                'language': 'es-MX' # Buscamos datos en español preferiblemente
            }
            response = requests.get(self.base_search, params=params)
            data = response.json()

            if data.get('results'):
                first_result = data['results'][0]
                poster_path = first_result.get('poster_path')
                tmdb_id = first_result.get('id')
                
                poster_url = f"{self.base_image}{poster_path}" if poster_path else "https://via.placeholder.com/500x750?text=No+Poster"
                
                return {
                    "poster_url": poster_url,
                    "tmdb_id": tmdb_id,
                    "overview": first_result.get('overview', '')
                }
            
        except Exception as e:
            print(f"Error fetching data for {title}: {e}")

        return {
            "poster_url": "https://via.placeholder.com/500x750?text=Error",
            "tmdb_id": None,
            "overview": ""
        }