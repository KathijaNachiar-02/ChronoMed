from huggingface_hub import hf_hub_download
import os

REPO_ID = "bavehackathon/2026-healthcare-ai"

FILES = [
    "clinical_cases.csv.gz",
    "labs_subset.csv.gz",
    "prescriptions_subset.csv.gz",
    "diagnoses_subset.csv.gz",
    "lab_dictionary.csv.gz",
    "diagnosis_dictionary.csv.gz"
]

OUTPUT_DIR = "datasets/clinical_ai"

os.makedirs(OUTPUT_DIR, exist_ok=True)

for filename in FILES:
    print(f"\nDownloading {filename}...")

    path = hf_hub_download(
        repo_id=REPO_ID,
        filename=filename,
        repo_type="dataset",
        local_dir=OUTPUT_DIR
    )

    print(f"Saved to: {path}")

print("\nAll files downloaded.")