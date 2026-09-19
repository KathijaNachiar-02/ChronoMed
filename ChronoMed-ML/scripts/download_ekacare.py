from datasets import load_dataset

print("Loading EkaCare dataset...")

dataset = load_dataset(
    "ekacare/medical_records_parsing_validation_set"
)

print(dataset)

dataset.save_to_disk(
    "datasets/ekacare"
)

print("EkaCare dataset saved.")