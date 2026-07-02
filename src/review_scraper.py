import json
import csv
from bs4 import BeautifulSoup
from datetime import datetime
from pathlib import Path


html_path = '/Users/tieukbinh/Desktop/nam&son_data/how-to-scrape-wayfair/web_htmls/amear_solid_wood_review.html'

product_name = Path(html_path).stem.replace(" copy", "").replace(" ", "_")
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
filename = f"{product_name}_{timestamp}.csv"
csv_filepath = f"{'/Users/tieukbinh/Desktop/nam&son_data/how-to-scrape-wayfair/outputs'}/{filename}"

# 1. Load the incomplete HTML file
with open(html_path, 'r', encoding='utf-8') as file:
    html_content = file.read()

# 2. Parse the HTML using BeautifulSoup
soup = BeautifulSoup(html_content, 'html.parser')

# Find the specific div containing the tracking data
target_div = soup.find('div', {'data-tracking-metadata': True})

if target_div:
    # 3. Extract and parse the embedded JSON string
    raw_json_str = target_div['data-tracking-metadata']
    json_data = json.loads(raw_json_str)
    
    # Drill down into the metadata dictionary
    metadata = json_data.get('metadata', {})
    
    # 4. Extract the parallel lists
    ids = metadata.get('reviewIdList', [])
    ratings = metadata.get('reviewRatingList', [])
    names = metadata.get('reviewCustomerNameList', [])
    locations = metadata.get('reviewLocationList', [])
    dates = metadata.get('reviewDateList', [])
    texts = metadata.get('reviewTextList', [])

    
    # 5. Zip them together and write to a CSV file
    with open(csv_filepath, 'w', newline='', encoding='utf-8') as csv_file:
        writer = csv.writer(csv_file)
        
        # Write headers
        writer.writerow(['Review ID', 'Rating', 'Customer Name', 'Location', 'Date', 'Text'])
        
        # Write rows by pairing elements from parallel lists
        for i in range(len(ids)):
            row = [
                ids[i] if i < len(ids) else '',
                ratings[i] if i < len(ratings) else '',
                names[i] if i < len(names) else '',
                locations[i] if i < len(locations) else '',
                dates[i] if i < len(dates) else '',
                texts[i] if i < len(texts) else ''
            ]
            writer.writerow(row)
            
    print(f"Data extraction complete! Saved to '{csv_filepath}'.")
else:
    print("Could not find the data-tracking-metadata attribute in the HTML.")