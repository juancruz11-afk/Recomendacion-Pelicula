# backend/recomendacion/generate_embeddings.py
import pandas as pd
import pickle
import os
from model import NLPModel

def generate():
    print("Cargando datos...")
    # Buscamos el archivo enriquecido, si no, el normal
    csv_path = "data/movies_enriched.csv"
    if not os.path.exists(csv_path):
        csv_path = "data/movies.csv"
        print("OJO: Usando movies.csv simple (sin sinopsis). Asegúrate de haber corrido enrich_data.py antes.")
    
    df = pd.read_csv(csv_path)
    
    # Recreamos el texto que lee la IA
    # Aseguramos que 'overview' exista aunque el CSV sea el viejo
    if "overview" not in df.columns:
        df["overview"] = ""

    df["semantic_text"] = (
        df["title"].fillna("") + " " +
        df["genres"].fillna("").str.replace("|", " ") + " " +
        df["overview"].fillna("")
    )
    
    print("Iniciando modelo IA...")
    model = NLPModel()
    
    print("Generando embeddings (esto tardará unos segundos/minutos)...")
    # Aquí es donde ocurre la magia pesada
    embeddings = model.encode(df["semantic_text"].tolist())
    
    # Guardamos el resultado en un archivo .pkl
    output_path = "data/movie_embeddings.pkl"
    print(f"Guardando archivo listo en: {output_path}")
    with open(output_path, "wb") as f:
        pickle.dump(embeddings, f)
        
    print("¡ÉXITO! Ahora debes subir el archivo 'data/movie_embeddings.pkl' a GitHub.")

if __name__ == "__main__":
    generate()