import pandas as pd

base = "datasets/clinical_ai/"

cases = pd.read_csv(
    base + "clinical_cases.csv.gz"
)

labs = pd.read_csv(
    base + "labs_subset.csv.gz"
)

prescriptions = pd.read_csv(
    base + "prescriptions_subset.csv.gz"
)

diagnoses = pd.read_csv(
    base + "diagnoses_subset.csv.gz"
)

lab_dictionary = pd.read_csv(
    base + "lab_dictionary.csv.gz"
)

diagnosis_dictionary = pd.read_csv(
    base + "diagnosis_dictionary.csv.gz"
)

print("\n===== CLINICAL CASES =====")
print(cases.shape)
print(cases.columns.tolist())

print("\n===== LABS =====")
print(labs.shape)
print(labs.columns.tolist())

print("\n===== PRESCRIPTIONS =====")
print(prescriptions.shape)
print(prescriptions.columns.tolist())

print("\n===== DIAGNOSES =====")
print(diagnoses.shape)
print(diagnoses.columns.tolist())

print("\n===== SAMPLE CASE =====")
print(cases.iloc[0])

print("\n===== SAMPLE LAB =====")
print(labs.iloc[0])

print("\n===== SAMPLE PRESCRIPTION =====")
print(prescriptions.iloc[0])