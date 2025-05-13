import faiss
import pickle
from typing import List
from sentence_transformers import SentenceTransformer
import numpy as np
import os

class RetrieverAgent:
    def __init__(self, index_path: str = "faiss_index"):
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        self.index_path = index_path
        self.index = None
        self.documents = []

        if os.path.exists(f"{index_path}.index") and os.path.exists(f"{index_path}_docs.pkl"):
            self.load_index()

    def build_index(self, texts: List[str]):
        self.documents = texts
        embeddings = self.model.encode(texts, convert_to_numpy=True)
        self.index = faiss.IndexFlatL2(embeddings.shape[1])
        self.index.add(embeddings)
        self.save_index()

    def retrieve(self, query: str, k: int = 3) -> List[str]:
        if self.index is None:
            raise ValueError("Index not built or loaded yet.")
        query_embedding = self.model.encode([query], convert_to_numpy=True)
        distances, indices = self.index.search(query_embedding, k)
        return [self.documents[i] for i in indices[0]]

    def save_index(self):
        faiss.write_index(self.index, f"{self.index_path}.index")
        with open(f"{self.index_path}_docs.pkl", "wb") as f:
            pickle.dump(self.documents, f)

    def load_index(self):
        self.index = faiss.read_index(f"{self.index_path}.index")
        with open(f"{self.index_path}_docs.pkl", "rb") as f:
            self.documents = pickle.load(f)
