````markdown
# Penerapan K-Nearest Neighbors (KNN) pada Content-Based Filtering untuk Sistem Rekomendasi Laptop Berbasis Web

Project ini merupakan tahap awal pengembangan sistem rekomendasi laptop berbasis web menggunakan pendekatan **Content-Based Filtering** dengan algoritma **K-Nearest Neighbors (KNN)**.

Pada tahap ini, fokus utama adalah mengumpulkan, membersihkan, menormalisasi, dan memperkaya dataset laptop dengan data benchmark CPU dan GPU. Implementasi KNN dan sistem rekomendasi belum dilakukan dan menjadi tahap lanjutan.

---

## 1. Project Overview

Tujuan project adalah membangun sistem yang dapat memberikan rekomendasi laptop berdasarkan kemiripan karakteristik hardware.

Pendekatan yang digunakan:

- **Content-Based Filtering** sebagai pendekatan sistem rekomendasi.
- **K-Nearest Neighbors (KNN)** sebagai algoritma untuk mencari laptop dengan karakteristik yang paling mirip.
- **PassMark benchmark** digunakan untuk merepresentasikan performa CPU dan GPU dalam bentuk nilai numerik.

Secara umum, pipeline project dirancang sebagai berikut:

```text
Web Scraping
     ↓
Raw Laptop Dataset
     ↓
Data Recovery & Cleaning
     ↓
Feature Extraction
     ↓
Hardware Name Normalization
     ↓
Benchmark Enrichment
     ↓
Final Feature Engineering
     ↓
Feature Scaling
     ↓
KNN Similarity
     ↓
Top-N Recommendation
     ↓
Comparison / Pros & Cons
     ↓
Web Interface
```
````

Status saat ini berada sampai tahap **Benchmark Enrichment**.

---

## 2. Current Status

### Sudah selesai

- Web scraping data laptop dari Plaza IT.
- Pengumpulan 648 unique laptop.
- Recovery beberapa missing specification dari nama produk.
- Parsing khusus untuk produk Apple.
- Cleaning dataset.
- Ekstraksi numerical features dasar.
- Normalisasi nama CPU dan GPU.
- Pengumpulan dan mapping benchmark CPU/GPU.
- Pembuatan dataset benchmark-enriched.
- Inspection dan validasi pada setiap tahap preprocessing.

### Belum dikerjakan

- Final feature selection.
- Analisis distribusi feature.
- Feature scaling.
- Implementasi KNN.
- Penentuan nilai `K`.
- Perhitungan similarity/distance.
- Top-N recommendation.
- Evaluasi sistem rekomendasi.
- Comparison engine.
- Pros/cons generation.
- Web application.

---

## 3. Data Source

### 3.1 Laptop Data

Sumber utama dataset laptop:

**Plaza IT**

```text
https://www.plazait.co.id/
```

Catalog yang digunakan:

```text
https://www.plazait.co.id/laptop
```

Scraping dilakukan pada halaman katalog 1–26.

Hasil scraping:

- 648 unique product URLs
- 648 laptop records

Data utama yang dikumpulkan:

```text
name
price
processor
memory
storage
graphics
url
```

### 3.2 Benchmark Data

Benchmark hardware menggunakan **PassMark** sebagai sumber benchmark utama.

CPU menggunakan:

```text
CPU Mark / Multithread Rating
```

GPU menggunakan:

```text
G3D Mark
```

Benchmark digunakan sebagai numerical representation untuk performa hardware.

Benchmark yang digunakan merupakan snapshot pada:

```text
2026-10-05
```

Nilai benchmark dapat berubah dari waktu ke waktu karena data PassMark berasal dari hasil benchmark yang dikumpulkan secara dinamis. Oleh karena itu, tanggal benchmark dicatat dalam dataset.

---

## 4. Dataset Pipeline

Dataset mengalami beberapa tahap transformasi.

```text
laptops_raw.csv
       ↓
laptops_recovered.csv
       ↓
laptops_cleaned.csv
       ↓
laptops_features.csv
       ↓
laptops_normalized.csv
       ↓
laptops_benchmark_enriched.csv
```

