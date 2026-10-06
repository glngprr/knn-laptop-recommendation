import requests
import csv
import os
import time

from bs4 import BeautifulSoup
from urllib.parse import urljoin


BASE_URL = "https://www.plazait.co.id"


def get_product_urls():
    """
    Mengambil seluruh URL produk dari 26 halaman katalog laptop.
    """

    product_urls = []

    for page in range(1, 27):

        if page == 1:
            catalog_url = f"{BASE_URL}/laptop"
        else:
            catalog_url = f"{BASE_URL}/laptop?p={page}"

        print(f"\nMengambil halaman katalog {page}/26")
        print(catalog_url)

        response = requests.get(
            catalog_url,
            timeout=15
        )

        print("Status:", response.status_code)

        soup = BeautifulSoup(
            response.text,
            "html.parser"
        )

        links = soup.select("a")

        page_product_count = 0

        for link in links:

            href = link.get("href")

            if href and "/product/" in href:

                # Menghindari link kategori
                if "/product/kategori/" not in href:

                    full_url = urljoin(
                        catalog_url,
                        href
                    )

                    # Menghindari duplikasi
                    if full_url not in product_urls:

                        product_urls.append(full_url)
                        page_product_count += 1

        print(
            "Produk baru:",
            page_product_count
        )

        # Jeda antar halaman katalog
        time.sleep(1)

    return product_urls


def scrape_product(url):
    """
    Mengambil informasi detail dari satu halaman produk.
    """

    response = requests.get(
        url,
        timeout=15
    )

    print(
        "Scraping:",
        url
    )

    print(
        "Status:",
        response.status_code
    )

    soup = BeautifulSoup(
        response.text,
        "html.parser"
    )

    # Nama produk
    product_name = soup.select_one(
        "#pd-title"
    )

    # Harga saat ini
    price = soup.select_one(
        "#pd-price-current"
    )

    # Daftar spesifikasi
    spec_items = soup.select(
        ".pd-short-desc li"
    )

    specs = {}

    for item in spec_items:

        text = item.get_text(
            strip=True
        )

        if " : " in text:

            key, value = text.split(
                " : ",
                1
            )

            specs[key] = value

    laptop = {
        "name": (
            product_name.get_text(strip=True)
            if product_name
            else None
        ),

        "price": (
            price.get_text(strip=True)
            if price
            else None
        ),

        "processor": specs.get(
            "Processor"
        ),

        "memory": specs.get(
            "Memory"
        ),

        "storage": specs.get(
            "Storage"
        ),

        "graphics": specs.get(
            "Graphics"
        ),

        "url": url
    }

    return laptop


# ==========================================
# 1. Mengambil seluruh URL produk
# ==========================================

product_urls = get_product_urls()


print("\n========================================")
print("TOTAL URL PRODUK UNIK:", len(product_urls))
print("========================================")


# ==========================================
# 2. Scraping seluruh produk
# ==========================================

laptops = []

total_products = len(product_urls)

for index, url in enumerate(
    product_urls,
    start=1
):

    print(
        f"\n[{index}/{total_products}]"
    )

    try:

        laptop = scrape_product(url)

        laptops.append(laptop)

    except requests.RequestException as error:

        print(
            "Gagal mengambil:",
            url
        )

        print(
            "Error:",
            error
        )

        # Tetap lanjut ke produk berikutnya
        continue

    # Jeda antar request produk
    time.sleep(1)


# ==========================================
# 3. Membuat folder dataset
# ==========================================

dataset_dir = os.path.join(
    os.path.dirname(
        os.path.dirname(__file__)
    ),
    "dataset"
)

os.makedirs(
    dataset_dir,
    exist_ok=True
)


# ==========================================
# 4. Menentukan lokasi CSV
# ==========================================

csv_path = os.path.join(
    dataset_dir,
    "laptops_raw.csv"
)


# ==========================================
# 5. Menyimpan hasil scraping
# ==========================================

with open(
    csv_path,
    "w",
    newline="",
    encoding="utf-8"
) as file:

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

    writer.writerows(
        laptops
    )


# ==========================================
# 6. Ringkasan
# ==========================================

print("\n========================================")
print("SCRAPING SELESAI")
print("========================================")

print(
    "URL produk ditemukan:",
    len(product_urls)
)

print(
    "Data berhasil diambil:",
    len(laptops)
)

print(
    "File:",
    csv_path
)