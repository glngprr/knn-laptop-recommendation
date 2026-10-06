import csv
import os


dataset_path = os.path.join(
    os.path.dirname(os.path.dirname(__file__)),
    "dataset",
    "laptops_raw.csv"
)

output_path = os.path.join(
    os.path.dirname(os.path.dirname(__file__)),
    "dataset",
    "laptops_recovered.csv"
)


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

        if any(
            keyword.lower() in possible_graphics.lower()
            for keyword in graphics_keywords
        ):
            extracted["graphics"] = possible_graphics

    return extracted


with open(dataset_path, "r", encoding="utf-8") as file:
    reader = csv.DictReader(file)
    data = list(reader)


recovered_count = 0

for row in data:

    name = row["name"]

    # Apple belum diproses pada tahap ini
    if name.strip().lower().startswith("apple "):
        continue

    missing_columns = []

    for column in ["processor", "memory", "storage", "graphics"]:
        if not row[column] or row[column].strip() == "":
            missing_columns.append(column)

    if not missing_columns:
        continue

    extracted = extract_specs_from_name(name)

    for column in missing_columns:
        value = extracted.get(column)

        if value:
            row[column] = value
            recovered_count += 1


with open(output_path, "w", newline="", encoding="utf-8") as file:
    writer = csv.DictWriter(
        file,
        fieldnames=[
            "name",
            "price",
            "processor",
            "memory",
            "storage",
            "graphics",
            "url"
        ]
    )

    writer.writeheader()
    writer.writerows(data)


print("========================================")
print("RECOVERY SELESAI")
print("========================================")
print("Total data:", len(data))
print("Nilai yang berhasil dipulihkan:", recovered_count)
print("Output:", output_path)
print("========================================")