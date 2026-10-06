import csv
import os
import re
from collections import defaultdict
from difflib import SequenceMatcher


dataset_path = os.path.join(
    os.path.dirname(os.path.dirname(__file__)),
    "dataset",
    "laptops_features.csv"
)


with open(dataset_path, "r", encoding="utf-8") as file:
    reader = csv.DictReader(file)
    data = list(reader)


def normalize_for_comparison(text):
    """
    Normalisasi ringan HANYA untuk mencari kandidat kemiripan.

    Tidak digunakan untuk mengubah dataset.
    """

    text = text.lower()

    # Hilangkan trademark / simbol
    text = text.replace("™", "")
    text = text.replace("®", "")

    # Samakan tanda hubung dan spasi
    text = text.replace("-", " ")
    text = text.replace(",", " ")

    # Hilangkan kata yang biasanya hanya menjelaskan format
    text = re.sub(r"\bprocessor\b", "", text)

    # Rapikan whitespace
    text = re.sub(r"\s+", " ", text)

    return text.strip()


def find_candidates(values, threshold=0.90):
    """
    Mencari pasangan nama yang sangat mirip.
    """

    values = sorted(values)

    candidates = []

    for i in range(len(values)):
        for j in range(i + 1, len(values)):

            a = values[i]
            b = values[j]

            a_normalized = normalize_for_comparison(a)
            b_normalized = normalize_for_comparison(b)

            similarity = SequenceMatcher(
                None,
                a_normalized,
                b_normalized
            ).ratio()

            if similarity >= threshold and a_normalized != b_normalized:
                candidates.append(
                    (similarity, a, b)
                )

    return sorted(
        candidates,
        key=lambda item: item[0],
        reverse=True
    )


# ========================================
# PROCESSOR
# ========================================

processors = {
    row["processor"].strip()
    for row in data
    if row["processor"] and row["processor"].strip()
}


processor_candidates = find_candidates(processors)


print("========================================")
print("KANDIDAT KEMIRIPAN PROCESSOR")
print("========================================")

print(
    "Jumlah processor unik:",
    len(processors)
)

print(
    "Jumlah pasangan kandidat:",
    len(processor_candidates)
)


for similarity, a, b in processor_candidates:

    print(
        f"{similarity:.3f} | {a}  <->  {b}"
    )


# ========================================
# GRAPHICS
# ========================================

graphics = {
    row["graphics"].strip()
    for row in data
    if row["graphics"] and row["graphics"].strip()
}


graphics_candidates = find_candidates(
    graphics,
    threshold=0.90
)


print("\n========================================")
print("KANDIDAT KEMIRIPAN GRAPHICS")
print("========================================")

print(
    "Jumlah graphics unik:",
    len(graphics)
)

print(
    "Jumlah pasangan kandidat:",
    len(graphics_candidates)
)


for similarity, a, b in graphics_candidates:

    print(
        f"{similarity:.3f} | {a}  <->  {b}"
    )


print("\n========================================")
print("ANALISIS SELESAI")
print("========================================")
print("Dataset TIDAK diubah.")
print("========================================")