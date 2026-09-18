from fastapi import APIRouter, UploadFile, File
import uuid
from pathlib import Path

from app.services.document_service import extract_text_from_file
from app.services.database_service import add_document, get_documents

router = APIRouter(
    prefix="/api/documents",
    tags=["Documents"]
)

UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)


@router.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    document_id = str(uuid.uuid4())

    file_path = UPLOAD_DIR / f"{document_id}_{file.filename}"

    file_content = await file.read()
    file_path.write_bytes(file_content)

    document = {
        "id": document_id,
        "filename": file.filename,
        "status": "uploaded",
        "patient_id": None,
        "file_path": str(file_path),
    }

    add_document(document)

    return document


@router.get("")
def list_documents():
    return get_documents()

@router.get("/{document_id}")
def get_document(document_id: str):
    documents = get_documents()

    document = next(
        (doc for doc in documents if doc["id"] == document_id),
        None
    )

    if document is None:
        return {
            "error": "Document not found"
        }

    return document

@router.post("/{document_id}/process")
def process_uploaded_document(document_id: str):
    documents = get_documents()

    document = next(
        (doc for doc in documents if doc["id"] == document_id),
        None
    )

    if document is None:
        return {
            "error": "Document not found"
        }

    try:
        text = extract_text_from_file(document["file_path"])

        document["status"] = "processed"
        document["text_length"] = len(text)

        return {
            "document_id": document_id,
            "status": "processed",
            "text_length": len(text),
            "message": "Document text extracted successfully"
        }

    except Exception as error:
        document["status"] = "failed"

        return {
            "document_id": document_id,
            "status": "failed",
            "error": str(error)
        }