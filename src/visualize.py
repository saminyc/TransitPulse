
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

df = pd.read_csv(
    "data/processed/m15_march_2025_clean.csv"
)

output = Path("reports/figures")
output.mkdir(parents=True, exist_ok=True)

# Identify one consistent segment and service
segment_cols = [
    "route_id",
    "route_type",
    "direction",
    "timepoint_stop_id",
    "next_timepoint_stop_id"
]

segment_totals = (
    df.groupby(segment_cols, dropna=True)["trip_count"]
    .sum()
    .sort_values(ascending=False)
)

if segment_totals.empty:
    raise ValueError("No usable segments found.")

selected = segment_totals.index[0]

for col, value in zip(segment_cols, selected):
    df = df[df[col] == value]

print("Selected segment:", selected)
print("Records:", len(df))

# Weighted average: rows with more trips
# contribute more to the average.
def weighted_average(group):
    return (
        (group["travel_time_minutes"] *
         group["trip_count"]).sum()
        / group["trip_count"].sum()
    )

# CHART 1: Travel time by hour
hourly = (
    df.groupby("hour_of_day")
    .apply(weighted_average, include_groups=False)
    .sort_index()
)

plt.figure(figsize=(10, 5))
plt.plot(hourly.index, hourly.values, marker="o")
plt.title("M15 Segment: Average Travel Time by Hour")
plt.xlabel("Hour of Day")
plt.ylabel("Average Travel Time (minutes)")
plt.xticks(range(0, 24, 2))
plt.grid(alpha=0.3)
plt.tight_layout()
plt.savefig(output / "01_hourly_travel_time.png")
plt.close()

# CHART 2: Weekday vs weekend
weekdays = [
    "Monday", "Tuesday", "Wednesday",
    "Thursday", "Friday"
]

df["day_type"] = df["day_of_week"].apply(
    lambda d: "Weekday" if d in weekdays
    else "Weekend"
)

day_summary = (
    df.groupby("day_type")
    .apply(weighted_average, include_groups=False)
)

plt.figure(figsize=(7, 5))
day_summary.plot(kind="bar")
plt.title("Weekday vs Weekend Travel Time")
plt.ylabel("Average Travel Time (minutes)")
plt.xlabel("")
plt.xticks(rotation=0)
plt.tight_layout()
plt.savefig(output / "02_weekday_weekend.png")
plt.close()

# CHART 3: Heatmap by day and hour
days = [
    "Monday", "Tuesday", "Wednesday",
    "Thursday", "Friday", "Saturday", "Sunday"
]

day_hour = (
    df.groupby(["day_of_week", "hour_of_day"])
    .apply(weighted_average, include_groups=False)
    .unstack()
    .reindex(index=days, columns=range(24))
)

plt.figure(figsize=(12, 5))
plt.imshow(
    day_hour,
    aspect="auto",
    cmap="YlOrRd",
    interpolation="nearest"
)
plt.yticks(range(7), days)
plt.xticks(range(0, 24, 2), range(0, 24, 2))
plt.xlabel("Hour of Day")
plt.title("Travel Time by Day and Hour")
plt.colorbar(label="Average minutes")
plt.tight_layout()
plt.savefig(output / "03_day_hour_heatmap.png")
plt.close()

print("\nSaved three charts to reports/figures/")
print("\nHourly travel time:")
print(hourly.round(2))
print("\nWeekday/weekend averages:")
print(day_summary.round(2))
