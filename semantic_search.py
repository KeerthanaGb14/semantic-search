from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Query(BaseModel):
    query: str
    k: int = 12
    rerank: bool = True
    rerankK: int = 7

@app.get("/")
def home():
    return {"status": "server working"}

@app.post("/search")
def search(q: Query):
    return {
        "results": [
            {"id": 1, "score": 0.9, "content": "sample doc", "metadata": {"source": "test"}}
        ],
        "reranked": True,
        "metrics": {"latency": 10, "totalDocs": 111}
    }
