import csv
import os
import re

dataset_path = os.path.join(
    os.path.dirname(os.path.dirname(__file__)),
    "dataset",
    "laptops_recovered.csv"
)

output_path = os.path.join(
    os.path.dirname(os.path.dirname(__file__)),
    "dataset",
    "laptops_cleaned.csv"
)


def extract_apple_specs(name):
    extracted = {}

    # Processor
    processor_match = re.search(
        r"\b((?:A18 Pro|M[1-5](?:\s+(?:Pro|Max))?))\b",
        name,
        re.IGNORECASE
    )

    if processor_match:
        extracted["processor"] = processor_match.group(1)

    # CPU cores
    cpu_match = re.search(
        r"(\d+)-core CPU",
        name,
        re.IGNORECASE
    )

    if cpu_match:
        extracted["cpu_cores"] = cpu_match.group(1)

    # GPU cores
    gpu_match = re.search(
        r"(\d+)-core GPU",
        name,
        re.IGNORECASE
    )

    if gpu_match:
        extracted["gpu_cores"] = gpu_match.group(1)

    # Memory
    memory_match = re.search(
        r"(\d+)\s*GB",
        name,
        re.IGNORECASE
    )

    if memory_match:
        extracted["memory"] = memory_match.group(1) + "GB"

    # Storage
    storage_match = re.search(
        r"(\d+)\s*(GB|TB)\s*SSD",
        name,
        re.IGNORECASE
    )

    if storage_match:
        extracted["storage"] = (
            storage_match.group(1)
            + storage_match.group(2).upper()
            + " SSD"
        )

    return extracted


with open(dataset_path, "r", encoding="utf-8") as file:
    reader = csv.DictReader(file)
    data = list(reader)


for row in data:

    # Default kosong
    row["cpu_cores"] = ""
    row["gpu_cores"] = ""

    name = row["name"]

    # Hanya gunakan parser khusus untuk Apple
    if name.strip().lower().startswith("apple "):

        extracted = extract_apple_specs(name)

        # Isi hanya jika data sebelumnya kosong
        if not row["processor"] and extracted.get("processor"):
            row["processor"] = extracted["processor"]

        if not row["memory"] and extracted.get("memory"):
            row["memory"] = extracted["memory"]

        if not row["storage"] and extracted.get("storage"):
            row["storage"] = extracted["storage"]

        if extracted.get("cpu_cores"):
            row["cpu_cores"] = extracted["cpu_cores"]

        if extracted.get("gpu_cores"):
            row["gpu_cores"] = extracted["gpu_cores"]


fieldnames = [
    "name",
    "price",
    "processor",
    "memory",
    "storage",
    "graphics",
    "cpu_cores",
    "gpu_cores",
    "url"
]


with open(output_path, "w", newline="", encoding="utf-8") as file:
    writer = csv.DictWriter(
        file,
        fieldnames=fieldnames
    )

    writer.writeheader()
    writer.writerows(data)


print("========================================")
print("RECOVERY APPLE SELESAI")
print("========================================")
print("Total data:", len(data))
print("Output:", output_path)
print("========================================")