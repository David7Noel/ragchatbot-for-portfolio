import json
from pathlib import Path
import sys

# Dies ist der Pfad zu deinem Modellordner
# Stelle sicher, dass dieser Pfad korrekt ist!
model_dir_path = Path(
    r"C:\xampp\htdocs\meine_projekte\RAG-Chatbot_mit_Portfolio-Integration\backend\local_models\Mistral-7B-Instruct-v0.2")

config_file_path = model_dir_path / "config.json"

print(f"Überprüfe config.json unter: {config_file_path}")

if config_file_path.exists():
    print(f"config.json existiert: {config_file_path}")
    try:
        with open(config_file_path, 'r', encoding='utf-8') as f:
            config_content = f.read()
            print(f"Inhalt der config.json (erste 200 Zeichen): {config_content[:200]}...")
            print(f"Länge der config.json: {len(config_content)} Zeichen")

            # Versuche, es als JSON zu parsen
            json_data = json.loads(config_content)
            print("config.json ist gültiges JSON.")

            # Optional: Einige Schlüssel aus der Konfiguration ausgeben
            if "model_type" in json_data:
                print(f"Model-Typ in config.json: {json_data['model_type']}")
            if "architectures" in json_data:
                print(f"Architekturen in config.json: {json_data['architectures']}")

    except json.JSONDecodeError as e:
        print(f"FEHLER: config.json ist kein gültiges JSON. Fehler: {e}")
        print("Bitte stelle sicher, dass die Datei vollständig und unbeschädigt heruntergeladen wurde.")
    except Exception as e:
        print(f"Fehler beim Lesen/Parsen der config.json: {e}")
else:
    print(f"FEHLER: config.json NICHT gefunden unter: {config_file_path}")
    print("Bitte stelle sicher, dass der Pfad korrekt ist und die Datei dort liegt.")

print("\n--- Überprüfung abgeschlossen ---")

