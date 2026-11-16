"""Data-ingestion utilities for TransitPulse AI."""

from pathlib import Path

import pandas as pd
import requests

# Public MTA dataset API
API_URL = "https://data.ny.gov/resource/kufs-yh3x.json"

# Request only a manageable sample
params = {
    "$where": "route_id = 'M15' AND year = 2025",
    "$order": "month ASC, hour_of_day ASC",
    "$limit": 2000,
}

print("Connecting to the MTA Open Data API...")

response = requests.get(
    API_URL,
    params=params,
    timeout=60
)

if response.status_code != 200:
    response.raise_for_status()

# Convert the JSON response to a pandas DataFrame
data=response.json()
df = pd.DataFrame(data)

if df.empty:
    raise ValueError("No data returned from the API. Please check the query parameters.")

print("\nDownload Successful!")
print("\nRows: ", len(df))
print("\nColumns: ", len(df.columns))

print("\nFirst 5 records:")
print(df.head().to_string(index=False))

print("\n Column Names:")
print(df.columns.tolist())

# Save data to project's data/raw folder

output_dir=Path("data/raw")
output_dir.mkdir(parents=True, exist_ok=True)

output_path = output_dir / "bus_m15_sample.csv"

df.to_csv(output_path, index=False)

print(f"\nSaved data to: {output_path}")