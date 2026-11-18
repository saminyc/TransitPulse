# TransitPulse — Day 2 Findings

## Dataset
- Source: MTA Bus Route Segment Speeds
- Route: M15
- Period: March 2025

## Exploratory Analysis

These figures are for one selected M15 northbound local segment, using trip-count-weighted averages.

### 1. Hourly Travel Time

- Hour with highest average travel time: **14:00 (2 PM)** — **3.99 minutes**
- Hour with lowest average travel time: **02:00 (2 AM)** — **1.81 minutes**
- Notable observations: Travel time is lowest overnight (roughly 0–5), rises sharply after 6 AM, stays elevated through the daytime, peaks at 2 PM, then gradually declines into the evening.

### 2. Weekday vs Weekend

- Weekday average: **3.29 minutes**
- Weekend average: **3.03 minutes**
- Interpretation: Weekday travel time is about **0.25 minutes (15 seconds)** higher, consistent with heavier weekday traffic and service demand.

### 3. Day and Hour Patterns

- Most noticeable patterns: Every day shows low travel times overnight and higher times from morning through early evening. The heatmap’s strongest values occur around midday and afternoon—especially near 2–3 PM.
- Hours with limited data: All day-hour combinations exist, but each hour has only **9–14 records** for this selected segment. The sparsest hours are **0–6, 21–23**, with **9 records each**.


