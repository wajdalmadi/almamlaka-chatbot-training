import os
import json
import math
import voyageai
from dotenv import load_dotenv

load_dotenv()

client = voyageai.Client()
INDEX_FILE = "index.json"


def cosine_similarity(vec1, vec2):
    dot_product = sum(a * b for a, b in zip(vec1, vec2))
    magnitude1 = math.sqrt(sum(a * a for a in vec1))
    magnitude2 = math.sqrt(sum(b * b for b in vec2))
    if magnitude1 == 0 or magnitude2 == 0:
        return 0
    return dot_product / (magnitude1 * magnitude2)


def load_index():
    with open(INDEX_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def retrieve(query, top_k=6):
    chunks = load_index()

    result = client.embed([query], model="voyage-multilingual-2", input_type="query")
    query_embedding = result.embeddings[0]

    scored = []
    for chunk in chunks:
        score = cosine_similarity(query_embedding, chunk["embedding"])
        scored.append((score, chunk))

    scored.sort(key=lambda x: x[0], reverse=True)

    top_chunks = scored[:top_k]
    return top_chunks