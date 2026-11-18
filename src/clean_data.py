# Objective: Data Cleaning and Preprocessing of m15_march_2025.csv file for TransitPulse AI

import pandas as pd 
from pathlib import Path


df = pd.read_csv("data/raw/m15_march_2025.csv")

print("Available columns:")
print(df.columns.tolist())

# Finds columns that contain "travel_time" in their name (case-insensitive)
time_candidates = [
    col for col in df.columns
    if "travel_time" in col.lower()
]

print("\nTravel-time candidates:")
print(time_candidates) # Prints average_travel_time in the list

# Finds columns that contain "trips" in their name (case-insensitive)
trip_candidates = [
    col for col in df.columns
    if "trip" in col.lower()
]

print("\nTrip-count candidates:")
print(trip_candidates) # Prints empty in the list for this csv dataset

if len(time_candidates) != 1 or len(trip_candidates) != 1:
    raise ValueError(
        "Please inspect the printed columns and "
        "identify travel-time and trip-count fields."
    )

time_col = time_candidates[0]
trips_col = trip_candidates[0]



df = df.rename(columns={
    time_col: "travel_time_minutes",
    trips_col: "trip_count"
})

numeric_cols = [
    "travel_time_minutes",
    "trip_count",
    "hour_of_day",
    "month",
    "year"
]

for col in numeric_cols:
    df[col] = pd.to_numeric(df[col], errors="coerce")

# print(df["travel_time_minutes"]) tested and works fine returning the output

print("\nMissing values:")
print(df[numeric_cols].isna().sum())

print("\nRows before cleaning:", len(df))

# Remove records unusable for our analysis
df = df.dropna(subset=numeric_cols)

# Keeping df and cleaned_df separate to avoid confusion
cleaned_df = df[
    (df["travel_time_minutes"] > 0)
    & (df["trip_count"] > 0)
    & (df["hour_of_day"].between(0, 23))
].copy()

cleaned_df["hour_of_day"] = cleaned_df["hour_of_day"].astype(int)
cleaned_df["day_of_week"] = cleaned_df["day_of_week"].str.strip()

Path("data/processed").mkdir(parents=True, exist_ok=True)
cleaned_df.to_csv(
    "data/processed/m15_march_2025_clean.csv",
    index=False
)

print("Rows after cleaning:", len(cleaned_df))
print("\nTravel-time statistics:")
print(cleaned_df["travel_time_minutes"].describe())
