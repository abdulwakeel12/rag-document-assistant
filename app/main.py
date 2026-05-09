# Python built-in libraries
import os
import uuid

# Third-party libraries
import chromadb
from dotenv import load_dotenv
from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from groq import Groq
from pypdf import PdfReader
from sentence_transformers import SentenceTransformer

# Load environment variables from .env file
load_dotenv()

app = FastAPI(title="RAG Document Assistant API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIR = "uploads"
CHROMA_DIR = "chroma_db"

os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(CHROMA_DIR, exist_ok=True)

embedding_model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

chroma_client = chromadb.PersistentClient(path=CHROMA_DIR)
collection = chroma_client.get_or_create_collection(name="documents")

groq_client = Groq(api_key=os.environ.get("GROQ_API_KEY"))


def chunk_text(text: str, chunk_size: int = 700, overlap: int = 100):
    chunks = []
    start = 0

    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end]

        if chunk.strip():
            chunks.append(chunk)

        start = end - overlap

    return chunks


def generate_answer_with_groq(question: str, context: str):
    response = groq_client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a document assistant. "
                    "Answer only from the provided context. "
                    "If the answer is not present in the context, say: "
                    "'I could not find this in the uploaded document.'"
                ),
            },
            {
                "role": "user",
                "content": f"Context:\n{context}\n\nQuestion:\n{question}",
            },
        ],
    )

    return response.choices[0].message.content


@app.get("/")
def home():
    return {"message": "Backend is running"}


@app.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):
    file_id = str(uuid.uuid4())
    file_path = os.path.join(UPLOAD_DIR, f"{file_id}_{file.filename}")

    content = await file.read()

    if len(content) > 25 * 1024 * 1024:
        return {"error": "File too large. Please upload a PDF under 25 MB."}

    with open(file_path, "wb") as f:
        f.write(content)

    reader = PdfReader(file_path)

    total_characters = 0
    total_chunks = 0

    for page_number, page in enumerate(reader.pages, start=1):
        page_text = page.extract_text() or ""
        total_characters += len(page_text)

        chunks = chunk_text(page_text)

        for chunk_index, chunk in enumerate(chunks):
            chunk_id = f"{file_id}_page_{page_number}_chunk_{chunk_index}"
            embedding = embedding_model.encode(chunk).tolist()

            collection.add(
                ids=[chunk_id],
                documents=[chunk],
                embeddings=[embedding],
                metadatas=[
                    {
                        "file_id": file_id,
                        "filename": file.filename,
                        "page": page_number,
                        "chunk_index": chunk_index,
                    }
                ],
            )

            total_chunks += 1

    return {
        "message": "PDF uploaded, chunked, embedded, and stored in ChromaDB",
        "file_id": file_id,
        "filename": file.filename,
        "pages": len(reader.pages),
        "characters_extracted": total_characters,
        "total_chunks": total_chunks,
        "stored_in_chroma": True,
    }


@app.get("/ask")
def ask_question(question: str, file_id: str):
    question_embedding = embedding_model.encode(question).tolist()

    results = collection.query(
    query_embeddings=[question_embedding],
    n_results=12,
    where={"file_id": file_id},
)

    matched_chunks = results["documents"][0]
    sources = results["metadatas"][0]

    context = "\n\n".join(matched_chunks)

    answer = generate_answer_with_groq(question, context)

    return {
        "question": question,
        "answer": answer,
        "sources": sources,
    }