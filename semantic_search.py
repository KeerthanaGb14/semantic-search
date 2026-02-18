from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import numpy as np

app = FastAPI()

# ---- CORS ----
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------- MODELS ----------
class SimilarityRequest(BaseModel):
    docs: list[str]
    query: str

# ---------- EMBEDDING ----------
def embed(text: str):
    np.random.seed(abs(hash(text)) % (10**6))
    return np.random.rand(384)

def cosine(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

# ---------- ROOT ----------
@app.get("/")
def home():
    return {"status": "running"}

# ---------- SIMILARITY ENDPOINT ----------
@app.post("/similarity")
def similarity(data: SimilarityRequest):
    query_vec = embed(data.query)

    scored = []
    for doc in data.docs:
        score = cosine(query_vec, embed(doc))
        scored.append((doc, score))

    scored.sort(key=lambda x: x[1], reverse=True)

    top3 = [doc for doc, _ in scored[:3]]

    return {"matches": top3}
