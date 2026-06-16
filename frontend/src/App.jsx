import { useEffect, useState } from "react";
import axios from "axios";
import "./App.css";

const API_URL = "http://127.0.0.1:8000";

function App() {
  const [file, setFile] = useState(null);
  const [query, setQuery] = useState("");
  const [topK, setTopK] = useState(5);
  const [documents, setDocuments] = useState([]);
  const [results, setResults] = useState([]);
  const [uploadMessage, setUploadMessage] = useState("");
  const [loadingUpload, setLoadingUpload] = useState(false);
  const [loadingSearch, setLoadingSearch] = useState(false);

  const fetchDocuments = async () => {
    try {
      const response = await axios.get(`${API_URL}/documents`);
      setDocuments(response.data.documents || []);
    } catch (error) {
      console.error(error);
    }
  };

  useEffect(() => {
    fetchDocuments();
  }, []);

  const handleUpload = async () => {
    if (!file) {
      setUploadMessage("Please select a PDF or TXT file first.");
      return;
    }

    const formData = new FormData();
    formData.append("file", file);

    try {
      setLoadingUpload(true);
      setUploadMessage("");

      const response = await axios.post(`${API_URL}/upload`, formData);

      if (response.data.error) {
        setUploadMessage(response.data.error);
      } else {
        setUploadMessage(
          `${response.data.file_name} uploaded successfully. ${response.data.chunks_created} chunks created.`
        );
      }

      setFile(null);
      fetchDocuments();
    } catch (error) {
      setUploadMessage("Upload failed. Please check backend server.");
    } finally {
      setLoadingUpload(false);
    }
  };

  const handleSearch = async () => {
    if (!query.trim()) {
      return;
    }

    const formData = new FormData();
    formData.append("query", query);
    formData.append("top_k", topK);

    try {
      setLoadingSearch(true);
      const response = await axios.post(`${API_URL}/search`, formData);
      setResults(response.data.results || []);
    } catch (error) {
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
      setUploadMessage("All documents cleared.");
    } catch (error) {
      setUploadMessage("Could not clear documents.");
    }
  };

  return (
    <div className="page">
      <header className="hero">
        <p className="tag">Python • FastAPI • Sentence Transformers • FAISS</p>
        <h1>AI-Powered Semantic Search Engine</h1>
        <p className="subtitle">
          Upload documents and search them by meaning, not just exact keywords.
        </p>
      </header>

      <main className="container">
        <section className="card">
          <h2>Upload Document</h2>
          <p className="muted">Supported formats: PDF and TXT</p>

          <div className="upload-row">
            <input
              type="file"
              accept=".pdf,.txt"
              onChange={(e) => setFile(e.target.files[0])}
            />
            <button onClick={handleUpload} disabled={loadingUpload}>
              {loadingUpload ? "Indexing..." : "Upload & Index"}
            </button>
          </div>

          {uploadMessage && <p className="message">{uploadMessage}</p>}
        </section>

        <section className="card">
          <div className="section-title">
            <h2>Indexed Documents</h2>
            <button className="danger" onClick={handleClear}>
              Clear All
            </button>
          </div>

          {documents.length === 0 ? (
            <p className="muted">No documents indexed yet.</p>
          ) : (
            <div className="doc-list">
              {documents.map((doc) => (
                <div className="doc-item" key={doc.file_name}>
                  <strong>{doc.file_name}</strong>
                  <span>{doc.chunks} chunks</span>
                </div>
              ))}
            </div>
          )}
        </section>

        <section className="card">
          <h2>Semantic Search</h2>

          <textarea
            placeholder="Example: What does this document say about machine learning?"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
          />

          <div className="search-row">
            <label>
              Results:
              <input
                type="number"
                min="1"
                max="10"
                value={topK}
                onChange={(e) => setTopK(e.target.value)}
              />
            </label>

            <button onClick={handleSearch} disabled={loadingSearch}>
              {loadingSearch ? "Searching..." : "Search"}
            </button>
          </div>
        </section>

        <section className="results">
          <h2>Search Results</h2>

          {results.length === 0 ? (
            <p className="muted">Results will appear here after searching.</p>
          ) : (
            results.map((result, index) => (
              <div className="result-card" key={index}>
                <div className="result-header">
                  <strong>#{index + 1} {result.file_name}</strong>
                  <span>Similarity: {result.score}</span>
                </div>
                <p>{result.text}</p>
              </div>
            ))
          )}
        </section>
      </main>
    </div>
  );
}

export default App;