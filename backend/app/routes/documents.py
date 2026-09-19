from fastapi import APIRouter, UploadFile, File
import uuid
from pathlib import Path

from app.services.document_service import extract_text_from_file
from app.services.database_service import add_document, get_documents
from app.services.ml_service import process_with_ml

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
        # Extract text from the uploaded document
        text = extract_text_from_file(document["file_path"])

        # Send the extracted text to the ML service
        ml_result = process_with_ml(
            document_id=document_id,
            patient_id=document.get("patient_id"),
            text=text
        )

        # If ML is unavailable or fails
        if ml_result.get("status") == "failed":
            document["status"] = "failed"

            return {
                "document_id": document_id,
                "status": "failed",
                "error": ml_result.get(
                    "error",
                    "ML processing failed"
                )
            }

        # ML processing succeeded
        document["status"] = "processed"
        document["text_length"] = len(text)
        document["ml_result"] = ml_result

        return {
            "document_id": document_id,
            "status": "processed",
            "text_length": len(text),
            "ml_result": ml_result,
            "message": "Document processed successfully"
        }

    except Exception as error:
        document["status"] = "failed"

        return {
            "document_id": document_id,
            "status": "failed",
            "error": str(error)
        }