### `laptops_raw.csv`

Dataset hasil scraping awal dari Plaza IT.

Berisi 648 laptop dengan data:

```text
name
price
processor
memory
storage
graphics
url
```

Dataset ini digunakan sebagai raw data dan tidak digunakan langsung sebagai input KNN.

---

### `laptops_recovered.csv`

Pada tahap ini dilakukan recovery terhadap specification yang kosong apabila informasinya masih dapat diperoleh dari nama produk.

Recovery dilakukan secara konservatif.

Informasi tidak diisi apabila tidak terdapat bukti yang cukup dari data yang tersedia.

---

### `laptops_cleaned.csv`

Dataset yang telah melalui proses cleaning dan recovery.

Beberapa informasi Apple diproses menggunakan parser khusus karena format nama produknya berbeda dengan sebagian besar laptop Windows.

Kolom utama:

```text
name
price
processor
memory
storage
graphics
cpu_cores
gpu_cores
url
```

---

### `laptops_features.csv`

Dataset dengan numerical features dasar yang diekstrak dari data laptop.

Feature utama:

```text
price_numeric
ram_gb
storage_gb
cpu_cores
gpu_cores
```

Contoh konversi:

```text
Rp 15.999.000 → 15999000
16GB → 16
1TB → 1024GB
```

Raw specification tetap dipertahankan agar informasi detail hardware tidak hilang.

---

### `laptops_normalized.csv`

Dataset setelah nama CPU dan GPU dinormalisasi.

Tujuan normalization adalah mengurangi perbedaan penulisan yang hanya bersifat format.

Contoh:

```text
Intel Core 5 120U
Intel Core 5-120U
Intel Core 5 Processor 120U
```

dapat dinormalisasi menjadi format yang konsisten.

Contoh GPU:

```text
RTX5060 8GB
RTX 5060 8GB
```

dinormalisasi menjadi:

```text
RTX 5060 8GB
```

Normalization dilakukan secara konservatif.

Hardware yang memiliki perbedaan model nyata tidak digabung hanya karena nama string-nya mirip.

Contoh:

```text
Intel Core Ultra 7-255H
Intel Core Ultra 7-255HX

Intel Core i7-13700H
Intel Core i7-13700HX

AMD Ryzen 5-7430
AMD Ryzen 5-7430U
```

Tidak boleh dianggap sebagai hardware yang sama hanya berdasarkan string similarity.

---

### `laptops_benchmark_enriched.csv`

Dataset terakhir yang telah diperkaya dengan benchmark CPU dan GPU.

Kolom benchmark utama:

```text
cpu_passmark_name
cpu_passmark_mark
cpu_mapping_status

gpu_passmark_name
gpu_passmark_g3d_mark
gpu_mapping_status

benchmark_date
```

Dataset ini merupakan titik awal untuk tahap final feature engineering dan implementasi KNN.

---

## 5. Data Recovery & Cleaning

Dataset hasil scraping tidak sepenuhnya lengkap.

Pada raw dataset terdapat beberapa specification yang kosong:

```text
Processor : 52
Memory    : 47
Storage   : 47
Graphics  : 67
```

Beberapa missing value dapat dipulihkan dari nama produk.

Namun, recovery tidak dilakukan secara agresif.

Jika informasi tidak dapat dipastikan dari data yang tersedia, value tetap dibiarkan kosong.

### Apple

Produk Apple memiliki format specification yang berbeda sehingga membutuhkan parsing khusus.

Parser Apple menangani beberapa jenis processor seperti:

```text
M1
M2
M3
M4
M5
M-series Pro
M-series Max
A18 Pro
```

Jika tersedia, informasi seperti CPU cores, GPU cores, RAM, dan storage juga diekstrak.

Apple GPU core count tidak dimasukkan sebagai nama GPU karena informasi tersebut secara semantik berbeda dari nama GPU discrete/integrated yang digunakan pada laptop non-Apple.

---

## 6. Hardware Name Normalization

