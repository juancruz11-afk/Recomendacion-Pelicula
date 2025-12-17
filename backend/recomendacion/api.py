# api.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from recomendador import Recomendador

app = FastAPI()
recomendador = Recomendador()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"status": "ok"}

@app.get("/recommend/text")
def recommend_text(q: str):
    return recomendador.recomendar_por_texto(q)