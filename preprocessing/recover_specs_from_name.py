import csv
import os


dataset_path = os.path.join(
    os.path.dirname(os.path.dirname(__file__)),
    "dataset",
    "laptops_raw.csv"
)


def is_apple(name):
    return name.strip().lower().startswith("apple ")


def extract_specs_from_name(name):
    parts = [part.strip() for part in name.split("/")]

    if len(parts) < 4:
        return {}

    extracted = {
        "processor": parts[1],
        "memory": parts[2],
        "storage": parts[3],
    }

    if len(parts) >= 5:
        possible_graphics = parts[4]

        graphics_keywords = [
            "NVIDIA",
            "GeForce",
            "AMD Radeon",
            "Intel Graphics",
            "Intel UHD",
            "Intel Iris",
            "Intel Arc",
            "Radeon",
            "RTX",
            "GTX",
            "Arc ",
        ]

        if any(keyword.lower() in possible_graphics.lower()
               for keyword in graphics_keywords):
            extracted["graphics"] = possible_graphics

    return extracted


with open(dataset_path, "r", encoding="utf-8") as file:
    reader = csv.DictReader(file)
    data = list(reader)


print("========================================")
print("SIMULASI RECOVERY SPESIFIKASI")
print("========================================")

recovered_count = 0
apple_count = 0

for index, row in enumerate(data, start=1):

    name = row["name"]

    if is_apple(name):
        apple_count += 1
        continue

    missing_columns = []

    for column in ["processor", "memory", "storage", "graphics"]:
        if not row[column] or row[column].strip() == "":
            missing_columns.append(column)

    if not missing_columns:
        continue

    extracted = extract_specs_from_name(name)

    recovered = {}

    for column in missing_columns:
        value = extracted.get(column)

        if value:
            recovered[column] = value

    if recovered:
        recovered_count += 1

        print(f"\nBaris dataset: {index}")
        print("Name:", name)

        for column, value in recovered.items():
            print(f"{column}: {value}")


print("\n========================================")
print("HASIL SIMULASI")
print("========================================")
print("Total data:", len(data))
print("Data Apple yang dilewati:", apple_count)
print("Baris yang memiliki recovery:", recovered_count)
print("========================================")