import csv
import os

dataset_path = os.path.join(
    os.path.dirname(os.path.dirname(__file__)),
    "dataset",
    "laptops_features.csv"
)

with open(dataset_path, "r", encoding="utf-8") as file:
    reader = csv.DictReader(file)
    data = list(reader)

print("========================================")
print("VALIDASI BASIC FEATURES")
print("========================================")

print("Jumlah baris :", len(data))
print("Jumlah kolom :", len(reader.fieldnames))

print("\nKolom:")
for column in reader.fieldnames:
    print("-", column)


print("\n========================================")
print("DATA KOSONG PADA FITUR NUMERIK")
print("========================================")

numeric_columns = [
    "price_numeric",
    "ram_gb",
    "storage_gb"
]

for column in numeric_columns:

    empty_count = 0

    for row in data:
        if row[column] is None or row[column].strip() == "":
            empty_count += 1

    print(f"{column}: {empty_count} kosong")


print("\n========================================")
print("CONTOH DATA")
print("========================================")

for index, row in enumerate(data[:10], start=1):

    print(f"\nData {index}")
    print("Name          :", row["name"])
    print("Price         :", row["price"])
    print("Price Numeric :", row["price_numeric"])
    print("Memory        :", row["memory"])
    print("RAM GB        :", row["ram_gb"])
    print("Storage       :", row["storage"])
    print("Storage GB    :", row["storage_gb"])


print("\n========================================")
print("RENTANG FITUR NUMERIK")
print("========================================")

for column in numeric_columns:

    values = []

    for row in data:
        value = row[column]

        if value and value.strip():
            values.append(float(value))

    if values:
        print(f"\n{column}")
        print("Minimum :", min(values))
        print("Maximum :", max(values))
        print("Jumlah  :", len(values))


print("\n========================================")
print("VALIDASI SELESAI")
print("========================================")