from datasets import load_dataset

dataset = load_dataset(
    "mozay22/Discharge-summary-Fine-Tune"
)

print(dataset)

dataset.save_to_disk(
    "datasets/discharge"
)