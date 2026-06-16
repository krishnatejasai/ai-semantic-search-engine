# AI-Powered Semantic Search Engine

A full-stack RAG-style semantic search application that lets users upload documents, retrieve relevant chunks using vector search, and generate concise answers from the retrieved context.

## Tech Stack

**Backend**
- Python
- FastAPI
- Sentence Transformers
- FAISS
- PyPDF

**Frontend**
- React
- Vite
- Axios
- CSS

## Features

- Upload PDF and TXT documents
- Extract document text
- Split documents into searchable chunks
- Generate semantic embeddings
- Store embeddings in FAISS vector index
- Search documents using meaning-based queries
- Display ranked results with similarity scores
- View indexed documents
- Clear all uploaded/indexed documents

## Project Architecture

```txt
User Uploads Document
        ↓
FastAPI Backend
        ↓
Text Extraction
        ↓
Chunking
        ↓
Sentence Transformer Embeddings
        ↓
FAISS Vector Store
        ↓
Semantic Search Results
        ↓
React Frontend

## Screenshots

### Application Dashboard
![Dashboard](screenshots/home.png)

### Generated Answer with Source Chunks
![Results](screenshots/results.png)