# app.py
import gradio as gr
import requests
import os

# FastAPI läuft im Space automatisch unter Port 8000 (Standard),
# die Gradio-Launch landet auf Port 7860.
API_URL = "/rag/rag_query/"

def chat_fn(question: str) -> str:
    try:
        resp = requests.post(API_URL, json={
            "question": question,
            "doc_path": "assets/test_capital_of.pdf"
        }, timeout=25)
        data = resp.json()
        return data.get("answer", "Keine Antwort erhalten")
    except Exception as e:
        return f"⚠️ Fehler: {e}"

iface = gr.Interface(
    fn=chat_fn,
    inputs=gr.Textbox(lines=2, placeholder="Frage an das PDF…"),
    outputs="text",
    title="Portfolio RAG‑Chatbot",
    description="Stelle Fragen zum PDF‑Inhalt.",
    allow_flagging="never"
)

if __name__ == "__main__":
    iface.launch(server_name="0.0.0.0", server_port=7860)
