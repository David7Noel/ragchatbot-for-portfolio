import os
import torch
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.config import settings
from app.utils.pdf_utils import extract_text_from_pdf

# Lokale Hugging Face Integrationen:
from langchain_huggingface.embeddings import HuggingFaceEmbeddings, HuggingFaceEndpointEmbeddings
from langchain_huggingface.llms import HuggingFacePipeline

from langchain_core.prompts import PromptTemplate
from langchain.chains import RetrievalQA

from langchain.schema import Document
from langchain.vectorstores import Chroma

router = APIRouter(prefix="/rag", tags=["RAG"])

class RagRequest(BaseModel):
    question: str
    doc_path: str

@router.post("/rag_query/")
async def rag_query(req: RagRequest):
    try:
        full_pdf_path = settings.BASE_DIR / req.doc_path
        if not full_pdf_path.is_file():
            raise HTTPException(status_code=400, detail=f"PDF nicht gefunden: {full_pdf_path}")

        lines = extract_text_from_pdf(str(full_pdf_path))
        if not lines:
            raise ValueError("❗ Kein Text aus PDF extrahiert.")

        # 🎯 Embeddings: Endpoint nutzen, wenn API-Token gesetzt ist
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
            chroma_mode="simple",
            collection_name="rag_pdf"
        )
        retriever = vectordb.as_retriever(search_kwargs={"k": 3})

        # 💡 GPT‑Neo (1.3B) lokal für generative Antworten
        llm = HuggingFacePipeline.from_model_id(
            model_id="EleutherAI/gpt-neo-1.3B",
            task="text-generation",
            device=0 if torch.cuda.is_available() else -1,
            pipeline_kwargs={"temperature": 0.2, "max_new_tokens": 150},
        )

        prompt = PromptTemplate(
            input_variables=["context", "question"],
            template=(
                "Du bist ein hilfreicher Dokument-Assistent.\n\n"
                "Hier ist relevanter Text aus deiner PDF:\n\n{context}\n\n"
                "Beantworte die Frage in max. 80 Wörtern (Deutsch oder Englisch):\n"
                "Frage: {question}\nAntwort:"
            )
        )

        qa = RetrievalQA.from_chain_type(
            llm=llm,
            chain_type="stuff",
            retriever=retriever,
            chain_type_kwargs={"prompt": prompt},
            return_source_documents=False,
        )

        result = qa({"query": req.question})
        answer = result.get("result") or ""
        return {"answer": answer.strip()}

    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal error: {e}")
