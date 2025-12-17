# backend/recomendacion/enrich_data.py
import pandas as pd
import requests
import os
import time
from dotenv import load_dotenv

load_dotenv()
TMDB_API_KEY = os.getenv("TMDB_API_KEY")

def fetch_overview(title):
    try:
        url = "https://api.themoviedb.org/3/search/movie"
        params = {
            "api_key": TMDB_API_KEY,
            "query": title,
            "language": "es-MX" # Descargamos sinopsis en español
        }
        response = requests.get(url, params=params)
        data = response.json()
        
        if data['results']:
            # Devolvemos la sinopsis de la primera coincidencia
            return data['results'][0].get('overview', '')
    except Exception as e:
        print(f"Error buscando {title}: {e}")
    
    return ""

print("Cargando películas...")
df = pd.read_csv("data/movies.csv")

# Creamos la columna overview vacía si no existe
if "overview" not in df.columns:
    df["overview"] = ""

print("Descargando sinopsis de TMDB (esto puede tardar)...")

# Recorremos las películas y buscamos su sinopsis
# NOTA: Para pruebas rápidas, puedes limitar esto agregando .head(50) al final de df.iterrows()
count = 0
for index, row in df.iterrows():
    # Solo buscamos si no tiene overview o es muy corto
    if pd.isna(row["overview"]) or len(str(row["overview"])) < 5:
        overview = fetch_overview(row["title"])
        df.at[index, "overview"] = overview
        
        count += 1
        if count % 10 == 0:
            print(f"Procesadas {count} películas...")
            time.sleep(0.2) # Pequeña pausa para no saturar la API

print("Guardando nuevo archivo enriquecido...")
df.to_csv("data/movies_enriched.csv", index=False)
print("¡Listo! Archivo 'data/movies_enriched.csv' creado.")