Normalization dilakukan sebelum benchmark mapping.

Pipeline yang digunakan:

```text
Raw Hardware Name
        ↓
Normalized Hardware Name
        ↓
Benchmark Mapping
        ↓
Benchmark Score
```

Normalization hanya bertujuan menyeragamkan format nama.

Contoh:

```text
Intel Core Ultra 9 Processor 185H
```

menjadi:

```text
Intel Core Ultra 9-185H
```

Contoh lainnya:

```text
RTX5070Ti 12GB
```

menjadi:

```text
RTX 5070 Ti 12GB
```

### Important Note

`SequenceMatcher` pada tahap exploration hanya digunakan untuk menemukan kandidat hardware dengan nama yang mirip.

Itu **bukan** dasar untuk otomatis menyatakan dua hardware identik.

Hal ini penting karena beberapa hardware memiliki nama yang sangat mirip tetapi performanya berbeda.

Contoh:

```text
Intel Core Ultra 7-255H
Intel Core Ultra 7-255HX
```

atau:

```text
Intel Core i7-13700H
Intel Core i7-13700HX
```

Mapping benchmark harus dilakukan berdasarkan identitas hardware yang benar.

---

## 7. Benchmark Enrichment

Benchmark mapping dilakukan dengan memisahkan:

1. Nama hardware dari dataset.
2. Nama hardware pada benchmark source.
3. Nilai benchmark.

Contoh struktur:

```text
Normalized Hardware
        ↓
Canonical / PassMark Name
        ↓
PassMark Score
```

### CPU

Feature benchmark:

```text
cpu_passmark_name
cpu_passmark_mark
cpu_mapping_status
```

CPU benchmark menggunakan CPU Mark / Multithread Rating.

### GPU

Feature benchmark:

```text
gpu_passmark_name
gpu_passmark_g3d_mark
gpu_mapping_status
```

GPU benchmark menggunakan G3D Mark.

### Mapping Status

Status mapping yang digunakan:

```text
MATCHED
AMBIGUOUS
NOT_FOUND
```

`MATCHED` berarti hardware berhasil dipetakan dengan cukup yakin.

`AMBIGUOUS` berarti terdapat lebih dari satu kemungkinan atau nama hardware terlalu generik untuk diberikan benchmark tertentu secara aman.

`NOT_FOUND` berarti hardware tidak ditemukan pada benchmark source.

---

## 8. Current Dataset Statistics

Dataset saat ini terdiri dari:

| Item                                   | Jumlah |
| -------------------------------------- | -----: |
| Total laptop                           |    648 |
| Unique processor setelah normalization |    138 |
| Unique graphics setelah normalization  |     75 |
| CPU benchmark tersedia                 |    636 |
| CPU benchmark missing                  |     12 |
| GPU benchmark tersedia                 |    455 |
| GPU benchmark missing                  |    193 |

Coverage CPU:

```text
636 / 648 = 98.15%
```

Coverage GPU:

```text
455 / 648 = 70.22%
```

---

## 9. Current Benchmark Coverage

Dari 648 laptop:

```text
455  CPU MATCHED + GPU MATCHED
146  CPU MATCHED + GPU AMBIGUOUS
35   CPU MATCHED + NO GPU DATA
7    CPU UNMAPPED + NO GPU DATA
5    CPU AMBIGUOUS + NO GPU DATA
--------------------------------
648  Total
```

Dengan demikian, terdapat 193 laptop yang belum memiliki GPU benchmark yang dapat digunakan secara aman.

### GPU Ambiguous

Sebagian besar missing GPU benchmark berasal dari hardware GPU yang ditulis terlalu generik, misalnya:

```text
AMD Radeon Graphics
Intel Arc Graphics
Qualcomm Adreno
```

Nama generik tersebut tidak cukup untuk langsung diberikan satu nilai G3D Mark tertentu.

Jangan memberikan benchmark berdasarkan perkiraan hanya untuk menghilangkan missing value.

---

## 10. Candidate KNN Features

Feature numerik yang saat ini menjadi kandidat utama untuk KNN:

