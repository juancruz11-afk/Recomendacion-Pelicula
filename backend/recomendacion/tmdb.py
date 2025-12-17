import requests
import os

TMDB_API_KEY = os.getenv('TMDB_API_KEY')

def get_watch_providers(tmdb_id, country='MX'):
    url = f'https://api.themoviedb.org/3/movie/{tmdb_id}/watch/providers'
    params = {'api_key': TMDB_API_KEY}
    res = requests.get(url, params=params).json()
    return res.get('results', {}).get(country, {})
