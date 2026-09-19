from datasets import load_dataset

print("Loading prescription OCR dataset...")

dataset = load_dataset(
    "chinmays18/medical-prescription-dataset"
)

print(dataset)

print("train samples =", len(dataset["train"]))
print("validation samples =", len(dataset["validation"]))
print("test samples =", len(dataset["test"]))

print("\nFirst training sample:")
sample = dataset["train"][0]

print(sample.keys())
print(sample["ground_truth"])