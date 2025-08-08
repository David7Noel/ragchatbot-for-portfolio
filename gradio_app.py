import gradio as gr
import requests
import json

FASTAPI_URL = "http://127.0.0.1:8000"

def chat_with_bot(message, history):
    """
    Sendet eine Chat-Nachricht an das FastAPI-Backend und empfängt eine Antwort.
    """
    try:
        response = requests.post(f"{FASTAPI_URL}/chat/chat_query/", json={"message": message})
        response.raise_for_status() # Löst eine Ausnahme für HTTP-Fehler (4xx oder 5xx) aus
        data = response.json()
        return data.get("answer", "Entschuldigung, ich konnte keine Antwort erhalten.")
    except requests.exceptions.ConnectionError:
        return "Fehler: Konnte keine Verbindung zum Backend herstellen. Stelle sicher, dass das FastAPI-Backend läuft."
    except requests.exceptions.Timeout:
        return "Fehler: Die Anfrage an das Backend hat zu lange gedauert."
    except requests.exceptions.HTTPError as e:
        return f"Fehler vom Backend: {e.response.status_code} - {e.response.text}"
    except json.JSONDecodeError:
        return "Fehler: Ungültige JSON-Antwort vom Backend."
    except Exception as e:
        return f"Ein unerwarteter Fehler ist aufgetreten: {e}"

with gr.Blocks() as demo:
    gr.Markdown("# 💬 Einfacher Chatbot")
    gr.ChatInterface(
        fn=chat_with_bot,
        chatbot=gr.Chatbot(height=400),
        # clear_btn und submit_btn wurden entfernt, da sie in neueren Gradio-Versionen nicht direkt unterstützt werden
        # Die Warnung bezüglich des `type`-Parameters für `chatbot` ist ebenfalls behoben, indem wir ihn entfernen.
        textbox=gr.Textbox(placeholder="Stelle mir eine Frage...", container=False, scale=7),
        examples=["Hallo, wie geht es dir?", "Erzähl mir einen Witz.", "Was ist das Wetter heute?"],
        title="Einfacher Chatbot",
        description="Stelle mir eine Frage und ich werde versuchen, sie zu beantworten."
    )

demo.launch()
