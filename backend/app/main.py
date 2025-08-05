import os
from dotenv import load_dotenv, find_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

# Hugging Face Auth
from huggingface_hub import login

# Router imports
from app.routers import query, pdf, langchain

# Load .env
load_dotenv(find_dotenv(), override=True)

# API-Schlüssel aus Umgebungsvariablen
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
HF_TOKEN = os.getenv("HUGGINGFACEHUB_API_TOKEN")

print("OPENAI_API_KEY:", bool(OPENAI_API_KEY), " ‣ HF-HUB‑Token:", bool(HF_TOKEN))

if not (OPENAI_API_KEY or HF_TOKEN):
    raise RuntimeError(
        "❗ Bitte setze entweder OPENAI_API_KEY oder HUGGINGFACEHUB_API_TOKEN in deiner .env"
    )

# Hugging Face Login
if HF_TOKEN:
    login(HF_TOKEN)
else:
    print("Kein HF-Token – OpenAI-API genutzt")

app = FastAPI(
    title="🧠 Portfolio RAG‑Chatbot Backend",
    description="API für PDF‑Upload, Retrieval‑QA mit RAG über lokale oder Hugging Face Modelle",
)

# CORS-Konfiguration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Router
app.include_router(query.router, prefix="/query", tags=["Query"])
app.include_router(pdf.router, prefix="/pdf", tags=["PDF"])
app.include_router(langchain.router, prefix="/rag", tags=["RAG"])

# Static files
root_dir = os.path.dirname(__file__)
assets_path = os.path.join(root_dir, '..', '..', 'assets')
score = "OK ✅" if os.path.isdir(assets_path) else "❌ dir missing"
print("Assets‑Ordner gefunden:", assets_path, score)
app.mount("/assets", StaticFiles(directory=assets_path), name="assets")

@app.get("/")
async def root():
    return {"status": "running", "key-check-passed": True}
