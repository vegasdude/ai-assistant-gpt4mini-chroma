import openai
import numpy as np

def create_embedding(text):
    try:
        resp = openai.Embedding.create(
            input=text,
            model="text-embedding-3-small"
        )
        return resp['data'][0]['embedding']
    except Exception as e:
        print("Embedding error:", e)
        return []

def cosine_similarity(vec1, vec2):
    if not vec1 or not vec2:
        return 0
    a = np.array(vec1)
    b = np.array(vec2)
    return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b)))

def search_embeddings(data, query, top_k=3):
    q_emb = create_embedding(query)
    scored = [(item, cosine_similarity(item.get('embedding', []), q_emb)) for item in data]
    scored.sort(key=lambda x: x[1], reverse=True)
    return [item for item, score in scored[:top_k]]
