import csv
import os

dataset_path = os.path.join(
    os.path.dirname(os.path.dirname(__file__)),
    "dataset",
    "laptops_cleaned.csv"
)

with open(dataset_path, "r", encoding="utf-8") as file:
    reader = csv.DictReader(file)
    data = list(reader)

print("========================================")
print("VALIDASI DATASET CLEANED")
print("========================================")
print("Jumlah baris :", len(data))
print("Jumlah kolom :", len(reader.fieldnames))

print("\nKolom:")
for column in reader.fieldnames:
    print("-", column)


print("\n========================================")
print("DATA KOSONG")
print("========================================")

for column in reader.fieldnames:
    empty_count = 0

    for row in data:
        value = row[column]

        if value is None or value.strip() == "":
            empty_count += 1

    print(f"{column}: {empty_count} kosong")


print("\n========================================")
print("DATA APPLE")
print("========================================")

apple_count = 0

for index, row in enumerate(data, start=1):

    if row["name"].strip().lower().startswith("apple "):
        apple_count += 1

        print(f"\nBaris {index}")
        print("Name      :", row["name"])
        print("Processor :", row["processor"])
        print("Memory    :", row["memory"])
        print("Storage   :", row["storage"])
        print("Graphics  :", row["graphics"])
        print("CPU Cores :", row["cpu_cores"])
        print("GPU Cores :", row["gpu_cores"])


print("\n========================================")
print("RINGKASAN")
print("========================================")
print("Total data Apple:", apple_count)

print("\n========================================")
print("VALIDASI SELESAI")
print("========================================")