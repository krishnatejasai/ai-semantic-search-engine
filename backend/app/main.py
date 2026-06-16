import os
import shutil
from pathlib import Path

from fastapi import FastAPI, File, Form, UploadFile
from fastapi.middleware.cors import CORSMiddleware

from app.document_loader import load_document_text, split_text
from app.embeddings import MODEL_NAME, create_embeddings
from app.search import semantic_search
from app.vector_store import vector_store


app = FastAPI(
    title="AI-Powered Semantic Search Engine",
    description="Upload documents, generate embeddings, store them in FAISS, and search by meaning.",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DATA_DIR = "data"
Path(DATA_DIR).mkdir(exist_ok=True)


@app.get("/")
def home():
    return {
        "message": "AI-Powered Semantic Search Engine is running",
        "model": MODEL_NAME,
        "features": [
            "PDF/TXT upload",
            "Text extraction",
            "Document chunking",
            "Sentence Transformer embeddings",
            "Persistent FAISS vector storage",
            "Semantic similarity search",
            "Document statistics"
        ]
    }


@app.get("/health")
def health_check():
    stats = vector_store.get_stats()

    return {
        "status": "healthy",
        "model": MODEL_NAME,
        "indexed_documents": stats["total_documents"],
        "indexed_chunks": stats["total_chunks"]
    }


@app.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    file_name = file.filename

    if not file_name:
        return {"success": False, "error": "Invalid file name"}

    if not file_name.lower().endswith((".pdf", ".txt")):
        return {"success": False, "error": "Only PDF and TXT files are supported"}

    if vector_store.file_exists(file_name):
        return {
            "success": False,
            "error": "This file is already indexed. Clear documents or rename the file before uploading again."
        }

    file_path = os.path.join(DATA_DIR, file_name)

    try:
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        text = load_document_text(file_path, file_name)

        if not text:
            return {
                "success": False,
                "error": "Could not extract readable text from this document"
            }

        chunks = split_text(text)
        embeddings = create_embeddings(chunks)
        vector_store.add_documents(chunks, embeddings, file_name)

        return {
            "success": True,
            "message": "Document uploaded and indexed successfully",
            "file_name": file_name,
            "chunks_created": len(chunks),
            "characters_extracted": len(text)
        }

    except Exception as error:
        return {
            "success": False,
            "error": str(error)
        }


@app.post("/search")
async def search_documents(
    query: str = Form(...),
    top_k: int = Form(5)
):
    if not query.strip():
        return {"success": False, "error": "Search query cannot be empty"}

    results = semantic_search(query, top_k)

    from app.search import generate_answer
    answer = generate_answer(query, results)

    return {
        "success": True,
        "query": query,
        "answer": answer,
        "results_count": len(results),
        "results": results
    }


@app.get("/documents")
def get_documents():
    return {
        "success": True,
        "documents": vector_store.get_documents()
    }


@app.get("/stats")
def get_stats():
    return {
        "success": True,
        "stats": vector_store.get_stats()
    }


@app.delete("/clear")
def clear_documents():
    vector_store.clear()

    if os.path.exists(DATA_DIR):
        for file_name in os.listdir(DATA_DIR):
            file_path = os.path.join(DATA_DIR, file_name)
            if os.path.isfile(file_path):
                os.remove(file_path)

    return {
        "success": True,
        "message": "All uploaded documents and vector indexes cleared successfully"
    }