```text
price_numeric
ram_gb
storage_gb
cpu_passmark_mark
gpu_passmark_g3d_mark
```

Alasannya:

- `price_numeric` merepresentasikan harga laptop.
- `ram_gb` merepresentasikan kapasitas RAM.
- `storage_gb` merepresentasikan kapasitas storage.
- `cpu_passmark_mark` merepresentasikan performa CPU.
- `gpu_passmark_g3d_mark` merepresentasikan performa GPU.

Raw text seperti:

```text
processor
graphics
memory
storage
```

tidak digunakan secara langsung sebagai numerical input KNN.

---

## 11. CPU/GPU Cores

Dataset juga memiliki:

```text
cpu_cores
gpu_cores
```

Namun feature tersebut belum digunakan sebagai primary KNN feature.

Coverage saat ini:

```text
cpu_cores : 45 / 648
gpu_cores : 44 / 648
```

Karena sebagian besar value missing, melakukan imputasi secara sembarangan dapat menghasilkan representasi hardware yang tidak valid.

Untuk sementara feature tersebut dipertahankan sebagai informasi tambahan, bukan feature utama KNN.

---

## 12. Important Methodological Decisions

Beberapa keputusan metodologis yang sudah dibuat:

### 1. KNN digunakan untuk similarity/recommendation

KNN pada project ini bukan digunakan sebagai supervised classification.

Tujuannya adalah mencari laptop yang memiliki karakteristik paling dekat dengan laptop/query tertentu.

### 2. Content-Based Filtering adalah pendekatannya

Content-Based Filtering menentukan bahwa rekomendasi didasarkan pada karakteristik item.

Dalam project ini karakteristik tersebut berasal dari:

```text
Price
RAM
Storage
CPU Performance
GPU Performance
```

### 3. Benchmark digunakan sebagai numerical representation

Daripada hanya menggunakan nama processor/GPU sebagai categorical text, benchmark digunakan untuk merepresentasikan performa hardware secara numerik.

### 4. Tidak melakukan arbitrary benchmark imputation

Missing benchmark tidak boleh langsung diisi menggunakan median atau nilai lain tanpa pertimbangan metodologis.

Contohnya, memberikan median GPU score kepada laptop dengan GPU yang sebenarnya tidak diketahui dapat membuat laptop tersebut terlihat memiliki performa yang tidak sesuai.

### 5. String similarity bukan final mapping

Kemiripan nama hardware hanya digunakan untuk mencari kandidat.

Final mapping harus mempertimbangkan identitas model hardware.

### 6. Catalog dan recommendation pool dapat dibedakan

Seluruh 648 laptop tetap dapat dipertahankan dalam catalog.

Namun, recommendation pool dapat menggunakan subset laptop yang memiliki feature yang cukup lengkap apabila strategi missing value belum ditentukan.

---

## 13. Current Problems / Open Questions

Tahap preprocessing dan benchmark enrichment belum sepenuhnya final.

Beberapa hal masih perlu diputuskan.

### A. GPU Benchmark Coverage

Masih terdapat 193 laptop tanpa GPU benchmark.

Prioritas investigasi:

```text
146 ambiguous GPU
        ↓
Investigasi apakah model GPU sebenarnya dapat diketahui
        ↓
35 no GPU data
        ↓
Evaluasi apakah informasi tambahan dapat diperoleh
        ↓
12 CPU benchmark unresolved
```

Jangan mengisi benchmark secara manual tanpa sumber yang dapat dipertanggungjawabkan.

---

### B. Final Feature Selection

Feature kandidat saat ini:

```text
price_numeric
ram_gb
storage_gb
cpu_passmark_mark
gpu_passmark_g3d_mark
```

Belum diputuskan secara final apakah seluruh feature akan digunakan.

Feature selection sebaiknya dilakukan setelah melihat:

- distribusi data;
- outlier;
- korelasi;
- tujuan rekomendasi;
- pengaruh masing-masing feature terhadap distance.

---

### C. Feature Scaling

