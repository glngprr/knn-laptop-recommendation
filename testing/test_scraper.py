import requests
from bs4 import BeautifulSoup


def scrape_product(url):
    response = requests.get(url)

    print("Status:", response.status_code)

    soup = BeautifulSoup(response.text, "html.parser")

    # Nama produk
    product_name = soup.select_one("#pd-title")

    # Harga
    price = soup.select_one("#pd-price-current")

    # Spesifikasi
    spec_items = soup.select(".pd-short-desc li")

    specs = {}

    for item in spec_items:
        text = item.get_text(strip=True)

        if " : " in text:
            key, value = text.split(" : ", 1)
            specs[key] = value

    # Gabungkan menjadi satu data laptop
    laptop = {
        "name": product_name.get_text(strip=True) if product_name else None,
        "price": price.get_text(strip=True) if price else None,
        "processor": specs.get("Processor"),
        "memory": specs.get("Memory"),
        "storage": specs.get("Storage"),
        "graphics": specs.get("Graphics"),
    }

    return laptop


url = "https://plazait.co.id/product/hp-14-ep0261tu-bd0y5pa-core-i3-1315u-intel-uhd-graphics-silver"

laptop = scrape_product(url)

print("\nHasil:")
print(laptop)