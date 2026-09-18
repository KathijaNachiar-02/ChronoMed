def process_with_ml(
    document_id: str,
    patient_id: str | None,
    text: str,
    document_date: str | None = None
):
    """
    Send document text to the ML inference module.

    This is a temporary connector.
    The real implementation will use ai/src/inference.py.
    """

    try:
        from ai.src.inference import process_document

        result = process_document(
            document_id=document_id,
            patient_id=patient_id,
            text=text,
            document_date=document_date
        )

        return result

    except Exception as error:
        return {
            "status": "failed",
            "error": str(error)
        }