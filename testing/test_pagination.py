import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

BASE_URL = "https://www.plazait.co.id"
CATALOG_URL = f"{BASE_URL}/laptop?p=2"

response = requests.get(CATALOG_URL)

print("Status:", response.status_code)

soup = BeautifulSoup(response.text, "html.parser")

links = soup.select("a")

product_urls = []

for link in links:
    href = link.get("href")

    if href and "/product/" in href:
        if "/product/kategori/" not in href:

            full_url = urljoin(CATALOG_URL, href)

            if full_url not in product_urls:
                product_urls.append(full_url)


print("\nJumlah produk halaman 2:", len(product_urls))

print("\n=== URL PRODUK ===")

for url in product_urls:
    print(url)