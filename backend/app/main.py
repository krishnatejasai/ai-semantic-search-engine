import os
import shutil
from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware

from app.document_loader import read_pdf, read_txt, split_text
from app.embeddings import create_embeddings
from app.vector_store import vector_store
from app.search import semantic_search


app = FastAPI(title="AI-Powered Semantic Search Engine")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DATA_DIR = "data"
os.makedirs(DATA_DIR, exist_ok=True)


@app.get("/")
def home():
    return {
        "message": "AI-Powered Semantic Search Engine is running",
        "features": [
            "PDF/TXT upload",
            "Sentence Transformer embeddings",
            "FAISS semantic search",
            "Document chunk retrieval"
        ]
    }


@app.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    file_path = os.path.join(DATA_DIR, file.filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    if file.filename.lower().endswith(".pdf"):
        text = read_pdf(file_path)
    elif file.filename.lower().endswith(".txt"):
        text = read_txt(file_path)
    else:
        return {"error": "Only PDF and TXT files are supported"}

    if not text:
        return {"error": "Could not extract text from this document"}

    chunks = split_text(text)
    embeddings = create_embeddings(chunks)

    vector_store.add_documents(chunks, embeddings, file.filename)

    return {
        "message": "Document uploaded and indexed successfully",
        "file_name": file.filename,
        "chunks_created": len(chunks)
    }


@app.post("/search")
async def search_documents(query: str = Form(...), top_k: int = Form(5)):
    if not query.strip():
        return {"error": "Search query cannot be empty"}

    results = semantic_search(query, top_k)

    return {
        "query": query,
        "results": results
    }


@app.get("/documents")
def get_documents():
    return {
        "documents": vector_store.get_documents()
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
        "message": "All documents and vectors cleared successfully"
    }