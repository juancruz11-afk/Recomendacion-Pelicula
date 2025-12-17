# backend/recomendacion/tmdb.py
import requests
import os

TMDB_API_KEY = os.getenv('TMDB_API_KEY')

def get_watch_providers(tmdb_id, country='MX'):
    if not tmdb_id:
        return {}
        
    url = f'https://api.themoviedb.org/3/movie/{tmdb_id}/watch/providers'
    params = {'api_key': TMDB_API_KEY}
    
    try:
        res = requests.get(url, params=params)
        data = res.json()
        # Devuelve los datos del país específico o un diccionario vacío
        return data.get('results', {}).get(country, {})
    except Exception as e:
        print(f"Error fetching watch providers: {e}")
        return {}