import csv
import os
from collections import Counter


# ==========================================
# 1. Menentukan lokasi dataset
# ==========================================

dataset_path = os.path.join(
    os.path.dirname(os.path.dirname(__file__)),
    "dataset",
    "laptops_raw.csv"
)


# ==========================================
# 2. Membaca dataset
# ==========================================

with open(
    dataset_path,
    "r",
    encoding="utf-8"
) as file:

    reader = csv.DictReader(file)

    data = list(reader)


# ==========================================
# 3. Informasi dasar dataset
# ==========================================

print("========================================")
print("INFORMASI DATASET")
print("========================================")

print("Jumlah baris :", len(data))
print("Jumlah kolom :", len(reader.fieldnames))

print("\nKolom:")
for column in reader.fieldnames:
    print("-", column)


# ==========================================
# 4. Mengecek data kosong
# ==========================================

print("\n========================================")
print("DATA KOSONG")
print("========================================")

for column in reader.fieldnames:

    empty_count = 0

    for row in data:

        value = row[column]

        if value is None or value.strip() == "":
            empty_count += 1

    print(
        f"{column}: {empty_count} kosong"
    )


# ==========================================
# 5. Mengecek duplikasi URL
# ==========================================

print("\n========================================")
print("DUPLIKASI URL")
print("========================================")

urls = [
    row["url"]
    for row in data
    if row["url"]
]

url_counts = Counter(urls)

duplicate_urls = {
    url: count
    for url, count in url_counts.items()
    if count > 1
}

print(
    "Jumlah URL unik:",
    len(url_counts)
)

print(
    "URL duplikat:",
    len(duplicate_urls)
)


# ==========================================
# 6. Mengecek duplikasi nama produk
# ==========================================

print("\n========================================")
print("DUPLIKASI NAMA PRODUK")
print("========================================")

names = [
    row["name"]
    for row in data
    if row["name"]
]

name_counts = Counter(names)

duplicate_names = {
    name: count
    for name, count in name_counts.items()
    if count > 1
}

print(
    "Jumlah nama unik:",
    len(name_counts)
)

print(
    "Nama yang muncul lebih dari sekali:",
    len(duplicate_names)
)


# ==========================================
# 7. Beberapa contoh nama duplikat
# ==========================================

if duplicate_names:

    print("\nContoh nama duplikat:")

    for name, count in list(
        duplicate_names.items()
    )[:10]:

        print(
            f"- {name} ({count}x)"
        )


# ==========================================
# 8. Distribusi processor
# ==========================================

print("\n========================================")
print("VARIASI PROCESSOR")
print("========================================")

processors = Counter(
    row["processor"]
    for row in data
    if row["processor"]
)

print(
    "Jumlah processor berbeda:",
    len(processors)
)

print("\nContoh:")

for processor, count in processors.most_common(15):

    print(
        f"- {processor} ({count}x)"
    )


# ==========================================
# 9. Distribusi graphics
# ==========================================

print("\n========================================")
print("VARIASI GRAPHICS")
print("========================================")

graphics = Counter(
    row["graphics"]
    for row in data
    if row["graphics"]
)

print(
    "Jumlah graphics berbeda:",
    len(graphics)
)

print("\nContoh:")

for graphic, count in graphics.most_common(15):

    print(
        f"- {graphic} ({count}x)"
    )


# ==========================================
# 10. Distribusi memory
# ==========================================

print("\n========================================")
print("VARIASI MEMORY")
print("========================================")

memory = Counter(
    row["memory"]
    for row in data
    if row["memory"]
)

print(
    "Jumlah format memory berbeda:",
    len(memory)
)

print("\nContoh:")

for value, count in memory.most_common(15):

    print(
        f"- {value} ({count}x)"
    )


# ==========================================
# 11. Distribusi storage
# ==========================================

print("\n========================================")
print("VARIASI STORAGE")
print("========================================")

storage = Counter(
    row["storage"]
    for row in data
    if row["storage"]
)

print(
    "Jumlah format storage berbeda:",
    len(storage)
)

print("\nContoh:")

for value, count in storage.most_common(15):

    print(
        f"- {value} ({count}x)"
    )


# ==========================================
# 12. Contoh beberapa data
# ==========================================

print("\n========================================")
print("5 CONTOH DATA")
print("========================================")

for index, row in enumerate(data[:5], start=1):

    print(f"\nData {index}")

    for column in reader.fieldnames:

        print(
            f"{column}: {row[column]}"
        )


print("\n========================================")
print("INSPEKSI SELESAI")
print("========================================")