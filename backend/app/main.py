from fastapi import FastAPI
# Importiere BEIDE spezifischen Router aus llm_service
from app.routers.llm_service import chat_router, rag_router

app = FastAPI(title="Einfacher Chatbot Backend", version="0.1.0") # Titel und Version aktualisiert

# Binde den Chat-Router ein (Präfix ist bereits im Router definiert)
app.include_router(chat_router)

# Binde den RAG-Router ein (Präfix ist bereits im Router definiert)
app.include_router(rag_router)