KNN merupakan distance-based algorithm.

Karena feature memiliki skala yang berbeda:

```text
price          → jutaan rupiah
RAM            → GB
storage        → GB
CPU benchmark  → ribuan
GPU benchmark  → ribuan
```

Feature scaling diperlukan sebelum menghitung distance.

`StandardScaler` dapat menjadi salah satu kandidat, tetapi metode scaling belum ditetapkan secara final.

Distribusi dan outlier sebaiknya dianalisis terlebih dahulu.

---

### D. Missing Benchmark Strategy

Belum ditentukan apakah recommendation engine akan:

1. Menggunakan hanya laptop dengan benchmark lengkap.
2. Menggunakan feature subset tertentu.
3. Membuat pendekatan lain untuk menangani missing benchmark.

Keputusan ini perlu mempertimbangkan trade-off antara:

```text
data coverage
vs
data reliability
```

---

## 14. Planned Next Steps

Tahapan yang direkomendasikan setelah repository ini diteruskan:

```text
1. Review / finalize benchmark mapping
        ↓
2. Investigate ambiguous GPU
        ↓
3. Finalize numerical features
        ↓
4. Analyze feature distributions
        ↓
5. Check outliers
        ↓
6. Apply feature scaling
        ↓
7. Implement KNN
        ↓
8. Determine K
        ↓
9. Generate Top-N recommendations
        ↓
10. Evaluate recommendation results
        ↓
11. Build comparison / pros-cons layer
        ↓
12. Integrate with web application
```

---

## 15. Project Folder Structure

```text
project/
├── benchmark/
│   ├── cpu_benchmark.csv
│   └── gpu_benchmark.csv
│
├── dataset/
│   ├── laptops_raw.csv
│   ├── laptops_recovered.csv
│   ├── laptops_cleaned.csv
│   ├── laptops_features.csv
│   ├── laptops_normalized.csv
│   └── laptops_benchmark_enriched.csv
│
├── exploration/
│   └── find_similar_hardware_names.py
│
├── inspection/
│   ├── inspect_cleaned.py
│   ├── inspect_dataset.py
│   ├── inspect_features.py
│   ├── inspect_missing_from_name.py
│   ├── inspect_normalized.py
│   ├── inspect_recovered.py
│   ├── inventory_hardware.py
│   └── inventory_normalized_hardware.py
│
├── preprocessing/
│   ├── create_basic_features.py
│   ├── normalize_hardware_names.py
│   ├── recover_apple_to_csv.py
│   ├── recover_specs_from_name.py
│   └── recover_specs_to_csv.py
│
├── scrape/
│   ├── get_product_urls.py
│   └── scrape_laptops.py
│
└── testing/
    ├── test_all_pages.py
    ├── test_multiple_products.py
    ├── test_pagination.py
    ├── test_recover_apple.py
    └── test_scraper.py
```

---

## 16. Script Documentation

### `scrape/`

| Script                | Fungsi                                               |
| --------------------- | ---------------------------------------------------- |
| `scrape_laptops.py`   | Melakukan scraping data laptop dari katalog Plaza IT |
| `get_product_urls.py` | Mengambil URL produk dari halaman katalog            |

### `preprocessing/`

| Script                        | Fungsi                                             |
| ----------------------------- | -------------------------------------------------- |
| `recover_specs_from_name.py`  | Mencari kemungkinan specification dari nama produk |
| `recover_specs_to_csv.py`     | Menyimpan hasil recovery specification             |
| `recover_apple_to_csv.py`     | Melakukan parsing khusus produk Apple              |
| `create_basic_features.py`    | Membuat numerical features dasar                   |
| `normalize_hardware_names.py` | Melakukan normalization nama CPU dan GPU           |

### `inspection/`

