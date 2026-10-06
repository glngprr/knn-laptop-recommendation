import csv
import os
from collections import Counter


dataset_path = os.path.join(
    os.path.dirname(os.path.dirname(__file__)),
    "dataset",
    "laptops_features.csv"
)


with open(dataset_path, "r", encoding="utf-8") as file:
    reader = csv.DictReader(file)
    data = list(reader)


# ========================================
# PROCESSOR
# ========================================

processors = Counter(
    row["processor"]
    for row in data
    if row["processor"] and row["processor"].strip()
)


print("========================================")
print("INVENTARIS PROCESSOR")
print("========================================")

print("Jumlah model processor unik:", len(processors))

for processor, count in processors.most_common():
    print(f"{count:>3}x | {processor}")


# ========================================
# GRAPHICS
# ========================================

graphics = Counter(
    row["graphics"]
    for row in data
    if row["graphics"] and row["graphics"].strip()
)


print("\n========================================")
print("INVENTARIS GRAPHICS")
print("========================================")

print("Jumlah model graphics unik:", len(graphics))

for graphic, count in graphics.most_common():
    print(f"{count:>3}x | {graphic}")


print("\n========================================")
print("RINGKASAN")
print("========================================")
print("Total data          :", len(data))
print("Processor unik      :", len(processors))
print("Graphics unik       :", len(graphics))
print("========================================")