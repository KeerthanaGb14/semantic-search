from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from openai import OpenAI
import numpy as np
import os

app = FastAPI()

# ---- CORS ----
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

class SimilarityRequest(BaseModel):
    docs: list[str]
    query: str

def cosine(a, b):
    a = np.array(a)
    b = np.array(b)
    return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b)))

@app.get("/")
def home():
    return {"status": "running"}

@app.post("/similarity")
def similarity(data: SimilarityRequest):

    # embed query once
    q_emb = client.embeddings.create(
        model="text-embedding-3-small",
        input=data.query
    ).data[0].embedding

    scores = []

    for doc in data.docs:
        d_emb = client.embeddings.create(
            model="text-embedding-3-small",
            input=doc
        ).data[0].embedding

        sim = cosine(q_emb, d_emb)
        scores.append((doc, sim))

    scores.sort(key=lambda x: x[1], reverse=True)

    top3 = [doc for doc, _ in scores[:3]]

    return {"matches": top3}
