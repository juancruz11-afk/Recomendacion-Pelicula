# model.py
from sentence_transformers import SentenceTransformer

class NLPModel:
    def __init__(self):
        # modelo ligero, rápido y perfecto para demos
        self.model = SentenceTransformer("all-MiniLM-L6-v2")

    def encode(self, texts):
        """
        Convierte texto(s) a embeddings numéricos
        texts: str o list[str]
        """
        if isinstance(texts, str):
            texts = [texts]
        return self.model.encode(texts)
