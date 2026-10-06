import csv
import os


INPUT_FILE = os.path.join(
    os.path.dirname(os.path.dirname(__file__)),
    "dataset",
    "laptops_normalized.csv"
)


with open(INPUT_FILE, "r", encoding="utf-8", newline="") as file:
    reader = csv.DictReader(file)
    data = list(reader)


print("Total data:", len(data))

print("\nPerubahan processor:")
processor_changes = 0

for row in data:
    original = row["processor"]
    normalized = row["processor_normalized"]

    if original != normalized:
        processor_changes += 1
        print(f"- {original}")
        print(f"  -> {normalized}")

print("Jumlah processor berubah:", processor_changes)


print("\nPerubahan graphics:")
graphics_changes = 0

for row in data:
    original = row["graphics"]
    normalized = row["graphics_normalized"]

    if original != normalized:
        graphics_changes += 1
        print(f"- {original}")
        print(f"  -> {normalized}")

print("Jumlah graphics berubah:", graphics_changes)