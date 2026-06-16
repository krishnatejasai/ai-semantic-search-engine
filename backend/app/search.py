from app.embeddings import create_embeddings
from app.vector_store import vector_store


def semantic_search(query: str, top_k: int = 5):
    query_embedding = create_embeddings([query])[0]
    return vector_store.search(query_embedding, top_k)