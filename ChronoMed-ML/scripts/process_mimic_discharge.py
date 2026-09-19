import pandas as pd
import json
import os

INPUT = "datasets/mimic/discharge.csv"

OUTPUT = (
    "processed/extraction/"
    "mimic_discharge.jsonl"
)

df = pd.read_csv(INPUT)

print("Rows:", len(df))

print(
    "Columns:",
    df.columns.tolist()
)

os.makedirs(
    "processed/extraction",
    exist_ok=True
)

with open(
    OUTPUT,
    "w",
    encoding="utf-8"
) as f:

    for _, row in df.iterrows():

        item = {
            "document_id": str(row["note_id"]),
            "patient_id": str(row["subject_id"]),
            "admission_id": str(row["hadm_id"]),
            "document_type": "DISCHARGE_SUMMARY",
            "date": str(row["charttime"]),
            "text": str(row["text"])
        }

        f.write(
            json.dumps(
                item,
                ensure_ascii=False
            ) + "\n"
        )

print("Saved:", OUTPUT)