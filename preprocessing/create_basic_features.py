import csv
import os
import re

dataset_path = os.path.join(
    os.path.dirname(os.path.dirname(__file__)),
    "dataset",
    "laptops_cleaned.csv"
)

output_path = os.path.join(
    os.path.dirname(os.path.dirname(__file__)),
    "dataset",
    "laptops_features.csv"
)


def parse_price(price):
    """
    Mengubah:
    Rp 9.350.000
    menjadi:
    9350000
    """
    if not price:
        return ""

    value = re.sub(r"[^\d]", "", price)

    return int(value) if value else ""


def parse_ram(memory):
    """
    Mengambil kapasitas RAM.

    Contoh:
    16GB LPDDR5X On Board -> 16
    8GB DDR4 -> 8
    """
    if not memory:
        return ""

    match = re.search(r"(\d+)\s*GB", memory, re.IGNORECASE)

    if match:
        return int(match.group(1))

    return ""


def parse_storage(storage):
    """
    Mengambil kapasitas storage dan mengubah TB menjadi GB.

    Contoh:
    512GB NVMe PCIe 4.0 SSD -> 512
    1TB NVMe SSD -> 1024
    """
    if not storage:
        return ""

    match = re.search(
        r"(\d+(?:\.\d+)?)\s*(TB|GB)",
        storage,
        re.IGNORECASE
    )

    if not match:
        return ""

    value = float(match.group(1))
    unit = match.group(2).upper()

    if unit == "TB":
        value *= 1024

    return int(value)


with open(dataset_path, "r", encoding="utf-8") as file:
    reader = csv.DictReader(file)
    data = list(reader)


for row in data:

    # Fitur numerik baru
    row["price_numeric"] = parse_price(row["price"])
    row["ram_gb"] = parse_ram(row["memory"])
    row["storage_gb"] = parse_storage(row["storage"])


fieldnames = [
    "name",
    "price",
    "price_numeric",
    "processor",
    "memory",
    "ram_gb",
    "storage",
    "storage_gb",
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
print("BASIC FEATURE ENGINEERING SELESAI")
print("========================================")
print("Total data:", len(data))
print("Output:", output_path)
print("========================================")