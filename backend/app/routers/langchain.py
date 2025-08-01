from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain
from langchain_community.embeddings.openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_community.llms import OpenAI
from app.utils.pdf_utils import extract_text_from_pdf
import os

router = APIRouter()

class RagRequest(BaseModel):
    question: str
    doc_path: str

@router.post("/rag_query/")
async def rag_query(req: RagRequest):
    try:
        docs = extract_text_from_pdf(req.doc_path)
        embeddings = OpenAIEmbeddings(openai_api_key=os.getenv("OPENAI_API_KEY"))
        vectordb = Chroma.from_texts(texts=docs, embedding=embeddings)
        retriever = vectordb.as_retriever(search_kwargs={"k": 3})

        prompt = ChatPromptTemplate.from_messages([
            ("system", "Use retrieved context to answer concisely. Context: {context}"),
            ("human", "{input}")
        ])
        llm = OpenAI(openai_api_key=os.getenv("OPENAI_API_KEY"))
        doc_chain = create_stuff_documents_chain(llm=llm, prompt=prompt)
        retrieval_chain = create_retrieval_chain(retriever=retriever, combine_docs_chain=doc_chain)

        result = retrieval_chain.invoke({"input": req.question})
        return {"answer": result.get("answer", "No answer generated")}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
