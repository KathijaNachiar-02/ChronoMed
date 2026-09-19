from datasets import load_from_disk

dataset = load_from_disk(
    "datasets/ekacare"
)

print(dataset)

test = dataset["test"]

print("\nNumber of samples:")
print(len(test))

print("\nColumns:")
print(test.column_names)

print("\nFirst sample:")
print(test[0])