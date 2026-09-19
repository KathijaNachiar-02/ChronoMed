from datasets import load_dataset

dataset = load_dataset(
    "Rockerleo/medical-doc-classification-llama3"
)

print(dataset)

dataset.save_to_disk(
    "datasets/classifier"
)