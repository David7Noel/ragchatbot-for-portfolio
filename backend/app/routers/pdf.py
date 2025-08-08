from fastapi import APIRouter, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from app.utils.pdf_utils import extract_text_from_pdf
import os
import tempfile
from app.routers.langchain import rag_system # Import the global RAGSystem instance

# KORRIGIERTE ZEILE: Entferne prefix="/pdf" von hier
router = APIRouter(tags=["PDF"])

@router.post("/process_pdf/")
async def process_pdf(file: UploadFile = File(...)):
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Nur PDF-Dateien erlaubt.")

    tmp_file_path = ""
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
            contents = await file.read()
            tmp.write(contents)
            tmp_file_path = tmp.name

        await rag_system.load_pdf(tmp_file_path)

        return JSONResponse(content={"message": f"PDF '{file.filename}' erfolgreich verarbeitet und für den Chat geladen."})

    except Exception as e:
        print(f"Fehler beim Verarbeiten/Laden des PDFs: {e}")
        raise HTTPException(status_code=400, detail=f"Fehler beim Verarbeiten oder Laden der PDF-Datei: {e}")
    finally:
        if os.path.exists(tmp_file_path):
            os.unlink(tmp_file_path)
