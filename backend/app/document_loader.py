from pathlib import Path
from pypdf import PdfReader


def read_pdf(file_path: str) -> str:
    reader = PdfReader(file_path)
    text_parts = []

    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text_parts.append(page_text)

    return "\n".join(text_parts).strip()


def read_txt(file_path: str) -> str:
    path = Path(file_path)
    return path.read_text(encoding="utf-8", errors="ignore").strip()


def load_document_text(file_path: str, file_name: str) -> str:
    lower_name = file_name.lower()

    if lower_name.endswith(".pdf"):
        return read_pdf(file_path)

    if lower_name.endswith(".txt"):
        return read_txt(file_path)

    raise ValueError("Only PDF and TXT files are supported")


def split_text(text: str, chunk_size: int = 450, overlap: int = 80):
    words = text.split()

    if not words:
        return []

    chunks = []
    start = 0

    while start < len(words):
        end = start + chunk_size
        chunk = " ".join(words[start:end]).strip()

        if chunk:
            chunks.append(chunk)

        start = end - overlap

    return chunks