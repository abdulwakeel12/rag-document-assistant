# RAG Document Assistant

I built a RAG-based document assistant using FastAPI, ChromaDB, SentenceTransformers, and Groq LLM. Users upload a PDF from the frontend UI. The backend extracts text from the PDF using pypdf, splits the text into chunks, converts each chunk into embeddings using SentenceTransformers, and stores those embeddings in ChromaDB. When the user asks a question, the question is also converted into an embedding. ChromaDB performs semantic similarity search to retrieve the most relevant chunks from the uploaded document. Those retrieved chunks are sent as context to the Groq LLM, which generates the final answer. The frontend communicates with the FastAPI backend using HTTP API calls.

---
## Demo

[Watch Demo on YouTube](https://youtu.be/avvtYP-iho0)

---
## Features

- Upload PDF documents
- Extract text using PyPDF
- Chunk and embed document text
- Store embeddings in ChromaDB
- Ask questions from the uploaded PDF
- Generate grounded answers using Groq LLM
- Prevents answers from unrelated documents using file-specific retrieval
- ChatGPT-style frontend using HTML, CSS, and JavaScript

---

## Tech Stack

- FastAPI
- PyPDF
- SentenceTransformers
- ChromaDB
- Groq API
- HTML
- CSS
- JavaScript

---

## Project Structure

```txt
rag-document-assistant/
├── app/
│   ├── __init__.py
│   └── main.py
├── frontend/
│   ├── index.html
│   ├── script.js
│   └── style.css
├── requirements.txt
├── .gitignore
└── README.md
```

---

## Setup

Install dependencies:

```bash
pip install -r requirements.txt
```

Create a `.env` file:

```env
GROQ_API_KEY=your_groq_api_key_here
```

Run backend:

```bash
uvicorn app.main:app --reload
```

Open frontend:

```txt
frontend/index.html
```

---

## Notes

The following are ignored for security and storage reasons:

- `.vscode/`
- `chroma_db/`
- `rag_env/`
- `uploads/`
- `.env`
