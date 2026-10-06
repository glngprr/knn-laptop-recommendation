import csv
import os
import re


INPUT_FILE = os.path.join(
    os.path.dirname(os.path.dirname(__file__)),
    "dataset",
    "laptops_features.csv"
)

OUTPUT_FILE = os.path.join(
    os.path.dirname(os.path.dirname(__file__)),
    "dataset",
    "laptops_normalized.csv"
)


def normalize_hardware_name(value):
    """
    Normalisasi umum nama hardware.

    Hanya membersihkan perbedaan format/penulisan.
    Tidak mengubah model hardware.
    """

    if not value:
        return ""

    text = value.strip()

    # Hapus simbol trademark
    text = text.replace("™", "")
    text = text.replace("®", "")

    # Normalisasi whitespace
    text = re.sub(r"\s+", " ", text).strip()

    # Rapikan spasi di sekitar tanda hubung
    text = re.sub(r"\s*-\s*", "-", text)

    # RTX5060 -> RTX 5060
    text = re.sub(
        r"\bRTX(?=\d)",
        "RTX ",
        text,
        flags=re.IGNORECASE
    )

    # RTX5070Ti -> RTX 5070 Ti
    text = re.sub(
        r"\b(RTX\s+\d+)\s*Ti\b",
        r"\1 Ti",
        text,
        flags=re.IGNORECASE
    )

    # Rapikan whitespace setelah proses sebelumnya
    text = re.sub(r"\s+", " ", text).strip()

    return text


def normalize_cpu_name(value):
    """
    Normalisasi nama CPU secara konservatif.

    Hanya menyamakan variasi penulisan yang jelas.
    Nomor/model CPU tidak diubah.
    """

    text = normalize_hardware_name(value)

    if not text:
        return ""

    # ---------------------------------------------------------
    # Intel Core i3/i5/i7/i9
    #
    # Contoh:
    # Intel Core i7 Processor 14650HX
    # -> Intel Core i7-14650HX
    #
    # Intel Core i7 14650HX
    # -> Intel Core i7-14650HX
    # ---------------------------------------------------------

    text = re.sub(
        r"\b(Intel Core i[3579]) Processor\s+(\d{3,5}[A-Z]{0,3})\b",
        r"\1-\2",
        text,
        flags=re.IGNORECASE
    )

    text = re.sub(
        r"\b(Intel Core i[3579])\s+(\d{3,5}[A-Z]{0,3})\b",
        r"\1-\2",
        text,
        flags=re.IGNORECASE
    )

    # ---------------------------------------------------------
    # Intel Core 3/5/7/9
    #
    # Contoh:
    # Intel Core 5 Processor 120U
    # -> Intel Core 5-120U
    #
    # Intel Core 5 120U
    # -> Intel Core 5-120U
    # ---------------------------------------------------------

    text = re.sub(
        r"\b(Intel Core [3579]) Processor\s+(\d{3,5}[A-Z]{0,3})\b",
        r"\1-\2",
        text,
        flags=re.IGNORECASE
    )

    text = re.sub(
        r"\b(Intel Core [3579])\s+(\d{3,5}[A-Z]{0,3})\b",
        r"\1-\2",
        text,
        flags=re.IGNORECASE
    )

    # ---------------------------------------------------------
    # Intel Core Ultra 5/7/9
    #
    # Contoh:
    # Intel Core Ultra 9 Processor 185H
    # -> Intel Core Ultra 9-185H
    #
    # Intel Core Ultra 7 355
    # -> Intel Core Ultra 7-355
    # ---------------------------------------------------------

    text = re.sub(
        r"\b(Intel Core Ultra [579]) Processor\s+(\d{3,5}[A-Z]{0,3})\b",
        r"\1-\2",
        text,
        flags=re.IGNORECASE
    )

    text = re.sub(
        r"\b(Intel Core Ultra [579])\s+(\d{3,5}[A-Z]{0,3})\b",
        r"\1-\2",
        text,
        flags=re.IGNORECASE
    )

    # ---------------------------------------------------------
    # AMD Ryzen 3/5/7/9
    #
    # Contoh:
    # AMD Ryzen 7 250
    # -> AMD Ryzen 7-250
    #
    # AMD Ryzen 5 40 Processor
    # -> AMD Ryzen 5-40 Processor
    #
    # Processor di akhir sengaja tidak dihapus.
    # ---------------------------------------------------------

    text = re.sub(
        r"\b(AMD Ryzen [3579])\s+(\d{2,5}[A-Z]{0,3})\b",
        r"\1-\2",
        text,
        flags=re.IGNORECASE
    )

    # ---------------------------------------------------------
    # AMD Ryzen AI 5/7/9
    #
    # Contoh:
    # AMD Ryzen AI 7 350
    # -> AMD Ryzen AI 7-350
    #
    # AMD Ryzen AI 9 465 Processor
    # -> AMD Ryzen AI 9-465 Processor
    # ---------------------------------------------------------

    text = re.sub(
        r"\b(AMD Ryzen AI [579])\s+(\d{2,5}[A-Z]{0,3})\b",
        r"\1-\2",
        text,
        flags=re.IGNORECASE
    )

    # Rapikan whitespace terakhir
    text = re.sub(r"\s+", " ", text).strip()

    return text


def normalize_gpu_name(value):
    """
    Normalisasi nama GPU.
    Hanya menangani variasi format penulisan.
    """

    text = normalize_hardware_name(value)

    if not text:
        return ""

    return text


# =========================================================
# Baca dataset
# =========================================================

with open(INPUT_FILE, "r", encoding="utf-8", newline="") as file:
    reader = csv.DictReader(file)
    data = list(reader)


# =========================================================
# Normalisasi
# =========================================================

for row in data:

    row["processor_normalized"] = normalize_cpu_name(
        row.get("processor", "")
    )

    row["graphics_normalized"] = normalize_gpu_name(
        row.get("graphics", "")
    )


# =========================================================
# Simpan hasil
# =========================================================

fieldnames = list(data[0].keys())

with open(OUTPUT_FILE, "w", encoding="utf-8", newline="") as file:
    writer = csv.DictWriter(
        file,
        fieldnames=fieldnames
    )

    writer.writeheader()
    writer.writerows(data)


print("Normalisasi hardware selesai.")
print("Total data:", len(data))
print("Output:", OUTPUT_FILE)