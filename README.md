# AI-Powered Semantic Search Engine

A full-stack semantic search engine that allows users to upload PDF/TXT documents and search them using natural language queries.  
The system uses Sentence Transformers to convert text into embeddings and FAISS for fast similarity search.

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