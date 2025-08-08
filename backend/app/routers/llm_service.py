import os
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.config import settings

# KORRIGIERT: Importiere OllamaLLM aus dem dedizierten Paket 'langchain_ollama'
from langchain_ollama import OllamaLLM

import asyncio

router = APIRouter(tags=["Chatbot"])

llm_instance = None


def get_llm_instance():
    global llm_instance
    if llm_instance is None:
        print("Initialisiere LLM über Ollama: gemma:2b")  # Angepasste Meldung für Gemma
        # KORRIGIERT: Initialisiere OllamaLLM mit gemma:2b
        llm_instance = OllamaLLM(
            model="gemma:2b",  # HIER IST DAS MODELL: "gemma:2b"
            temperature=0.7,
        )
    return llm_instance


class ChatRequest(BaseModel):
    message: str


@router.post("/chat_query/")
async def chat_query(req: ChatRequest):
    try:
        llm = get_llm_instance()

        answer = await asyncio.to_thread(llm.invoke, req.message)

        if not answer:
            answer = "Entschuldigung, ich konnte keine Antwort generieren."
        return {"answer": answer}

    except Exception as e:
        print(f"Fehler bei Chat-Abfrage: {e}")
        raise HTTPException(status_code=500, detail=f"Interner Fehler bei der Chat-Abfrage: {e}")
