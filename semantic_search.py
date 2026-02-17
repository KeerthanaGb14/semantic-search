from fastapi import FastAPI
from pydantic import BaseModel
import time

app = FastAPI()

class Query(BaseModel):
    query: str
    k: int = 12
    rerank: bool = True
    rerankK: int = 7

@app.get("/")
def home():
    return {"status": "running"}

@app.post("/search")
def search(q: Query):
    start = time.time()

    results = []
    for i in range(7):
        results.append({
            "id": i,
            "score": round(1 - i*0.1, 2),
            "content": f"News article about {q.query} {i}",
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
