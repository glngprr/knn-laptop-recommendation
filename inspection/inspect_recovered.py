import csv
import os


dataset_path = os.path.join(
    os.path.dirname(os.path.dirname(__file__)),
    "dataset",
    "laptops_recovered.csv"
)


with open(dataset_path, "r", encoding="utf-8") as file:
    reader = csv.DictReader(file)
    data = list(reader)


print("========================================")
print("VALIDASI DATASET RECOVERED")
print("========================================")
print("Jumlah baris :", len(data))
print("Jumlah kolom :", len(reader.fieldnames))


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
print("MISSING VALUE SPESIFIKASI")
print("========================================")

spec_columns = [
    "processor",
    "memory",
    "storage",
    "graphics"
]

for column in spec_columns:

    print(f"\n{column.upper()} yang masih kosong:")

    count = 0

    for index, row in enumerate(data, start=1):

        if not row[column] or row[column].strip() == "":
            count += 1

            print(f"Baris {index}: {row['name']}")

    print("Total:", count)


print("\n========================================")
print("VALIDASI SELESAI")
print("========================================")