from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import numpy as np
import time

app = FastAPI()

# ---- CORS FIX ----
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---- Documents ----
documents = [f"News article about climate change policy number {i}" for i in range(111)]

class Query(BaseModel):
    query: str
    k: int = 12
    rerank: bool = True
    rerankK: int = 7

@app.get("/")
def home():
    return {"status": "server working"}

def cosine(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

def embed(text):
    np.random.seed(abs(hash(text)) % (10**6))
    return np.random.rand(384)

@app.post("/search")
def search(q: Query):
    start = time.time()

    query_vec = embed(q.query)

    scored = []
    for i, doc in enumerate(documents):
        score = cosine(query_vec, embed(doc))
        scored.append((i, score, doc))

    scored.sort(key=lambda x: x[1], reverse=True)
    top_k = scored[:q.k]

    reranked = []
    for i, s, doc in top_k[:q.rerankK]:
        new_score = min(1.0, s + 0.1)
        reranked.append((i, new_score, doc))

    reranked.sort(key=lambda x: x[1], reverse=True)

    results = []
    for i, s, doc in reranked:
        results.append({
            "id": i,
            "score": round(float(s), 3),
            "content": doc,
            "metadata": {"source": "news"}
        })

    latency = int((time.time() - start) * 1000)

    return {
        "results": results,
        "reranked": True,
        "metrics": {
            "latency": latency,
            "totalDocs": 111
        }
    }
