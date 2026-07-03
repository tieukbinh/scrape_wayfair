#This script extracts review data from Wayfair HTML files and saves it to CSV files.
#It uses BeautifulSoup to parse the HTML and extract the relevant data from a specific div with the attribute 'data-tracking-metadata'.
#The extracted data includes review IDs, ratings, customer names, locations, dates, and review texts.
#The output CSV files are saved in a specified output folder with a timestamped filename.

import json
import csv
from bs4 import BeautifulSoup
from datetime import datetime
from pathlib import Path

input_folder = Path('/Users/tieukbinh/Desktop/nam&son_data/how-to-scrape-wayfair/html_inputs')
output_folder = Path('/Users/tieukbinh/Desktop/nam&son_data/how-to-scrape-wayfair/outputs')

def load_html(html_path:Path) -> str:
    with open(html_path, 'r', encoding='utf-8') as file:
        return file.read()
    
def get_output_path(html_path: Path) -> Path:
    product_name = html_path.stem.replace(" copy", "").replace(" ", "_")
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    filename = f"{product_name}_{timestamp}.csv"
    return output_folder / filename
   
def extract_reviews(html_content: str) -> list:
    soup = BeautifulSoup(html_content, 'html.parser')
    target_div = soup.find('div', {'data-tracking-metadata': True})

    if not target_div:
        print("Error: No div with 'data-tracking-metadata' found.")
        return {}
    
    raw_json_str = target_div['data-tracking-metadata']
    json_data = json.loads(raw_json_str)

    metadata = json_data.get('metadata', {})

    return {
        "ids": metadata.get('reviewIdList', []),
        "ratings": metadata.get('reviewRatingList', []),
        "names": metadata.get('reviewCustomerNameList', []),
        "locations": metadata.get('reviewLocationList', []),
        "dates": metadata.get('reviewDateList', []),
        "texts": metadata.get('reviewTextList', [])
    }

def write_csv(data: dict, csv_path: Path):
    with open(csv_path, 'w', newline='', encoding='utf-8') as csv_file:
        writer = csv.writer(csv_file)

        writer.writerow([
            'review_id',
            'rating',
            'name',
            'location',
            'date',
            'content'
        ])

        ids = data.get("ids", [])
        ratings = data.get("ratings", [])
        names = data.get("names", [])
        locations = data.get("locations", [])
        dates = data.get("dates", [])
        texts = data.get("texts", [])

        for i in range(len(ids)):
            writer.writerow([
                ids[i],
                ratings[i] if i < len(ratings) else '',
                names[i] if i < len(names) else '',
                locations[i] if i < len(locations) else '',
                dates[i] if i < len(dates) else '',
                texts[i] if i < len(texts) else ''
            ])

def process_html_file(html_path: Path):
    html_content = load_html(html_path)
    review_data = extract_reviews(html_content)

    if not review_data:
        print(f"No data found in {html_path}")
        return

    csv_path = get_output_path(html_path)
    write_csv(review_data, csv_path)
    print(f"Saved: {csv_path}")


def main():
    for html_path in input_folder.glob('*.html'):
        process_html_file(html_path)

if __name__ == "__main__":
    main()

