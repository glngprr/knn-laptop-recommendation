import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin


BASE_URL = "https://www.plazait.co.id"


def get_product_urls():

    product_urls = []

    for page in range(1, 27):

        if page == 1:
            catalog_url = f"{BASE_URL}/laptop"
        else:
            catalog_url = f"{BASE_URL}/laptop?p={page}"

        print(f"\nMengambil halaman {page}")

        response = requests.get(catalog_url)

        print("Status:", response.status_code)

        soup = BeautifulSoup(response.text, "html.parser")

        links = soup.select("a")

        page_product_count = 0

        for link in links:

            href = link.get("href")

            if href and "/product/" in href:

                if "/product/kategori/" not in href:

                    full_url = urljoin(catalog_url, href)

                    if full_url not in product_urls:

                        product_urls.append(full_url)
                        page_product_count += 1

        print("Produk baru:", page_product_count)

    return product_urls


product_urls = get_product_urls()

print("\n==============================")
print("TOTAL URL PRODUK UNIK:", len(product_urls))
print("==============================")