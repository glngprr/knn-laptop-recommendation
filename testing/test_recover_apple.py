import csv
import os
import re


dataset_path = os.path.join(
    os.path.dirname(os.path.dirname(__file__)),
    "dataset",
    "laptops_recovered.csv"
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
        extracted["cpu_cores"] = int(cpu_match.group(1))

    # GPU cores
    gpu_match = re.search(
        r"(\d+)-core GPU",
        name,
        re.IGNORECASE
    )

    if gpu_match:
        extracted["gpu_cores"] = int(gpu_match.group(1))

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


print("========================================")
print("SIMULASI RECOVERY APPLE")
print("========================================")


apple_count = 0
successful_count = 0


for index, row in enumerate(data, start=1):

    name = row["name"]

    if not name.strip().lower().startswith("apple "):
        continue

    apple_count += 1

    extracted = extract_apple_specs(name)

    if extracted:
        successful_count += 1

    print(f"\nBaris dataset: {index}")
    print("Name:", name)

    print("Hasil ekstraksi:")

    for key, value in extracted.items():
        print(f"  {key}: {value}")


print("\n========================================")
print("HASIL SIMULASI")
print("========================================")
print("Total data Apple:", apple_count)
print("Apple berhasil diekstrak:", successful_count)
print("Apple gagal diekstrak:", apple_count - successful_count)
print("========================================")