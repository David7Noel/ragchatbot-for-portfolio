from fastapi import APIRouter, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from app.utils.pdf_utils import extract_text_from_pdf
import os
import tempfile

router = APIRouter()

@router.post("/process_pdf/")
async def process_pdf(file: UploadFile = File(...)):
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Nur PDF-Dateien erlaubt.")
    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
    contents = await file.read()
    tmp.write(contents)
    tmp.flush()
    tmp.close()

    try:
        text_lines = extract_text_from_pdf(tmp.name)
        os.unlink(tmp.name)
        return JSONResponse(content={"text": text_lines})
    except HTTPException:
        os.unlink(tmp.name)
        raise
    except Exception as e:
        os.unlink(tmp.name)
        raise HTTPException(status_code=400, detail=str(e))
