from fastapi import FastAPI
from app.routers import llm_service # Geändert von langchain

app = FastAPI(title="Einfacher Chatbot Backend") # Titel aktualisiert

# Füge den neuen Router hinzu
app.include_router(llm_service.router, prefix="/chat") # Präfix und Router-Name geändert

