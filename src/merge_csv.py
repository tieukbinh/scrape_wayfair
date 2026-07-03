import csv
from pathlib import Path

output_folder = Path('/Users/tieukbinh/Desktop/nam&son_data/how-to-scrape-wayfair/outputs')
merged_file_path = output_folder / 'merged_reviews.csv'

def get_clean_product_name(file_path: Path) -> str:
    """Strips the _YYYYMMDD_HHMMSS timestamp suffix from the file stem."""
    stem = file_path.stem  # e.g., "allmodern-florian-platform-bed_20260702_133548"
    
    # Split from the right side at the underscores to remove the time and date components
    # rsplit('_', 2) splits at the last two underscores: [product, date, time]
    parts = stem.rsplit('_', 2)
    
    return parts[0] # Returns just "allmodern-florian-platform-bed"

def merge_csv_files():
    # Exclude an existing merged file to prevent loop feedback
    csv_files = [f for f in output_folder.glob('*.csv') if f.name != 'merged_reviews.csv']
    
    if not csv_files:
        print("No CSV files found to merge.")
        return

    print(f"Found {len(csv_files)} files to merge...")

    with open(merged_file_path, 'w', newline='', encoding='utf-8') as master_file:
        writer = csv.writer(master_file)
        headers_written = False

        for file_path in csv_files:
            product_name = get_clean_product_name(file_path)
            
            with open(file_path, 'r', encoding='utf-8') as f:
                reader = csv.reader(f)
                
                try:
                    headers = next(reader)
                except StopIteration:
                    continue # Skip empty files safely

                # Write the header only ONCE, adding the new column name at the beginning
                if not headers_written:
                    writer.writerow(['product_name'] + headers)
                    headers_written = True

                # Write all remaining rows, prepending the clean product name
                for row in reader:
                    writer.writerow([product_name] + row)
                    
            print(f"Merged: {file_path.name} -> Label: {product_name}")

    print(f"\nSuccessfully merged everything into: {merged_file_path}")

if __name__ == "__main__":
    merge_csv_files()