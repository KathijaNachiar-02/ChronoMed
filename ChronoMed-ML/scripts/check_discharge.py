from datasets import load_from_disk

dataset = load_from_disk(
    "datasets/discharge"
)

print(dataset)

for split in dataset.keys():

    print(
        split,
        len(dataset[split])
    )

print("\nFirst sample:")

print(
    dataset[list(dataset.keys())[0]][0]
)