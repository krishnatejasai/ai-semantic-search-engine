import json
import os
from collections import Counter
from datetime import datetime

import faiss
import numpy as np


STORAGE_DIR = "storage"
INDEX_PATH = os.path.join(STORAGE_DIR, "faiss.index")
DOCS_PATH = os.path.join(STORAGE_DIR, "documents.json")
META_PATH = os.path.join(STORAGE_DIR, "metadata.json")


class VectorStore:
    def __init__(self):
        self.index = None
        self.documents = []
        self.metadata = {
            "total_chunks": 0,
            "total_documents": 0,
            "last_updated": None
        }

        os.makedirs(STORAGE_DIR, exist_ok=True)
        self.load()

    def add_documents(self, chunks, embeddings, file_name):
        if not chunks:
            raise ValueError("No text chunks found to index")

        embeddings = np.array(embeddings).astype("float32")

        if self.index is None:
            dimension = embeddings.shape[1]
            self.index = faiss.IndexFlatIP(dimension)

        self.index.add(embeddings)

        uploaded_at = datetime.now().isoformat(timespec="seconds")

        for position, chunk in enumerate(chunks, start=1):
            self.documents.append({
                "file_name": file_name,
                "chunk_number": position,
                "text": chunk,
                "uploaded_at": uploaded_at
            })

        self._refresh_metadata()
        self.save()

    def search(self, query_embedding, top_k=5):
        if self.index is None or len(self.documents) == 0:
            return []

        top_k = max(1, min(int(top_k), len(self.documents)))

        query_embedding = np.array([query_embedding]).astype("float32")
        scores, indices = self.index.search(query_embedding, top_k)

        results = []

        for score, index in zip(scores[0], indices[0]):
            if index == -1:
                continue

            document = self.documents[index]

            results.append({
                "file_name": document["file_name"],
                "chunk_number": document["chunk_number"],
                "text": document["text"],
                "score": round(float(score), 4),
                "uploaded_at": document.get("uploaded_at")
            })

        return results

    def get_documents(self):
        counts = Counter(doc["file_name"] for doc in self.documents)
        uploaded_times = {}

        for doc in self.documents:
            uploaded_times[doc["file_name"]] = doc.get("uploaded_at")

        return [
            {
                "file_name": file_name,
                "chunks": chunk_count,
                "uploaded_at": uploaded_times.get(file_name)
            }
            for file_name, chunk_count in counts.items()
        ]

    def file_exists(self, file_name):
        return any(doc["file_name"] == file_name for doc in self.documents)

    def get_stats(self):
        self._refresh_metadata()
        return self.metadata

    def save(self):
        if self.index is not None:
            faiss.write_index(self.index, INDEX_PATH)

        with open(DOCS_PATH, "w", encoding="utf-8") as file:
            json.dump(self.documents, file, indent=2)

        with open(META_PATH, "w", encoding="utf-8") as file:
            json.dump(self.metadata, file, indent=2)

    def load(self):
        if os.path.exists(INDEX_PATH):
            self.index = faiss.read_index(INDEX_PATH)

        if os.path.exists(DOCS_PATH):
            with open(DOCS_PATH, "r", encoding="utf-8") as file:
                self.documents = json.load(file)

        if os.path.exists(META_PATH):
            with open(META_PATH, "r", encoding="utf-8") as file:
                self.metadata = json.load(file)

        self._refresh_metadata()

    def clear(self):
        self.index = None
        self.documents = []
        self.metadata = {
            "total_chunks": 0,
            "total_documents": 0,
            "last_updated": None
        }

        for path in [INDEX_PATH, DOCS_PATH, META_PATH]:
            if os.path.exists(path):
                os.remove(path)

    def _refresh_metadata(self):
        unique_files = set(doc["file_name"] for doc in self.documents)

        self.metadata = {
            "total_chunks": len(self.documents),
            "total_documents": len(unique_files),
            "last_updated": datetime.now().isoformat(timespec="seconds")
            if self.documents
            else None
        }


vector_store = VectorStore()