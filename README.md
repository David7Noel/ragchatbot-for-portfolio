💬 Einfacher Chatbot mit Ollama, FastAPI und Gradio – Lokale LLM-Inferenz
Willkommen zu meinem neuesten Projekt: Ein minimalistischer Full-Stack-Chatbot, der ein großes Sprachmodell (LLM) komplett lokal ausführt! In diesem Video zeige ich dir, wie dieser Chatbot funktioniert und welche Technologien dahinterstecken.

✨ Funktionen
Lokale LLM-Inferenz: Nutzt Ollama, um große Sprachmodelle (LLMs) wie Gemma oder Llama 2 direkt auf deinem Computer auszuführen – keine Cloud-APIs, keine Kosten, maximaler Datenschutz!

Full-Stack-Architektur:

Backend: Robuste RESTful API mit FastAPI.

Frontend: Intuitive Web-Oberfläche mit Gradio.

Einfache Interaktion: Eine benutzerfreundliche Chat-Schnittstelle zum Stellen von Fragen an das LLM.

Kostenfrei & Datenschutzfreundlich: Da das LLM lokal läuft, fallen keine API-Kosten an und deine Daten verlassen deinen Rechner nicht.

## 🎬 Demo

Schau dir eine kurze Video-Demo des Chatbots in Aktion an:

[![Chatbot Demo Video](https://img.youtube.com/vi/2egz-IzPhmo/0.jpg)](https://www.youtube.com/watch?v=2egz-IzPhmo)
*(Hinweis: Das Vorschaubild wird automatisch von YouTube generiert. Der Link führt direkt zum Video.)*

🛠️ Lokale Einrichtung
Befolge diese Schritte, um den Chatbot auf deinem lokalen Computer einzurichten und auszuführen.

Voraussetzungen
Python 3.10.11 installiert.

Ollama für dein Betriebssystem installiert.

Ein Hugging Face User Access Token (mit "Read"-Rechten), da langchain-huggingface dies intern für einige Funktionen verwendet. Diesen Token wirst du als Umgebungsvariable setzen.

1. Ollama Modell herunterladen
Öffne ein Terminal und lade das gewünschte LLM-Modell herunter. Wir empfehlen gemma:2b für eine gute Balance zwischen Leistung und Qualität auf CPUs:

ollama run gemma:2b

Warte, bis der Download abgeschlossen ist, und gib dann /bye ein, um die Ollama-Sitzung zu beenden. Stelle sicher, dass der Ollama-Dienst im Hintergrund läuft (normalerweise startet er automatisch nach der Installation).

2. Projekt klonen und navigieren
Wenn du das Projekt bereits geklont hast, überspringe diesen Schritt. Andernfalls klone dieses Repository auf deinen lokalen Computer und navigiere in das Projektverzeichnis:

git clone [https://github.com/DEIN_GITHUB_USERNAME/DEIN_REPO_NAME.git](https://github.com/DEIN_GITHUB_USERNAME/DEIN_REPO_NAME.git)
cd DEIN_REPO_NAME

(Ersetze DEIN_GITHUB_USERNAME und DEIN_REPO_NAME durch deine tatsächlichen Werte)

3. Virtuelles Environment einrichten
Erstelle ein virtuelles Python-Environment und aktiviere es:

python -m venv venv
# Auf Windows PowerShell:
.\venv\Scripts\activate.ps1
# Auf macOS/Linux:
source venv/bin/activate

4. Abhängigkeiten installieren
Installiere alle benötigten Python-Pakete aus der requirements.txt:

pip install -r requirements.txt

5. Umgebungsvariablen setzen
Bevor du das Backend startest, musst du deinen Hugging Face API Token als Umgebungsvariable setzen. Dies ist notwendig für die langchain-huggingface Bibliothek, auch wenn wir hauptsächlich Ollama nutzen.

# Auf Windows PowerShell:
$env:HUGGINGFACEHUB_API_TOKEN="DEIN_HUGGING_FACE_TOKEN"

# Auf macOS/Linux:
export HUGGINGFACEHUB_API_TOKEN="DEIN_HUGGING_FACE_TOKEN"

(Ersetze DEIN_HUGGING_FACE_TOKEN durch deinen tatsächlichen Token.)

6. Anwendung starten
Öffne drei separate Terminalfenster und führe die folgenden Befehle aus:

Terminal 1: Ollama Server (Muss bereits laufen oder gestartet werden)
Stelle sicher, dass der Ollama-Dienst im Hintergrund läuft. Wenn er nicht automatisch startet, kannst du ihn manuell starten:

ollama serve

(Dieser Befehl muss während der Nutzung des Chatbots aktiv bleiben.)

Terminal 2: FastAPI Backend starten
Navigiere in das backend-Verzeichnis und starte den FastAPI-Server:

cd backend
python -m uvicorn app.main:app --reload

(Warte auf die Meldung INFO: Application startup complete.)

Terminal 3: Gradio Frontend starten
Navigiere zurück in das Hauptprojektverzeichnis und starte die Gradio-Anwendung:

cd .. # Falls du noch im Backend-Ordner bist
python gradio_app.py

(Öffne dann die angezeigte URL in deinem Webbrowser, normalerweise http://127.0.0.1:7860)

💡 Hinweise zur Performance
Die Geschwindigkeit der Antworten hängt stark von der Leistung deiner CPU und dem verwendeten LLM-Modell ab. Für optimale Leistung auf CPU-basierten Systemen wird die Verwendung von kleineren oder quantisierten Modellen wie gemma:2b empfohlen.

🤝 Mitwirken
Fühle dich frei, Issues zu öffnen oder Pull Requests einzureichen, um dieses Projekt zu verbessern.

📄 Lizenz
Dieses Projekt steht unter der MIT-Lizenz.