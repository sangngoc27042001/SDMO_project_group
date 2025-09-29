from sentence_transformers import SentenceTransformer
import numpy as np

# Load a local model (downloads once, then cached)
model = SentenceTransformer("all-MiniLM-L6-v2")  # 384 dimensions, very fast

def get_embedding(text: str):
    return model.encode(text)

def cosine_similarity(vec1, vec2):
    v1, v2 = np.array(vec1), np.array(vec2)
    return np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))

def compare_texts(text1: str, text2: str):
    emb1 = get_embedding(text1)
    emb2 = get_embedding(text2)
    return cosine_similarity(emb1, emb2)


# Example
# e1 = get_embedding("I love programming in Python")
# e2 = get_embedding("Python coding is fun")
# print("Cosine similarity:", cosine_similarity(e1, e2))
