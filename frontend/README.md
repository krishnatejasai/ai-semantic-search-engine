# AI-Powered Semantic Search Engine

A full-stack semantic search engine that allows users to upload PDF/TXT documents and search them by meaning using Sentence Transformers and FAISS.

## Tech Stack

- Python
- FastAPI
- Sentence Transformers
- FAISS
- React
- Vite
- Axios

## Features

- Upload PDF/TXT documents
- Extract and chunk document text
- Generate semantic embeddings
- Store vectors using FAISS
- Search documents using natural language queries
- Display ranked results with similarity scores
- Clear indexed documents

## Run Backend

```bash
cd backend
source venv/bin/activate
uvicorn app.main:app --reload