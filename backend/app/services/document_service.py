from pathlib import Path


def extract_text_from_file(file_path: str) -> str:
    """
    Extract text from a simple text file.
    """

    path = Path(file_path)

    if path.suffix.lower() == ".txt":
        return path.read_text(encoding="utf-8")

    raise ValueError(
        f"Unsupported file type: {path.suffix}. "
        "Currently only .txt files are supported."
    )