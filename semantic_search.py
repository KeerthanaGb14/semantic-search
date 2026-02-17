from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Query(BaseModel):
    query: str
    k: int = 12
    rerank: bool = True
    rerankK: int = 7

@app.get("/")
def root():
    return {"status": "running"}

@app.post("/search")
def search(q: Query):
    results = []
    for i in range(7):
        results.append({
            "id": i,
            "score": round(1 - i*0.1, 2),
            "content": f"Sample news document {i}",
            "metadata": {"source": "news"}
        })

    return {
        "results": results,
        "reranked": True,
        "metrics": {
            "latency": 50,
            "totalDocs": 111
        }
    }
