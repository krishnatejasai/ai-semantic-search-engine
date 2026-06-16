import faiss
import numpy as np


class VectorStore:
    def __init__(self):
        self.index = None
        self.documents = []
        self.dimension = None

    def add_documents(self, chunks, embeddings, file_name):
        embeddings = np.array(embeddings).astype("float32")

        if self.index is None:
            self.dimension = embeddings.shape[1]
            self.index = faiss.IndexFlatIP(self.dimension)

        self.index.add(embeddings)

        for chunk in chunks:
            self.documents.append({
                "file_name": file_name,
                "text": chunk
            })

    def search(self, query_embedding, top_k=5):
        if self.index is None or len(self.documents) == 0:
            return []

        query_embedding = np.array([query_embedding]).astype("float32")
        scores, indices = self.index.search(query_embedding, top_k)

        results = []

        for score, index in zip(scores[0], indices[0]):
            if index == -1:
                continue

            document = self.documents[index]

            results.append({
                "file_name": document["file_name"],
                "text": document["text"],
                "score": round(float(score), 4)
            })

        return results

    def get_documents(self):
        files = {}

        for doc in self.documents:
            file_name = doc["file_name"]
            files[file_name] = files.get(file_name, 0) + 1

        return [
            {
                "file_name": file_name,
                "chunks": chunks
            }
            for file_name, chunks in files.items()
        ]

    def clear(self):
        self.index = None
        self.documents = []
        self.dimension = None


vector_store = VectorStore()