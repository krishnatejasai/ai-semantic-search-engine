# AI-Powered Semantic Search Engine

A full-stack RAG-style semantic search application that allows users to upload PDF/TXT documents, retrieve relevant content using vector search, and generate concise answers from retrieved context.

---

## Demo Screenshots

### Dashboard

![Dashboard](./screenshots/home.png)

### Semantic Search Results

![Semantic Search Results](./screenshots/results.png)

---

## Tech Stack

### Backend

* Python
* FastAPI
* Sentence Transformers
* FAISS
* PyPDF
* NumPy

### Frontend

* React
* Vite
* Axios
* CSS

---

## Features

* Upload PDF and TXT documents
* Extract document text automatically
* Split documents into searchable chunks
* Generate semantic embeddings using Sentence Transformers
* Store embeddings in a FAISS vector database
* Perform meaning-based semantic search
* Generate concise answers from retrieved context
* Display ranked source chunks with similarity scores
* View indexed document statistics
* Clear all indexed documents and embeddings
* Interactive React-based frontend

---

## Project Architecture

```text
User Uploads Document
        ↓
FastAPI Backend
        ↓
Text Extraction
        ↓
Document Chunking
        ↓
Sentence Transformer Embeddings
        ↓
FAISS Vector Store
        ↓
Semantic Retrieval
        ↓
Generated Answer
        ↓
React Frontend
```

---

## Folder Structure

```text
ai-semantic-search-engine/
│
├── backend/
│   ├── app/
│   │   ├── document_loader.py
│   │   ├── embeddings.py
│   │   ├── main.py
│   │   ├── search.py
│   │   └── vector_store.py
│   │
│   └── requirements.txt
│
├── frontend/
│   ├── src/
│   │   ├── App.jsx
│   │   ├── App.css
│   │   └── main.jsx
│   │
│   └── package.json
│
├── screenshots/
│   ├── home.png
│   └── results.png
│
└── README.md
```

---

## How It Works

1. User uploads a PDF or TXT document.
2. The backend extracts document text.
3. Text is divided into smaller chunks.
4. Sentence Transformers generate vector embeddings.
5. Embeddings are stored in a FAISS vector index.
6. User submits a natural language query.
7. FAISS retrieves the most relevant chunks.
8. Retrieved chunks are used to generate an answer.
9. Source chunks and similarity scores are displayed.

---

## Running the Backend

```bash
cd backend

python3 -m venv venv

source venv/bin/activate

pip install -r requirements.txt

uvicorn app.main:app --reload
```

Backend URL:

```text
http://127.0.0.1:8000
```

API Documentation:

```text
http://127.0.0.1:8000/docs
```

---

## Running the Frontend

```bash
cd frontend

npm install

npm run dev
```

Frontend URL:

```text
http://localhost:5173
```

---

## API Endpoints

| Method | Endpoint   | Description                           |
| ------ | ---------- | ------------------------------------- |
| GET    | /          | Backend status                        |
| GET    | /health    | Health check                          |
| POST   | /upload    | Upload and index document             |
| POST   | /search    | Semantic search and answer generation |
| GET    | /documents | View indexed documents                |
| GET    | /stats     | View indexing statistics              |
| DELETE | /clear     | Clear all indexed data                |

---

## Resume Description

Built a full-stack AI-powered semantic search engine using FastAPI, React, Sentence Transformers, and FAISS to enable meaning-based document retrieval and answer generation from uploaded documents.

---

## Resume Bullet Points

* Developed a full-stack semantic search engine that enables users to upload PDF/TXT documents and search them using natural language queries.
* Implemented document chunking, vector embedding generation, and FAISS-based similarity search for context-aware document retrieval.
* Built FastAPI REST APIs and a React frontend to support document indexing, generated answers, ranked source chunks, and similarity scoring.
* Designed an end-to-end retrieval pipeline using Sentence Transformers and vector databases for semantic document understanding.

---

## Future Improvements

* Gemini/OpenAI-powered RAG responses
* Multi-document conversational chat
* User authentication and document management
* Cloud deployment using Docker and Kubernetes
* Support for Word, Excel, and PowerPoint documents
* Search analytics dashboard
