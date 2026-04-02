import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import csv
import requests

API_URL = "http://localhost:8000"

def load_csv(filepath):
    items = []
    with open(filepath, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            items.append({
                "title": row["title"],
                "description": f"{row['genre']}. {row['description']}"
            })
    return items

def ingest(items, batch_size=10):
    total = 0
    for i in range(0, len(items), batch_size):
        batch = items[i:i+batch_size]
        response = requests.post(
            f"{API_URL}/api/ingest",
            json={"items": batch}
        )
        if response.status_code == 200:
            total += len(batch)
            print(f"Ingested batch {i//batch_size + 1}: {len(batch)} items")
        else:
            print(f"Batch failed: {response.text}")
    print(f"\nDone. Total ingested: {total} items.")

if __name__ == "__main__":
    csv_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'movies.csv')
    print(f"Loading dataset...")
    items = load_csv(csv_path)
    print(f"Loaded {len(items)} items. Ingesting...")
    ingest(items)