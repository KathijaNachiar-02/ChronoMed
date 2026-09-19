import pandas as pd
import json
import os

BASE = "datasets/clinical_ai/"

cases = pd.read_csv(
    BASE + "clinical_cases.csv.gz"
)

labs = pd.read_csv(
    BASE + "labs_subset.csv.gz"
)

prescriptions = pd.read_csv(
    BASE + "prescriptions_subset.csv.gz"
)

lab_dictionary = pd.read_csv(
    BASE + "lab_dictionary.csv.gz"
)

# Add lab names
labs = labs.merge(
    lab_dictionary[["itemid", "lab_name"]],
    on="itemid",
    how="left"
)

events = []

# -------------------------
# DISCHARGE SUMMARY EVENTS
# -------------------------

for _, row in cases.iterrows():

    events.append({
        "patient_id": str(row["subject_id"]),
        "admission_id": str(row["hadm_id"]),
        "event_type": "DISCHARGE_SUMMARY",
        "date": None,
        "source": "clinical_cases.csv.gz",
        "text": str(row["discharge_summary"])
    })


# -------------------------
# LAB EVENTS
# -------------------------

for _, row in labs.iterrows():

    events.append({
        "patient_id": None,
        "admission_id": str(row["hadm_id"]),
        "event_type": "LAB_RESULT",
        "date": str(row["charttime"]),
        "lab_test": str(row["lab_name"]),
        "value": row["value"],
        "unit": str(row["unit"]),
        "source": "labs_subset.csv.gz"
    })


# -------------------------
# PRESCRIPTION EVENTS
# -------------------------

for _, row in prescriptions.iterrows():

    events.append({
        "patient_id": str(row["subject_id"]),
        "admission_id": str(row["hadm_id"]),
        "event_type": "MEDICATION",
        "date": str(row["startdate"]),
        "medication": str(row["drug"]),
        "dosage": str(row["dose_value"]),
        "dose_unit": str(row["dose_unit"]),
        "route": str(row["route"]),
        "source": "prescriptions_subset.csv.gz"
    })


os.makedirs(
    "processed/extraction",
    exist_ok=True
)

with open(
    "processed/extraction/clinical_events.jsonl",
    "w",
    encoding="utf-8"
) as f:

    for event in events:
        f.write(
            json.dumps(
                event,
                default=str
            ) + "\n"
        )

print(f"Created {len(events)} events.")