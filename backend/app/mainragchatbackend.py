import os
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from app.routers import query, pdf, langchain

# Load .env file for API key
env_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '.env'))
load_dotenv(dotenv_path=env_path, override=True)

api_key = os.getenv("OPENAI_API_KEY")
print("OpenAI API Key loaded:", bool(api_key))
if not api_key:
    raise RuntimeError("ERROR: OPENAI_API_KEY not loaded from .env")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(query.router, prefix="/query", tags=["Query"])
app.include_router(pdf.router, prefix="/pdf", tags=["PDF"])
app.include_router(langchain.router, prefix="/rag", tags=["RAG"])

# Serve static PDF files, placed in backend/assets/
app.mount(
    "/assets",
    StaticFiles(directory=os.path.join(os.path.dirname(__file__), '..', 'assets')),
    name="assets"
)

@app.get("/")
async def root():
    return {"message": "OK"}
