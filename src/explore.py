"""Data-exploration utilities for TransitPulse AI."""

from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt

# Load the dataset
df = pd.read_csv("data/raw/bus_m15_sample.csv")

print("\n--- DATASET SHAPE ---")
print(df.shape)

print("\n--- COLUMNS NAMES ---")
print(df.columns.tolist())

print("\n--- FIRST FIVE ROWS ---")
print(df.head().to_string(index=False))

print("\n--- DATA TYPES ---")
print(df.dtypes)

print("\n--- MISSING VALUES ---")
print(df.isnull().sum().sort_values(ascending=False))

print("\n--- DUPLICATE ROWS ---")
print(df.duplicated().sum())

print("\n--- BASIC STATISTICS ---")
print(df.describe(include="all").to_string())


# Convert hour to numeric 
df["hour_of_day"] = pd.to_numeric(df["hour_of_day"], errors="coerce")

# Remove records without a usable hour
df = df.dropna(subset=["hour_of_day"]).copy()
df["hour_of_day"] = df["hour_of_day"].astype(int)

# Save the working dataset
output_dir = Path("data/processed")
output_dir.mkdir(parents=True, exist_ok=True)
df.to_csv(output_dir / "bus_m15_clean.csv", index=False)



# Explore how many records occur at each hour
hourly_counts = (
    df.groupby("hour_of_day")
    .size()
    .reindex(range(24), fill_value=0)
)

hourly_counts.plot(
    kind="bar",
    figsize=(10, 5)
)

plt.title("Records by Hour - M15 API Sample")
plt.xlabel("Hour of Day")
plt.ylabel("Number of Records")
plt.tight_layout()
plt.savefig("data/processed/hourly_records.png")
plt.show()

