# RAG Document Assistant

A web-based RAG application that allows users to upload PDF documents and ask questions from them using semantic search and an LLM.

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

- `.env`
- `uploads/`
- `chroma_db/`
- `rag_env/`
- `__pycache__/`
