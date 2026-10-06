import csv
import os
from collections import Counter


INPUT_FILE = os.path.join(
    os.path.dirname(os.path.dirname(__file__)),
    "dataset",
    "laptops_normalized.csv"
)


with open(INPUT_FILE, "r", encoding="utf-8", newline="") as file:
    reader = csv.DictReader(file)
    data = list(reader)


processor_counter = Counter(
    row["processor_normalized"]
    for row in data
    if row["processor_normalized"]
)

graphics_counter = Counter(
    row["graphics_normalized"]
    for row in data
    if row["graphics_normalized"]
)


print("=" * 60)
print("INVENTORY HARDWARE SETELAH NORMALISASI")
print("=" * 60)

print("\nTotal laptop:", len(data))

print("\nUnique processor:", len(processor_counter))
print("Unique graphics:", len(graphics_counter))


print("\n" + "=" * 60)
print("PROCESSOR")
print("=" * 60)

for processor, count in processor_counter.most_common():
    print(f"{count:>3}x  {processor}")


print("\n" + "=" * 60)
print("GRAPHICS")
print("=" * 60)

for graphics, count in graphics_counter.most_common():
    print(f"{count:>3}x  {graphics}")