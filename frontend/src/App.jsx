import { useEffect, useState } from "react";
import axios from "axios";
import "./App.css";

const API_URL = "http://127.0.0.1:8000";

function App() {
  const [file, setFile] = useState(null);
  const [query, setQuery] = useState("");
  const [topK, setTopK] = useState(5);

  const [documents, setDocuments] = useState([]);
  const [stats, setStats] = useState({
    total_documents: 0,
    total_chunks: 0,
    last_updated: null,
  });

  const [results, setResults] = useState([]);
  const [answer, setAnswer] = useState("");
  const [message, setMessage] = useState("");
  const [loadingUpload, setLoadingUpload] = useState(false);
  const [loadingSearch, setLoadingSearch] = useState(false);

  const fetchDocuments = async () => {
    try {
      const docsResponse = await axios.get(`${API_URL}/documents`);
      const statsResponse = await axios.get(`${API_URL}/stats`);

      setDocuments(docsResponse.data.documents || []);
      setStats(statsResponse.data.stats || {});
    } catch {
      setMessage("Backend server is not reachable.");
    }
  };

  useEffect(() => {
    fetchDocuments();
  }, []);

  const highlightText = (text, searchQuery) => {
    if (!searchQuery.trim()) return text;

    const words = searchQuery
      .split(" ")
      .filter((word) => word.length > 3)
      .map((word) => word.replace(/[.*+?^${}()|[\]\\]/g, "\\$&"));

    if (words.length === 0) return text;

    const regex = new RegExp(`(${words.join("|")})`, "gi");

    return text.split(regex).map((part, index) =>
      regex.test(part) ? <mark key={index}>{part}</mark> : <span key={index}>{part}</span>
    );
  };

  const handleUpload = async () => {
    if (!file) {
      setMessage("Please select a PDF or TXT file first.");
      return;
    }

    const formData = new FormData();
    formData.append("file", file);

    try {
      setLoadingUpload(true);
      setMessage("");

      const response = await axios.post(`${API_URL}/upload`, formData);

      if (!response.data.success) {
        setMessage(response.data.error || "Upload failed.");
        return;
      }

      setMessage(
        `${response.data.file_name} indexed successfully. ${response.data.chunks_created} chunks created.`
      );

      setFile(null);
      setResults([]);
      setAnswer("");
      fetchDocuments();
    } catch {
      setMessage("Upload failed. Make sure the backend is running.");
    } finally {
      setLoadingUpload(false);
    }
  };

  const handleSearch = async () => {
    if (!query.trim()) {
      setMessage("Please enter a search query.");
      return;
    }

    const formData = new FormData();
    formData.append("query", query);
    formData.append("top_k", topK);

    try {
      setLoadingSearch(true);
      setMessage("");
      setAnswer("");
      setResults([]);

      const response = await axios.post(`${API_URL}/search`, formData);

      if (!response.data.success) {
        setMessage(response.data.error || "Search failed.");
        return;
      }

      setAnswer(response.data.answer || "");
      setResults(response.data.results || []);
    } catch {
      setMessage("Search failed. Make sure the backend is running.");
      setAnswer("");
      setResults([]);
    } finally {
      setLoadingSearch(false);
    }
  };

  const handleClear = async () => {
    try {
      await axios.delete(`${API_URL}/clear`);

      setDocuments([]);
      setResults([]);
      setAnswer("");
      setStats({
        total_documents: 0,
        total_chunks: 0,
        last_updated: null,
      });

      setMessage("All documents and indexes cleared.");
    } catch {
      setMessage("Could not clear documents.");
    }
  };

  return (
    <div className="page">
      <header className="hero">
        <p className="tag">Python • FastAPI • Sentence Transformers • FAISS</p>
        <h1>AI-Powered Semantic Search Engine</h1>
        <p className="subtitle">
          Upload PDF/TXT documents and search them using semantic retrieval and generated answers.
        </p>
      </header>

      <main className="container">
        <section className="stats-grid">
          <div className="stat-card">
            <span>Indexed Documents</span>
            <strong>{stats.total_documents || 0}</strong>
          </div>

          <div className="stat-card">
            <span>Text Chunks</span>
            <strong>{stats.total_chunks || 0}</strong>
          </div>

          <div className="stat-card">
            <span>Last Updated</span>
            <strong>
              {stats.last_updated ? new Date(stats.last_updated).toLocaleString() : "Not yet"}
            </strong>
          </div>
        </section>

        <section className="card">
          <h2>Upload Document</h2>
          <p className="muted">Supported formats: PDF and TXT</p>

          <div className="upload-row">
            <input
              type="file"
              accept=".pdf,.txt"
              onChange={(event) => setFile(event.target.files[0])}
            />

            <button onClick={handleUpload} disabled={loadingUpload}>
              {loadingUpload ? "Indexing..." : "Upload & Index"}
            </button>
          </div>

          {message && <p className="message">{message}</p>}
        </section>

        <section className="card">
          <div className="section-title">
            <div>
              <h2>Indexed Documents</h2>
              <p className="muted">Documents currently available for search</p>
            </div>

            <button className="danger" onClick={handleClear}>
              Clear All
            </button>
          </div>

          {documents.length === 0 ? (
            <p className="muted">No documents indexed yet.</p>
          ) : (
            <div className="doc-list">
              {documents.map((document) => (
                <div className="doc-item" key={document.file_name}>
                  <div>
                    <strong>{document.file_name}</strong>
                    <p>{document.chunks} chunks indexed</p>
                  </div>

                  <span>
                    {document.uploaded_at
                      ? new Date(document.uploaded_at).toLocaleDateString()
                      : "Saved"}
                  </span>
                </div>
              ))}
            </div>
          )}
        </section>

        <section className="card">
          <h2>Semantic Search</h2>
          <p className="muted">
            Ask a natural language question about your uploaded documents.
          </p>

          <textarea
            placeholder="Example: What skills does this document have?"
            value={query}
            onChange={(event) => setQuery(event.target.value)}
          />

          <div className="search-row">
            <label>
              Results
              <input
                type="number"
                min="1"
                max="10"
                value={topK}
                onChange={(event) => setTopK(event.target.value)}
              />
            </label>

            <button onClick={handleSearch} disabled={loadingSearch}>
              {loadingSearch ? "Searching..." : "Search"}
            </button>
          </div>
        </section>

        {answer && (
          <section className="answer-card">
            <h2>Generated Answer</h2>
            <p>{answer}</p>
          </section>
        )}

        <section className="results">
          <h2>Source Chunks</h2>

          {results.length === 0 ? (
            <p className="muted">Relevant source chunks will appear here.</p>
          ) : (
            results.map((result, index) => (
              <article className="result-card" key={`${result.file_name}-${index}`}>
                <div className="result-header">
                  <div>
                    <strong>
                      #{index + 1} {result.file_name}
                    </strong>
                    <p>Chunk {result.chunk_number}</p>
                  </div>

                  <span>Similarity: {result.score}</span>
                </div>

                <p className="result-text">{highlightText(result.text, query)}</p>
              </article>
            ))
          )}
        </section>
      </main>
    </div>
  );
}

export default App;