from pathlib import Path
from pypdf import PdfReader


def extract_text_from_file(file_path: str) -> str:
    """
    Extract text from TXT and PDF files.
    """

    path = Path(file_path)

    # TXT file
    if path.suffix.lower() == ".txt":
        return path.read_text(encoding="utf-8")

    # PDF file
    if path.suffix.lower() == ".pdf":
        reader = PdfReader(str(path))

        text = ""

        for page in reader.pages:
            page_text = page.extract_text()

            if page_text:
                text += page_text + "\n"

        if not text.strip():
            raise ValueError(
                "PDF contains no extractable text. OCR is required."
            )

        return text

    raise ValueError(
        f"Unsupported file type: {path.suffix}. "
        "Currently supported: .txt and .pdf"
    )