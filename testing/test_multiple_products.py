import requests
from bs4 import BeautifulSoup


def scrape_product(url):
    response = requests.get(url)

    print("Status:", response.status_code)

    soup = BeautifulSoup(response.text, "html.parser")

    product_name = soup.select_one("#pd-title")
    price = soup.select_one("#pd-price-current")
    spec_items = soup.select(".pd-short-desc li")

    specs = {}

    for item in spec_items:
        text = item.get_text(strip=True)

        if " : " in text:
            key, value = text.split(" : ", 1)
            specs[key] = value

    laptop = {
        "name": product_name.get_text(strip=True) if product_name else None,
        "price": price.get_text(strip=True) if price else None,
        "processor": specs.get("Processor"),
        "memory": specs.get("Memory"),
        "storage": specs.get("Storage"),
        "graphics": specs.get("Graphics"),
    }

    return laptop


urls = [
    "https://www.plazait.co.id/product/lenovo-ideapad-slim-3-14amn8-82xn00c5id-ryzen-3-7320u-amd-radeon-graphics-arctic-grey",

    "https://www.plazait.co.id/product/hp-14-em0321au-bd0y0pa-gold-2y",

    "https://www.plazait.co.id/product/hp-14-ep0261tu-bd0y5pa-core-i3-1315u-intel-uhd-graphics-silver",
]


laptops = []

for url in urls:
    print("\nScraping:", url)

    laptop = scrape_product(url)
    laptops.append(laptop)


print("\n=== HASIL ===")

for laptop in laptops:
    print(laptop)