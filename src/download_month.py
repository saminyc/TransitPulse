"""
We'll use March 2025 for our initial exploration.

Why March? It's a completed historical month, so we're not mixing incomplete current-month data into our analysis. 
Later, we'll add additional months for model training.
"""

from pathlib import Path
import time

import pandas as pd
import requests

URL = "https://data.ny.gov/resource/kufs-yh3x.json"

PAGE_SIZE = 5000 # Pagination limit for the API
all_rows = []
offset = 0



while True:
    params = {
        "$where": (
            "route_id = 'M15' "
            "AND year = 2025 "
            "AND month = 3" # March
        ),
        "$order": (
            "day_of_week, hour_of_day, route_type, "
            "direction, stop_order, "
            "timepoint_stop_id, next_timepoint_stop_id"
        ),
        "$limit": PAGE_SIZE,
        "$offset": offset
    }

    response = requests.get(
        URL, params=params, timeout=60
    )
    response.raise_for_status()

    rows = response.json() # Each batch of results
    all_rows.extend(rows) # Accumulate all results

    print(
        f"Downloaded {len(all_rows)} rows so far"
    )

    if len(rows) < PAGE_SIZE:
        break

    offset += PAGE_SIZE
    time.sleep(0.2)

# If all_rows is empty, raise an error
if not all_rows:
    raise ValueError("No records returned. Check API filters.")

# DataFrame creation using the accumulated rows
df = pd.DataFrame(all_rows)


Path("data/raw").mkdir(
    parents=True, exist_ok=True
)

df.to_csv(
    "data/raw/m15_march_2025.csv",
    index=False
)

print("\nTotal records:", len(df))
print("\nColumns:")
print(df.columns.tolist())
print("\nSaved successfully!")