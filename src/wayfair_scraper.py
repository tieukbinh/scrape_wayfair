import requests
from bs4 import BeautifulSoup
import pandas as pd
import json

import os
from dotenv import load_dotenv



product_url = "https://www.wayfair.com/boards/470a3fc2-8eb5-45cd-8710-805593406b87"
payload = {
    "source": "universal_ecommerce",
    "url": product_url,
    "user_agent_type": "desktop_safari",
    "geo_location": "United States",
    "render": "html",
    "browser_instructions": [
        {
            "type": "wait_for_element",
            "selector": {
                "type": "css",
                "value": "div.SFPrice span.oakhm64z_6112"
            },
            "timeout_s": 10
        }
    ]
}

load_dotenv()
username = os.getenv("USERNAME")
password = os.getenv("PASSWORD")

response = requests.post(
    "https://realtime.oxylabs.io/v1/queries",
    auth=(username, password),
    json=payload,
    timeout=180
)
print(response.status_code)

content = response.json()["results"][0]["content"]
with open("wayfair_page.html", "w", encoding="utf-8") as f:
    f.write(content)

soup = BeautifulSoup(content, "html.parser")
cards = soup.find_all("div", {"data-test-id": "CardWrapper"})

data = []

for card in cards:
    meta_raw = card.get("data-tracking-metadata")

    if not meta_raw:
        continue

    meta = json.loads(meta_raw)["metadata"]

    title = meta.get("listingCardName")
    price = meta.get("firstPriceValue")
    rating = meta.get("averageRating")
    reviews = meta.get("totalReviewCount")
    link_tag = card.find("a", href=True)
    link = link_tag["href"] if link_tag else None

    data.append({
        "Product Title": title,
        "Price": price,
        "Rating": rating,
        "Reviews": reviews,
        "Link": link
    })

df = pd.DataFrame(data)
df.to_csv("product_data.csv", index=False)
df.to_json("product_data.json", orient="records")
