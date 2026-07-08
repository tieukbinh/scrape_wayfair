import datetime
import requests
import json
import logging
from typing import Any
from dotenv import load_dotenv
import os

load_dotenv()

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

def load_product_links(filename: str) -> list[dict]:
    logging.info(f"Loading product links from {filename}")

    try:
        with open(filename, "r", encoding="utf-8") as f:
            inputs = [
                {"url": line.strip()}
                for line in f
                if line.strip()
            ]
            if not inputs:
                logging.warning(f"No valid product links found in {filename}")
            else:
                logging.info(f"Loaded {len(inputs)} product link(s)...")
            return inputs
        
    except FileNotFoundError:
        logging.error(f"File not found: {filename}")
        return []
    
    except Exception as e:
        logging.error(f"Error loading product links: {str(e)}")
        return []

class WayfairCollector:
    SCRAPE_URL = "https://api.brightdata.com/datasets/v3/scrape"
    DATASET_ID = "gd_ltr9ne3p24zrhrbu28"

    def __init__(self, api_token: str):
        self.api_token = api_token
        self.headers = {
            "Authorization": f"Bearer {api_token}",
            "Content-Type": "application/json",
        }

    def collect_data(
        self, inputs: list[dict]
    ) -> list[dict] | None:
        logging.info(
            f"Scraping {len(inputs)} url(s)..."
        )
        try:
            response = requests.post(
                self.SCRAPE_URL,
                headers=self.headers,
                params={"dataset_id": self.DATASET_ID, "format": "json"},
                json=inputs,
                timeout=300,
            )
            response.raise_for_status()
            data = response.json()
            logging.info(f"Received {len(data)} records")
            self._save_data(data)
            return data
        except requests.exceptions.RequestException as e:
            logging.error(f"Scrape request failed: {str(e)}")
            return None

    def _save_data(
        self,
        data: list[dict[str, Any]],
        output_dir: str = "output_product_detail",
    ) -> None:
        try:
            Path(output_dir).mkdir(parents=True, exist_ok=True)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

            filename = os.path.join(output_dir, f"product_details_{timestamp}.json")    
            
            with open(filename, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            logging.info(f"Data saved to {filename}")
        except Exception as e:
            logging.error(f"Error saving data: {str(e)}")


def main() -> None:
    api_token = os.getenv("BRIGHTDATA_WEBSCRAPER_API_TOKEN")
    if not api_token:
        raise ValueError("API token not found. Please set BRIGHTDATA_WEBSCRAPER_API_TOKEN in your environment.")
        
    scraper = WayfairCollector(api_token)
    inputs = load_product_links("/Users/tieukbinh/Desktop/nam&son_data/how-to-scrape-wayfair/input_url_link/test.txt")

    scraper.collect_data(inputs)


if __name__ == "__main__":
    main()