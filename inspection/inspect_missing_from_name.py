import csv
import os

dataset_path = os.path.join(
    os.path.dirname(os.path.dirname(__file__)),
    "dataset",
    "laptops_raw.csv"
)

with open(dataset_path, "r", encoding="utf-8") as file:
    reader = csv.DictReader(file)
    data = list(reader)

spec_columns = [
    "processor",
    "memory",
    "storage",
    "graphics"
]

print("========================================")
print("DATA DENGAN MISSING VALUE")
print("========================================")

count = 0

for index, row in enumerate(data, start=1):

    missing_columns = []

    for column in spec_columns:
        if not row[column] or row[column].strip() == "":
            missing_columns.append(column)

    if missing_columns:
        count += 1

        print(f"\nBaris dataset: {index}")
        print("Missing:", ", ".join(missing_columns))
        print("Name   :", row["name"])
        print("Processor:", row["processor"])
        print("Memory   :", row["memory"])
        print("Storage  :", row["storage"])
        print("Graphics :", row["graphics"])

print("\n========================================")
print("TOTAL BARIS DENGAN MISSING:", count)
print("========================================")