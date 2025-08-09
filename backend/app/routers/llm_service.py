import os
import torch
import asyncio
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.config import settings
from app.utils.pdf_utils import extract_text_from_pdf

# Importe für Ollama (Basis-Chat)
from langchain_ollama import OllamaLLM

# Importe für Hugging Face (RAG-Funktionalität)
from langchain_huggingface.embeddings import HuggingFaceEmbeddings, HuggingFaceEndpointEmbeddings
from langchain_huggingface.llms import HuggingFacePipeline

from langchain_core.prompts import PromptTemplate
from langchain.chains import RetrievalQA

from langchain.schema import Document
from langchain_community.vectorstores import Chroma # Geändert von langchain.vectorstores zu langchain_community.vectorstores


# --- Definiere separate APIRouter Instanzen für Chat und RAG ---
chat_router = APIRouter(prefix="/chat", tags=["Chatbot"])
rag_router = APIRouter(prefix="/rag", tags=["RAG"])


# --- Ollama / Basis-Chat Instanz ---
def get_ollama_llm_instance():
    print("Initialisiere LLM über Ollama: gemma:2b")
    return OllamaLLM(
        model="gemma:2b",  # HIER IST DAS MODELL: "gemma:2b"
        temperature=0.7,
    )

class ChatRequest(BaseModel):
    message: str

@chat_router.post("/chat_query/") # Verwende chat_router hier
async def chat_query(req: ChatRequest):
    try:
        llm = get_ollama_llm_instance()
        answer = await asyncio.to_thread(llm.invoke, req.message)
        if not answer:
            answer = "Entschuldigung, ich konnte keine Antwort generieren."
        return {"answer": answer}
    except Exception as e:
        print(f"Fehler bei Chat-Abfrage: {e}")
        raise HTTPException(status_code=500, detail=f"Interner Fehler bei der Chat-Abfrage: {e}")


# --- RAG-Funktionalität (aus der alten langchain.py verschoben) ---
class RagRequest(BaseModel):
    question: str
    doc_path: str

@rag_router.post("/rag_query/") # Verwende rag_router hier
async def rag_query(req: RagRequest):
    try:
        full_pdf_path = settings.BASE_DIR / req.doc_path
        if not full_pdf_path.is_file():
            raise HTTPException(status_code=400, detail=f"PDF nicht gefunden: {full_pdf_path}")
        lines = extract_text_from_pdf(str(full_pdf_path))
        if not lines:
            raise ValueError("❗ Kein Text aus PDF extrahiert.")
        if settings.HUGGINGFACEHUB_API_TOKEN:
            embeddings = HuggingFaceEndpointEmbeddings(
                model="sentence-transformers/all-MiniLM-L6-v2",
                huggingfacehub_api_token=settings.HUGGINGFACEHUB_API_TOKEN,
            )
        else:
            embeddings = HuggingFaceEmbeddings(
                model_name="sentence-transformers/all-MiniLM-L6-v2",
                model_kwargs={"device": "cpu"},
            )
        docs = [Document(page_content=line, metadata={}) for line in lines]
        vectordb = Chroma.from_documents(
            documents=docs,
            embedding=embeddings,
            collection_name="rag_pdf_collection"
        )
        retriever = vectordb.as_retriever(search_kwargs={"k": 3})
        llm_rag = HuggingFacePipeline.from_model_id(
            model_id="EleutherAI/gpt-neo-1.3B",
            task="text-generation",
            device=0 if torch.cuda.is_available() else -1,
            pipeline_kwargs={"temperature": 0.2, "max_new_tokens": 20}, # max_new_tokens leicht reduziert
        )
        # NEUER, SIMPLERER PROMPT
        prompt = PromptTemplate(
            input_variables=["context", "question"],
            template=(
                "Verwende den folgenden Kontext, um die Frage zu beantworten:\n"
                "Kontext: {context}\n"
                "Frage: {question}\n"
                "Antwort:"
            )
        )
        qa = RetrievalQA.from_chain_type(
            llm=llm_rag,
            chain_type="stuff",
            retriever=retriever,
            chain_type_kwargs={"prompt": prompt},
            return_source_documents=False,
        )
        result = await asyncio.to_thread(qa.invoke, {"query": req.question})
        answer = result.get("result") or ""
        # Füge eine Nachbearbeitung hinzu, um möglicherweise den Prompt-Echo zu entfernen
        if "Antwort:" in answer:
            answer = answer.split("Antwort:", 1)[-1].strip()
        if "Kontext:" in answer: # Entferne auch Kontext-Echo, falls es auftritt
            answer = answer.split("Kontext:", 1)[-1].strip()
        
        # Entferne Wiederholungen (einfacher Ansatz)
        # Dies ist nur ein sehr einfacher Ansatz; für komplexere Wiederholungen bräuchte man mehr Logik
        # answer_parts = answer.split('.')
        # unique_parts = []
        # for part in answer_parts:
        #     if part.strip() not in unique_parts:
        #         unique_parts.append(part.strip())
        # answer = '. '.join(unique_parts) + ('.' if answer.endswith('.') else '')


        return {"answer": answer.strip()}
    except HTTPException as he:
        raise he
    except Exception as e:
        print(f"Fehler bei RAG-Abfrage: {e}")
        raise HTTPException(status_code=500, detail=f"Interner Fehler bei der RAG-Abfrage: {e}")
