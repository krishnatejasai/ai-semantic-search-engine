from pypdf import PdfReader


def read_pdf(file_path: str) -> str:
    reader = PdfReader(file_path)
    text = ""

    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text + "\n"

    return text.strip()


def read_txt(file_path: str) -> str:
    with open(file_path, "r", encoding="utf-8") as file:
        return file.read().strip()


def split_text(text: str, chunk_size: int = 450, overlap: int = 80):
    words = text.split()
    chunks = []

    if not words:
        return chunks

    start = 0
    while start < len(words):
        end = start + chunk_size
        chunk = " ".join(words[start:end])
        chunks.append(chunk)
        start = end - overlap

    return chunks