| Script                             | Fungsi                                  |
| ---------------------------------- | --------------------------------------- |
| `inspect_dataset.py`               | Inspection dataset awal                 |
| `inspect_missing_from_name.py`     | Memeriksa missing specification         |
| `inspect_recovered.py`             | Memeriksa hasil recovery                |
| `inspect_cleaned.py`               | Memeriksa dataset cleaned               |
| `inspect_features.py`              | Memeriksa numerical features            |
| `inspect_normalized.py`            | Memeriksa hasil normalization           |
| `inventory_hardware.py`            | Melihat inventory CPU/GPU               |
| `inventory_normalized_hardware.py` | Melihat inventory setelah normalization |

### `exploration/`

| Script                           | Fungsi                                                                      |
| -------------------------------- | --------------------------------------------------------------------------- |
| `find_similar_hardware_names.py` | Mencari kandidat hardware dengan nama yang mirip untuk membantu investigasi |

Script ini bersifat exploratory dan bukan bagian dari final benchmark mapping.

### `testing/`

| Script                      | Fungsi                           |
| --------------------------- | -------------------------------- |
| `test_scraper.py`           | Testing fungsi scraper           |
| `test_multiple_products.py` | Testing scraping beberapa produk |
| `test_pagination.py`        | Testing pagination               |
| `test_all_pages.py`         | Testing seluruh halaman katalog  |
| `test_recover_apple.py`     | Testing parser Apple             |

---

## 17. Reproducing the Preprocessing Pipeline

Urutan umum preprocessing:

```text
1. Scraping
2. Recovery specification
3. Apple parsing
4. Feature extraction
5. Hardware normalization
6. Benchmark enrichment
```

Contoh menjalankan preprocessing:

```bash
python preprocessing/recover_specs_from_name.py
python preprocessing/recover_specs_to_csv.py
python preprocessing/recover_apple_to_csv.py
python preprocessing/create_basic_features.py
python preprocessing/normalize_hardware_names.py
```

Catatan:

Dataset benchmark-enriched saat ini sudah tersedia di:

```text
dataset/laptops_benchmark_enriched.csv
```

Sehingga tahap berikutnya tidak perlu mengulang seluruh proses preprocessing apabila tidak ada perubahan pada data sebelumnya.

---

## 18. Important Files for the Next Stage

Jika ingin langsung melanjutkan ke tahap KNN, file utama yang perlu diperhatikan adalah:

```text
dataset/laptops_benchmark_enriched.csv
```

File benchmark:

```text
benchmark/cpu_benchmark.csv
benchmark/gpu_benchmark.csv
```

Untuk memahami preprocessing:

```text
preprocessing/
```

Untuk memahami hasil dan coverage:

```text
inspection/
```

---

## 19. Notes for Further Development

Beberapa hal sebaiknya tidak diubah tanpa alasan metodologis:

- Jangan menggabungkan processor hanya berdasarkan kemiripan string.
- Jangan menggabungkan GPU berbeda hanya karena berada pada product family yang sama.
- Jangan mengisi benchmark missing menggunakan nilai arbitrer.
- Jangan menggunakan `cpu_cores` dan `gpu_cores` sebagai feature utama tanpa menangani missing value secara metodologis.
- Jangan langsung melakukan KNN sebelum feature scaling.
- Jangan menganggap KNN sebagai classifier pada project ini.
- Jangan menghapus 193 laptop dari dataset catalog hanya karena benchmark GPU belum tersedia.

Dataset lengkap tetap berguna sebagai catalog, sedangkan recommendation pool dapat ditentukan setelah strategi missing feature diputuskan.

---

## 20. Project Status

**Current stage:**

```text
[✓] Web Scraping
[✓] Data Recovery
[✓] Data Cleaning
[✓] Basic Feature Extraction
[✓] Hardware Normalization
[✓] Benchmark Enrichment
[ ] Final Feature Engineering
[ ] Feature Scaling
[ ] KNN
[ ] Top-N Recommendation
[ ] Evaluation
[ ] Comparison Engine
[ ] Web Application
```

Repository ini saat ini berfungsi sebagai **data preparation dan research stage** untuk sistem rekomendasi laptop.

Tahap selanjutnya adalah menentukan feature final, menyelesaikan strategi missing benchmark, kemudian membangun model KNN dan recommendation pipeline.
