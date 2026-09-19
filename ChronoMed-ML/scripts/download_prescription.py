from huggingface_hub import snapshot_download

print("Downloading prescription OCR dataset files...")

snapshot_download(
    repo_id="chinmays18/medical-prescription-dataset",
    repo_type="dataset",
    local_dir="datasets/prescription_raw",
)

print("Dataset files downloaded successfully.")