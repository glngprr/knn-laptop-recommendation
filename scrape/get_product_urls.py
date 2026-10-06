import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

url = "https://www.plazait.co.id/laptop"

response = requests.get(url)

print("Status:", response.status_code)

soup = BeautifulSoup(response.text, "html.parser")

links = soup.select("a")

product_urls = []

for link in links:
    href = link.get("href")

    if href and "/product/" in href:
        if "/product/kategori/" not in href:
            full_url = urljoin(url, href)

            if full_url not in product_urls:
                product_urls.append(full_url)

print("\nJumlah URL:", len(product_urls))

for product_url in product_urls[:10]:
    print(product_url)