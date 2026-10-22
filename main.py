from fastapi import FastAPI, UploadFile, File
import os

from ocr.ocr_service import process_certificate
from database import save_certificate
from hash_service import calculate_file_hash


app = FastAPI()

UPLOAD_FOLDER = "uploads"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@app.get("/")
def home():
    return {
        "message": "Degree Verification Backend is running!"
    }


@app.post("/verify")
async def verify_certificate(file: UploadFile = File(...)):

    # -------------------------
    # 1. Save uploaded file
    # -------------------------

    file_path = os.path.join(
        UPLOAD_FOLDER,
        file.filename
    )

    with open(file_path, "wb") as buffer:
        content = await file.read()
        buffer.write(content)

    # -------------------------
    # 2. Process certificate
    # -------------------------

    result = process_certificate(file_path)

    certificate_data = result["certificate_data"]

    # -------------------------
    # 3. Calculate SHA-256 hash
    # -------------------------

    certificate_hash = calculate_file_hash(file_path)

    # -------------------------
    # 4. Save data + hash
    #    to PostgreSQL
    # -------------------------

    database_id = save_certificate(
        certificate_data,
        certificate_hash
    )

    # -------------------------
    # 5. Return result
    # -------------------------

    return {
        "message": "Certificate processed and saved successfully!",
        "database_id": database_id,
        "filename": file.filename,
        "certificate_hash": certificate_hash,
        "ocr_text": result["ocr_text"],
        "certificate_data": certificate_data
    }